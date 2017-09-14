
from __future__ import absolute_import, print_function, unicode_literals
import re
from collections import namedtuple
from functools import partial
from MidiRemoteScript import MutableVector
from ableton.v2.base import EventError, EventObject, const, depends, listenable_property, listens, liveobj_changed, liveobj_valid, mixin
from ableton.v2.control_surface import DeviceProvider as DeviceProviderBase
from ableton.v2.control_surface.control import control_list, ButtonControl
from ableton.v2.control_surface.mode import ModesComponent
from pushbase.device_component import DeviceComponent as DeviceComponentBase
from pushbase.parameter_provider import ParameterInfo
from .colors import COLOR_INDEX_TO_SCREEN_COLOR
from .device_decoration import InstrumentVectorFilterType, InstrumentVectorOscillatorType
from .device_parameter_bank_with_options import create_device_bank_with_options, OPTIONS_PER_BANK
from .real_time_channel import RealTimeDataComponent
from .parameter_mapping_sensitivities import PARAMETER_SENSITIVITIES, DEFAULT_SENSITIVITY_KEY, FINE_GRAINED_SENSITIVITY_KEY, parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity
from .routing import InputChannelRouter, InputChannelAndPositionRouter, InputTypeRouter, RoutingChannelList, RoutingChannelPositionList, RoutingMeterRealTimeChannelAssigner, RoutingTypeList
from .visualisation_settings import VisualisationGuides

def make_vector(items):
    vector = MutableVector()
    for item in items:
        vector.append(item)

    return vector


def parameter_sensitivities(device_class, parameter):
    sensitivities = {}
    try:
        param_name = parameter.name if liveobj_valid(parameter) else u''
        sensitivities = PARAMETER_SENSITIVITIES[device_class][param_name]
    except KeyError:
        pass

    for key, getter in ((DEFAULT_SENSITIVITY_KEY, parameter_mapping_sensitivity), (FINE_GRAINED_SENSITIVITY_KEY, fine_grain_parameter_mapping_sensitivity)):
        if key not in sensitivities:
            sensitivities[key] = getter(parameter)

    return sensitivities


class VisualisationLayout(object):
    button_width = 106
    button_gap = 15
    light_margin = 10


class Push2DeviceProvider(DeviceProviderBase):
    allow_update_callback = const(True)

    def update_device_selection(self):
        if self.allow_update_callback():
            super(Push2DeviceProvider, self).update_device_selection()


class DeviceComponentProvider(ModesComponent):
    u"""
    Provides the currently selected device, its options and parameters
    to other components.
    It has access to the device provider and listens to its device changes.
    When a new device is set, it chooses the right device component that knows how to
    handle behavior specific to the given device.
    """
    __events__ = (u'device',)

    @depends(device_provider=None)
    def __init__(self, device_component_layer = None, device_decorator_factory = None, banking_info = None, device_bank_registry = None, device_provider = None, *a, **k):
        super(DeviceComponentProvider, self).__init__(*a, **k)
        self._device_provider = device_provider
        self._visualisation_real_time_data = self.register_component(RealTimeDataComponent(channel_type=u'visualisation'))
        self.__on_visualisation_attached.subject = self._visualisation_real_time_data
        self.__on_visualisation_channel_changed.subject = self._visualisation_real_time_data
        self._device_component_modes = {}
        for mode_name, component_class in DEVICE_COMPONENT_MODES.iteritems():
            self._device_component_modes[mode_name] = component_class(device_decorator_factory=device_decorator_factory, banking_info=banking_info, device_bank_registry=device_bank_registry, device_provider=device_provider, name=u'{}DeviceComponent'.format(mode_name), visualisation_real_time_data=self._visualisation_real_time_data, is_enabled=False)

        for mode_name, device_component in self._device_component_modes.iteritems():
            self.add_mode(mode_name, [device_component, (device_component, device_component_layer)])

        self.selected_mode = u'Generic'
        self.__on_provided_device_changed.subject = device_provider
        self.__on_provided_device_changed()

    def set_device(self, device):
        self._device_provider.device = device

    def _set_device(self, device):
        name = device.class_name if device and device.class_name in self._device_component_modes else u'Generic'
        self.selected_mode = name
        device_component = self._device_component_modes[name]
        self.__on_parameters_changed.subject = device_component
        self.__on_shrink_parameters_changed.subject = device_component
        self.__on_options_changed.subject = device_component
        self.__on_visualisation_visible_changed.subject = device_component
        self._visualisation_real_time_data.set_data(device)
        self.notify_shrink_parameters()
        device_component.set_device(device)

    @property
    def device_component(self):
        return self._device_component_modes[self.selected_mode or u'Generic']

    @listenable_property
    def parameters(self):
        return self.device_component.parameters

    @listenable_property
    def shrink_parameters(self):
        return self.device_component.shrink_parameters

    @listenable_property
    def options(self):
        return self.device_component.options

    def device(self):
        return self.device_component.device()

    def device_changed(self, device):
        current_device = getattr(self.device(), u'_live_object', self.device())
        return liveobj_changed(current_device, device)

    @listens(u'device')
    def __on_provided_device_changed(self):
        device = self._device_provider.device
        if self.device_changed(device):
            self._set_device(device)
            self.notify_device()

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.notify_parameters()
        self.device_component.parameters_changed()

    @listens(u'shrink_parameters')
    def __on_shrink_parameters_changed(self):
        self.notify_shrink_parameters()

    @listens(u'options')
    def __on_options_changed(self):
        self.notify_options()

    @listens(u'attached')
    def __on_visualisation_attached(self):
        self.device_component.initialize_visualisation_view_data()

    @listens(u'channel_id')
    def __on_visualisation_channel_changed(self):
        self.notify_visualisation_real_time_channel_id()

    @listenable_property
    def visualisation_real_time_channel_id(self):
        if self.device_component.visualisation_visible:
            return self._visualisation_real_time_data.channel_id

    @listens(u'visualisation_visible')
    def __on_visualisation_visible_changed(self):
        self.notify_visualisation_real_time_channel_id()

    def disconnect(self):
        super(DeviceComponentProvider, self).disconnect()
        self._visualisation_real_time_data.set_data(None)


class GenericDeviceComponent(DeviceComponentBase):
    parameter_touch_buttons = control_list(ButtonControl, control_count=8)
    shift_button = ButtonControl()

    def __init__(self, visualisation_real_time_data = None, *a, **k):
        super(GenericDeviceComponent, self).__init__(*a, **k)
        self._visualisation_real_time_data = visualisation_real_time_data

    def _initialize_subcomponents(self):
        super(GenericDeviceComponent, self)._initialize_subcomponents()
        self.default_sensitivity = partial(self._sensitivity, DEFAULT_SENSITIVITY_KEY)
        self.fine_sensitivity = partial(self._sensitivity, FINE_GRAINED_SENSITIVITY_KEY)

    def set_device(self, device):
        self._set_device(device)

    def _set_device(self, device):
        super(GenericDeviceComponent, self)._set_device(device)
        self.notify_options()

    def _on_device_changed(self, device):
        u"""
        Override the base class behaviour, which calls _set_device when a device in
        the device provider changes. It's already donne by the DeviceComponentProvider.
        """
        pass

    @parameter_touch_buttons.pressed
    def parameter_touch_buttons(self, button):
        if button.index < len(self._provided_parameters):
            parameter = self._provided_parameters[button.index].parameter
            self._parameter_touched(parameter)

    @parameter_touch_buttons.released
    def parameter_touch_buttons(self, button):
        if button.index < len(self._provided_parameters):
            parameter = self._provided_parameters[button.index].parameter
            self._parameter_released(parameter)

    def parameters_changed(self):
        pass

    def _parameter_touched(self, parameter):
        pass

    def _parameter_released(self, parameter):
        pass

    @shift_button.pressed
    def shift_button(self, button):
        self._shift_button_pressed(button)

    @shift_button.released
    def shift_button(self, button):
        self._shift_button_released(button)

    def _shift_button_pressed(self, button):
        pass

    def _shift_button_released(self, button):
        pass

    def initialize_visualisation_view_data(self):
        view_data = self._initial_visualisation_view_data()
        if view_data:
            self._update_visualisation_view_data(view_data)

    def _update_visualisation_view_data(self, view_data):
        visualisation = self._visualisation_real_time_data.device_visualisation()
        if liveobj_valid(visualisation):
            visualisation_view_data = visualisation.get_view_data()
            for key, value in view_data.iteritems():
                visualisation_view_data[key] = value

            visualisation.set_view_data(visualisation_view_data)

    def _initial_visualisation_view_data(self):
        return {}

    def _is_parameter_available(self, parameter):
        return True

    def _create_parameter_info(self, parameter, name):
        return ParameterInfo(parameter=parameter if self._is_parameter_available(parameter) else None, name=name, default_encoder_sensitivity=self.default_sensitivity(parameter), fine_grain_encoder_sensitivity=self.fine_sensitivity(parameter))

    def _sensitivity(self, sensitivity_key, parameter):
        device = self.device()
        sensitivity = parameter_sensitivities(device.class_name, parameter)[sensitivity_key]
        if liveobj_valid(parameter):
            sensitivity = self._adjust_parameter_sensitivity(parameter, sensitivity)
        return sensitivity

    def _adjust_parameter_sensitivity(self, parameter, sensitivity):
        return sensitivity

    @listenable_property
    def options(self):
        return getattr(self._bank, u'options', [None] * OPTIONS_PER_BANK)

    @property
    def bank_view_description(self):
        return getattr(self._bank, u'bank_view_description', u'')

    @listenable_property
    def visualisation_visible(self):
        return self._visualisation_visible

    @property
    def _visualisation_visible(self):
        return False

    @listenable_property
    def shrink_parameters(self):
        return self._shrink_parameters

    @property
    def _shrink_parameters(self):
        return [False] * 8

    @listens(u'options')
    def __on_options_changed(self):
        self.notify_options()

    def _setup_bank(self, device):
        super(GenericDeviceComponent, self)._setup_bank(device, bank_factory=create_device_bank_with_options)
        try:
            self.__on_options_changed.subject = self._bank
        except EventError:
            pass


class DeviceComponentWithTrackColorViewData(GenericDeviceComponent):

    def _set_device(self, device):
        super(DeviceComponentWithTrackColorViewData, self)._set_device(device)
        self.__on_track_or_chain_color_changed.subject = device.canonical_parent if liveobj_valid(device) else None

    def _initial_visualisation_view_data(self):
        view_data = {}
        track_color = self._track_color_for_visualisation()
        if track_color is not None:
            view_data[u'TrackColor'] = track_color
        return view_data

    def _track_color_for_visualisation(self):
        device = self._decorated_device
        canonical_parent = device.canonical_parent if liveobj_valid(device) else None
        if liveobj_valid(canonical_parent) and canonical_parent.color_index is not None:
            color = COLOR_INDEX_TO_SCREEN_COLOR[canonical_parent.color_index]
            return color.as_remote_script_color()

    @listens(u'color_index')
    def __on_track_or_chain_color_changed(self):
        track_color = self._track_color_for_visualisation()
        if track_color is not None:
            self._update_visualisation_view_data({u'TrackColor': track_color})


class SimplerDeviceComponent(GenericDeviceComponent):
    ZOOM_SENSITIVE_PARAMETERS = (u'S Start', u'S Length', u'Start', u'End', u'Nudge')
    PARAMETERS_RELATIVE_TO_ACTIVE_AREA = (u'S Start', u'S Length')

    def _initialize_subcomponents(self):
        super(SimplerDeviceComponent, self)._initialize_subcomponents()
        self._playhead_real_time_data = self.register_component(RealTimeDataComponent(channel_type=u'playhead'))
        self._waveform_real_time_data = self.register_component(RealTimeDataComponent(channel_type=u'waveform'))
        self.__on_playhead_channel_changed.subject = self._playhead_real_time_data
        self.__on_waveform_channel_changed.subject = self._waveform_real_time_data

    def _set_device_for_subcomponents(self, device):
        super(SimplerDeviceComponent, self)._set_device_for_subcomponents(device)
        self._playhead_real_time_data.set_data(device)
        self._waveform_real_time_data.set_data(device)

    def _set_decorated_device_for_subcomponents(self, decorated_device):
        super(SimplerDeviceComponent, self)._set_decorated_device_for_subcomponents(decorated_device)
        self.__on_sample_or_file_path_changed.subject = decorated_device
        self.__on_waveform_visible_region_changed.subject = decorated_device
        if liveobj_valid(decorated_device):
            decorated_device.zoom.reset_focus_and_animation()

    def _parameter_touched(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            self._decorated_device.zoom.touch_object(parameter)

    def _parameter_released(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            self._decorated_device.zoom.release_object(parameter)

    def _is_parameter_available(self, parameter):
        name = parameter.name if liveobj_valid(parameter) else u''
        return not self._in_multisample_mode() or name not in self.ZOOM_SENSITIVE_PARAMETERS + (u'Zoom',)

    def _adjust_parameter_sensitivity(self, parameter, sensitivity):
        device = self._decorated_device
        if liveobj_valid(device) and liveobj_valid(device.sample):
            if parameter.name in self.ZOOM_SENSITIVE_PARAMETERS and device.waveform_navigation is not None:
                sensitivity *= device.waveform_navigation.visible_proportion
            if parameter.name in self.PARAMETERS_RELATIVE_TO_ACTIVE_AREA:
                active_area_quotient = device.sample.length / float(device.sample.end_marker - device.sample.start_marker + 1)
                sensitivity *= active_area_quotient
        return sensitivity

    @listens(u'channel_id')
    def __on_playhead_channel_changed(self):
        self._update_real_time_channel(u'playhead')

    @listens(u'channel_id')
    def __on_waveform_channel_changed(self):
        self._update_real_time_channel(u'waveform')

    @listens(u'sample.file_path')
    def __on_sample_or_file_path_changed(self):
        self._waveform_real_time_data.invalidate()

    @listens(u'waveform_navigation.visible_region')
    def __on_waveform_visible_region_changed(self, *a):
        self._update_parameter_sensitivities()

    def _update_parameter_sensitivities(self):
        changed_parameters = False
        for index, info in enumerate(self._provided_parameters):
            if info.name in self.ZOOM_SENSITIVE_PARAMETERS:
                self._provided_parameters[index] = self._create_parameter_info(info.parameter, info.name)
                changed_parameters = True

        if changed_parameters:
            self.notify_parameters()

    def _in_multisample_mode(self):
        return liveobj_valid(self._decorated_device) and self._decorated_device.multi_sample_mode

    def _update_real_time_channel(self, channel_name):
        if liveobj_valid(self._decorated_device):
            rt_data = getattr(self, u'_%s_real_time_data' % channel_name)
            setattr(self._decorated_device, channel_name + u'_real_time_channel_id', rt_data.channel_id)

    @property
    def wants_waveform_shown(self):
        return getattr(self._bank, u'wants_waveform_shown', True)

    def disconnect(self):
        super(SimplerDeviceComponent, self).disconnect()
        self._playhead_real_time_data.set_data(None)
        self._waveform_real_time_data.set_data(None)


class Eq8DeviceComponent(DeviceComponentWithTrackColorViewData):
    FILTER_BAND_PARAMETER_NAMES = re.compile(u'([1-8] [A-z ]+ [A])|(Scale)')

    def _parameter_touched(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            if self.FILTER_BAND_PARAMETER_NAMES.match(parameter.name):
                self._update_visualisation_view_data({u'AdjustingSelectedBand': True})
            elif parameter.name == u'Band':
                self._update_visualisation_view_data({u'ChangingSelectedBand': True})

    def _parameter_released(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            if not self._any_filter_band_parameter_touched():
                self._update_visualisation_view_data({u'AdjustingSelectedBand': False})
            if parameter.name == u'Band':
                self._update_visualisation_view_data({u'ChangingSelectedBand': False})

    def _any_filter_band_parameter_touched(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        return any([ self.FILTER_BAND_PARAMETER_NAMES.match(parameter.name) for parameter in touched_parameters ])

    def _initial_visualisation_view_data(self):
        view_data = super(Eq8DeviceComponent, self)._initial_visualisation_view_data()
        view_data[u'AdjustingSelectedBand'] = False
        view_data[u'ChangingSelectedBand'] = False
        return view_data

    @property
    def _visualisation_visible(self):
        return True

    @property
    def _shrink_parameters(self):
        return [True] * 8


class CompressorInputRouterMixin(object):

    class NullRoutingHost(EventObject):

        @listenable_property
        def available_input_routing_types(self):
            return []

        @listenable_property
        def input_routing_type(self):
            return None

        @listenable_property
        def available_input_routing_channels(self):
            return []

        @listenable_property
        def input_routing_channel(self):
            return None

    _compressor = None
    _null_routing_host = NullRoutingHost()
    _registered_listeners = []

    def _get_routing_host(self):
        if liveobj_valid(self._compressor):
            return self._compressor
        return self._null_routing_host

    def set_compressor(self, compressor):
        self._unregister_listeners()
        self._compressor = compressor
        self._register_listeners()
        self.__on_target_changed()
        self.notify_routing_targets()

    def _register_listeners(self):
        self._registered_listeners = [self.register_slot(subject=self._get_routing_host(), event_name=u'available_%ss' % self._current_target_property, listener=self.notify_routing_targets), self.register_slot(subject=self._get_routing_host(), event_name=self._current_target_property, listener=self.__on_target_changed)]

    def _unregister_listeners(self):
        for listener in self._registered_listeners:
            self.unregister_disconnectable(listener)
            listener.disconnect()

        self._registered_listeners = []

    def __on_target_changed(self):
        self.current_target_index = self._current_target_index()
        self.notify_current_target_index(self.current_target_index)


class CompressorDeviceComponent(DeviceComponentWithTrackColorViewData):

    @depends(real_time_mapper=None, register_real_time_data=None)
    def _initialize_subcomponents(self, real_time_mapper = None, register_real_time_data = None):
        super(CompressorDeviceComponent, self)._initialize_subcomponents()
        self._input_channel_router, self._input_type_router = self.register_disconnectables([mixin(CompressorInputRouterMixin, InputChannelRouter)(song=self.song), mixin(CompressorInputRouterMixin, InputTypeRouter)(song=self.song)])
        self._input_router = self.register_disconnectable(InputChannelAndPositionRouter(input_channel_router=self._input_channel_router, input_type_router=self._input_type_router))
        self._type_list = self.register_disconnectable(RoutingTypeList(parent_task_group=self._tasks, router=self._input_type_router))
        self._channel_list = self.register_disconnectable(RoutingChannelList(parent_task_group=self._tasks, rt_channel_assigner=self.register_component(RoutingMeterRealTimeChannelAssigner(real_time_mapper=real_time_mapper, register_real_time_data=register_real_time_data)), router=self._input_router))
        self._positions_list = self.register_disconnectable(RoutingChannelPositionList(input_channel_router=self._input_router))

    def _parameter_touched(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter) and parameter.name == u'Threshold':
            self._update_visualisation_view_data({u'AdjustingThreshold': True})

    def _parameter_released(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter) and parameter.name == u'Threshold':
            self._update_visualisation_view_data({u'AdjustingThreshold': False})

    def _set_device_for_subcomponents(self, device):
        super(CompressorDeviceComponent, self)._set_device_for_subcomponents(device)
        self._input_type_router.set_compressor(device)
        self._input_channel_router.set_compressor(device)

    def _set_decorated_device_for_subcomponents(self, decorated_device):
        super(CompressorDeviceComponent, self)._set_decorated_device_for_subcomponents(decorated_device)
        decorated_device.set_routing_infrastructure(self._input_router, self._type_list, self._channel_list, self._positions_list)

    def _set_bank_index(self, bank):
        super(CompressorDeviceComponent, self)._set_bank_index(bank)
        self.notify_visualisation_visible()

    def _initial_visualisation_view_data(self):
        view_data = super(CompressorDeviceComponent, self)._initial_visualisation_view_data()
        view_data[u'AdjustingThreshold'] = False
        view_data[u'VisualisationLeft'] = VisualisationLayout.light_margin
        view_data[u'VisualisationWidth'] = VisualisationLayout.button_width * 4 + VisualisationLayout.button_gap * 3 - VisualisationLayout.light_margin
        return view_data

    @property
    def _visualisation_visible(self):
        return self._bank.index == 0


BankEnvelopeConfig = namedtuple(u'BankEnvelopeConfig', [u'name_function', u'left_button_index', u'right_button_index'])

class OperatorDeviceComponent(DeviceComponentWithTrackColorViewData):

    @depends(real_time_mapper=None, register_real_time_data=None)
    def _initialize_subcomponents(self, real_time_mapper = None, register_real_time_data = None):
        super(OperatorDeviceComponent, self)._initialize_subcomponents()
        self._bank_envelope_configuration = {1: BankEnvelopeConfig(lambda : u'Operator%i' % self.selected_oscillator, 3, 6),
         3: BankEnvelopeConfig(const(u'Filter'), 2, 5),
         6: BankEnvelopeConfig(const(u'LFO'), 2, 5),
         8: BankEnvelopeConfig(const(u'Pitch'), 2, 5)}
        envelope_prefixes = [u'A',
         u'B',
         u'C',
         u'D',
         u'F',
         u'L',
         u'P']

        def parameter_names_for_feature(feature_name):
            return [ prefix + u'e ' + feature_name for prefix in envelope_prefixes ]

        feature_parameter_names = {u'InitNode': parameter_names_for_feature(u'Init'),
         u'AttackLine': parameter_names_for_feature(u'Init') + parameter_names_for_feature(u'Attack') + parameter_names_for_feature(u'Peak') + parameter_names_for_feature(u'A Slope'),
         u'AttackNode': parameter_names_for_feature(u'Attack') + parameter_names_for_feature(u'Peak'),
         u'DecayLine': parameter_names_for_feature(u'Attack') + parameter_names_for_feature(u'Peak') + parameter_names_for_feature(u'Decay') + parameter_names_for_feature(u'Sustain') + parameter_names_for_feature(u'D Slope'),
         u'DecayNode': parameter_names_for_feature(u'Decay') + parameter_names_for_feature(u'Sustain'),
         u'SustainLine': parameter_names_for_feature(u'Decay') + parameter_names_for_feature(u'Sustain'),
         u'SustainNode': parameter_names_for_feature(u'Sustain'),
         u'ReleaseLine': parameter_names_for_feature(u'Sustain') + parameter_names_for_feature(u'Release') + parameter_names_for_feature(u'End') + parameter_names_for_feature(u'R Slope'),
         u'ReleaseNode': parameter_names_for_feature(u'Release') + parameter_names_for_feature(u'End')}
        self._parameter_name_features = {}
        for feature_name, parameter_names in feature_parameter_names.iteritems():
            for parameter_name in parameter_names:
                parameter_feature_set = self._parameter_name_features.setdefault(parameter_name, set())
                parameter_feature_set.add(feature_name)

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._envelope_visualisation_data())

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._envelope_visualisation_data())

    def parameters_changed(self):
        self._update_visualisation_view_data(self._envelope_visualisation_data())

    def _set_bank_index(self, bank):
        super(OperatorDeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._envelope_visualisation_data())
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    def _set_decorated_device(self, decorated_device):
        super(OperatorDeviceComponent, self)._set_decorated_device(decorated_device)
        self.__on_selected_oscillator_changed.subject = decorated_device

    @property
    def selected_oscillator(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.oscillator_index
        return 0

    def _initial_visualisation_view_data(self):
        view_data = super(OperatorDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._envelope_visualisation_data())
        return view_data

    def _envelope_visualisation_data(self):
        config = self._bank_envelope_configuration.get(self._bank.index, BankEnvelopeConfig(const(u''), 0, 0))
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        shown_features = set([u'AttackLine',
         u'DecayLine',
         u'SustainLine',
         u'ReleaseLine'])
        for parameter in self.parameters:
            if parameter.parameter is not None:
                name = parameter.parameter.name
                if name in self._parameter_name_features:
                    shown_features |= self._parameter_name_features[name]

        focused_features = set()
        for parameter in touched_parameters:
            if parameter.parameter is not None:
                name = parameter.parameter.name
                if name in self._parameter_name_features:
                    focused_features |= self._parameter_name_features[name]

        return {u'EnvelopeName': config.name_function(),
         u'EnvelopeLeft': VisualisationGuides.light_left_x(config.left_button_index),
         u'EnvelopeRight': VisualisationGuides.light_right_x(config.right_button_index),
         u'EnvelopeShow': make_vector(list(shown_features)),
         u'EnvelopeFocus': make_vector(list(focused_features))}

    @listens(u'oscillator_index')
    def __on_selected_oscillator_changed(self):
        self._update_visualisation_view_data(self._envelope_visualisation_data())

    @property
    def _visualisation_visible(self):
        return self._bank != None and self._bank.index in self._bank_envelope_configuration

    @property
    def _shrink_parameters(self):
        if self._visualisation_visible:
            config = self._bank_envelope_configuration[self._bank.index]
            return [ config.left_button_index <= index <= config.right_button_index for index in xrange(8) ]
        else:
            return [False] * 8


class InstrumentVectorDeviceComponent(DeviceComponentWithTrackColorViewData):
    OSCILLATOR_POSITION_PARAMETER_NAMES = re.compile(u'^(Osc (1|2) Pos)$|^Position$')
    FILTER_PARAMETER_NAMES = re.compile(u'^(Filter (1|2) (Type|Freq|Res))$|^Filter Type$|^Frequency$|^Resonance$')

    def _parameter_touched(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            view_data = {}
            self._update_single_selected_parameter()
            if self.OSCILLATOR_POSITION_PARAMETER_NAMES.match(parameter.name):
                view_data[u'AdjustingPosition'] = True
            if self.FILTER_PARAMETER_NAMES.match(parameter.name):
                view_data[u'AdjustingFilter'] = True
            if view_data:
                self._update_visualisation_view_data(view_data)

    def _parameter_released(self, parameter):
        if liveobj_valid(self._decorated_device) and liveobj_valid(parameter):
            view_data = {}
            self._update_single_selected_parameter()
            if self.OSCILLATOR_POSITION_PARAMETER_NAMES.match(parameter.name):
                view_data[u'AdjustingPosition'] = False
            if not self._any_filter_parameter_touched():
                view_data[u'AdjustingFilter'] = False
            if view_data:
                self._update_visualisation_view_data(view_data)

    def _shift_button_pressed(self, button):
        self._decorated_device.osc_1_pitch.adjust_finegrain = True
        self._decorated_device.osc_2_pitch.adjust_finegrain = True

    def _shift_button_released(self, button):
        self._decorated_device.osc_1_pitch.adjust_finegrain = False
        self._decorated_device.osc_2_pitch.adjust_finegrain = False

    def _set_decorated_device(self, decorated_device):
        super(InstrumentVectorDeviceComponent, self)._set_decorated_device(decorated_device)
        self.__on_selected_oscillator_changed.subject = decorated_device
        self.__on_selected_filter_changed.subject = decorated_device
        self.__on_request_mod_matrix_bank_view.subject = decorated_device

    def _set_bank_index(self, bank):
        super(InstrumentVectorDeviceComponent, self)._set_bank_index(bank)
        self._update_single_selected_parameter()
        self._update_visualisation_view_data({u'WavetableVisualisationStart': VisualisationGuides.light_left_x(1) if bank == 1 else VisualisationGuides.light_left_x(0),
         u'WavetableVisualisationVisible': self.wavetable_visualisation_visible,
         u'FilterVisualisationVisible': self.filter_visualisation_visible})
        self.notify_visualisation_visible()
        self.notify_wavetable_visualisation_visible()
        self.notify_filter_visualisation_visible()

    def _update_single_selected_parameter(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        self._decorated_device.set_single_selected_parameter(touched_parameters[0].parameter if len(touched_parameters) == 1 else None)

    def _any_filter_parameter_touched(self):
        touched_parameters = [ self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed ]
        return any([ self.FILTER_PARAMETER_NAMES.match(parameter.name) for parameter in touched_parameters ])

    @property
    def _visualisation_visible(self):
        return self.wavetable_visualisation_visible or self.filter_visualisation_visible

    @listenable_property
    def wavetable_visualisation_visible(self):
        return self._bank.index < 2 and self.selected_oscillator in [InstrumentVectorOscillatorType.one, InstrumentVectorOscillatorType.two]

    @listenable_property
    def filter_visualisation_visible(self):
        return self._bank.index == 0

    @property
    def selected_oscillator(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.oscillator_index
        return 0

    @property
    def selected_filter(self):
        if liveobj_valid(self._decorated_device):
            return self._decorated_device.filter_index
        return 0

    @property
    def visualisation_width(self):
        return VisualisationGuides.light_right_x(2) - VisualisationGuides.light_left_x(0)

    def _initial_visualisation_view_data(self):
        view_data = super(InstrumentVectorDeviceComponent, self)._initial_visualisation_view_data()
        view_data[u'SelectedOscillator'] = self.selected_oscillator
        view_data[u'AdjustingPosition'] = False
        view_data[u'AdjustingFilter'] = False
        view_data[u'WavetableVisualisationStart'] = VisualisationGuides.light_left_x(0)
        view_data[u'WavetableVisualisationWidth'] = self.visualisation_width
        view_data[u'FilterCurveVisualisationStart'] = VisualisationGuides.light_left_x(3)
        view_data[u'FilterCurveVisualisationWidth'] = self.visualisation_width
        view_data[u'WavetableVisualisationVisible'] = True
        view_data[u'FilterVisualisationVisible'] = True
        view_data[u'SelectedFilter'] = InstrumentVectorFilterType.one
        return view_data

    @listens(u'request_mod_matrix_bank_view')
    def __on_request_mod_matrix_bank_view(self):
        MOD_MATRIX_BANK_INDEX = 5
        self._device_bank_registry.set_device_bank(self._device_provider.device, MOD_MATRIX_BANK_INDEX)

    @listens(u'oscillator_index')
    def __on_selected_oscillator_changed(self):
        self._update_visualisation_view_data({u'SelectedOscillator': self.selected_oscillator,
         u'WavetableVisualisationVisible': self.wavetable_visualisation_visible})
        self.notify_visualisation_visible()
        self.notify_wavetable_visualisation_visible()

    @listens(u'filter_index')
    def __on_selected_filter_changed(self):
        self._update_visualisation_view_data({u'SelectedFilter': self.selected_filter})


DEVICE_COMPONENT_MODES = {u'Generic': GenericDeviceComponent,
 u'OriginalSimpler': SimplerDeviceComponent,
 u'Eq8': Eq8DeviceComponent,
 u'Compressor2': CompressorDeviceComponent,
 u'InstrumentVector': InstrumentVectorDeviceComponent,
 u'Operator': OperatorDeviceComponent}