
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import EventObject, depends, find_if, listenable_property, listens, liveobj_valid
from pushbase.decoration import LiveObjectDecorator, DecoratorFactory
from pushbase.internal_parameter import EnumWrappingParameter, InternalParameter
from pushbase.message_box_component import Messenger
from pushbase.simpler_decoration import BoolWrappingParameter, SimplerDeviceDecorator as SimplerDeviceDecoratorBase
from .device_options import DeviceTriggerOption, DeviceSwitchOption, DeviceOnOffOption
from .timeline_navigation import Region, SimplerWaveformNavigation
RESET_SLICING_NOTIFICATION = u'Slicing has been reset'
MAX_NUMBER_SLICES = 64

def get_parameter_by_name(decorator, name):
    return find_if(lambda p: p.name == name, decorator._live_object.parameters)


class EnvelopeType(int):
    pass


EnvelopeType.volume_env = EnvelopeType(0)
EnvelopeType.filter_env = EnvelopeType(1)
EnvelopeType.pitch_env = EnvelopeType(2)

class OscillatorType(int):
    pass


OscillatorType.a = OscillatorType(0)
OscillatorType.b = OscillatorType(1)
OscillatorType.c = OscillatorType(2)
OscillatorType.d = OscillatorType(3)

class NotifyingList(EventObject):
    __events__ = (u'index',)

    def __init__(self, available_values, default_value = None, *a, **k):
        super(NotifyingList, self).__init__(*a, **k)
        self._index = default_value if default_value is not None else 0
        self._available_values = available_values

    @property
    def available_values(self):
        return self._available_values

    def _get_index(self):
        return self._index

    def _set_index(self, value):
        if value < 0 or value >= len(self.available_values):
            raise IndexError
        self._index = value
        self.notify_index()

    index = property(_get_index, _set_index)


class EnvelopeTypesList(NotifyingList):

    def __init__(self):
        super(EnvelopeTypesList, self).__init__(available_values=[u'Volume', u'Filter', u'Pitch'], default_value=EnvelopeType.volume_env)


class OscillatorTypesList(NotifyingList):

    def __init__(self):
        super(OscillatorTypesList, self).__init__(available_values=[u'A',
         u'B',
         u'C',
         u'D'], default_value=OscillatorType.a)


class WaveformNavigationParameter(InternalParameter):
    u""" Class for connecting a Simpler with a WaveformNavigation. It will create a new
        instance of WaveformNavigation for every sample. It also still acts as a
        parameter, for the current zooming implemenation.
    
        It also provides the "zoom" method interface, so it works with the
        pushbase.mapped_control.MappedControl class.
    """

    def __init__(self, simpler = None, *a, **k):
        super(WaveformNavigationParameter, self).__init__(*a, **k)
        self._simpler = simpler
        self._waveform_navigation = None
        self.post_sample_changed()

    @listenable_property
    def waveform_navigation(self):
        return self._waveform_navigation

    @property
    def visible_region(self):
        if self._waveform_navigation:
            return self._waveform_navigation.visible_region
        return Region(0, 1)

    @visible_region.setter
    def visible_region(self, region):
        if self._waveform_navigation:
            self._waveform_navigation.visible_region = region

    def set_visible_region(self, region):
        if self._waveform_navigation:
            self._waveform_navigation.set_visible_region(region)

    def zoom(self, value):
        if self._waveform_navigation:
            self._waveform_navigation.zoom(value)

    def touch_object(self, parameter):
        if self._waveform_navigation:
            self._waveform_navigation.touch_object(parameter)

    def release_object(self, parameter):
        if self._waveform_navigation:
            self._waveform_navigation.release_object(parameter)

    def change_object(self, parameter):
        if self._waveform_navigation:
            self._waveform_navigation.change_object(parameter)

    def focus_object(self, parameter):
        if self._waveform_navigation:
            self._waveform_navigation.focus_object(parameter)

    def focus_region_of_interest(self, roi_identifier, focused_object):
        if self._waveform_navigation:
            self._waveform_navigation.focus_region_of_interest(roi_identifier, focused_object)

    def reset_focus_and_animation(self):
        if self._waveform_navigation:
            self._waveform_navigation.reset_focus_and_animation()

    def post_sample_changed(self):
        sample = self._simpler.sample
        if self._waveform_navigation is not None:
            self.unregister_disconnectable(self._waveform_navigation)
            self._waveform_navigation.disconnect()
        if liveobj_valid(sample):
            self._waveform_navigation = self.register_disconnectable(SimplerWaveformNavigation(simpler=self._simpler))
        else:
            self._waveform_navigation = None
        self.notify_waveform_navigation()


class SlicePoint(object):

    def __init__(self, identifier, time):
        self.__id__ = identifier
        self.time = time

    def __eq__(self, other):
        if isinstance(other, SlicePoint):
            return self.__id__ == other.__id__ and self.time == other.time
        return False

    def __ne__(self, other):
        return not self == other


class SimplerPositions(EventObject):
    __events__ = (u'warp_markers', u'before_update_all', u'after_update_all')
    start = listenable_property.managed(0.0)
    end = listenable_property.managed(0.0)
    start_marker = listenable_property.managed(0.0)
    end_marker = listenable_property.managed(0.0)
    active_start = listenable_property.managed(0.0)
    active_end = listenable_property.managed(0.0)
    loop_start = listenable_property.managed(0.0)
    loop_end = listenable_property.managed(0.0)
    loop_fade_in_samples = listenable_property.managed(0.0)
    env_fade_in = listenable_property.managed(0.0)
    env_fade_out = listenable_property.managed(0.0)
    slices = listenable_property.managed([])
    selected_slice = listenable_property.managed(SlicePoint(0, 0.0))
    use_beat_time = listenable_property.managed(False)

    def __init__(self, simpler = None, *a, **k):
        raise simpler is not None or AssertionError
        super(SimplerPositions, self).__init__(*a, **k)
        self._simpler = simpler
        self.__on_active_start_changed.subject = simpler.view
        self.__on_active_end_changed.subject = simpler.view
        self.__on_loop_start_changed.subject = simpler.view
        self.__on_loop_end_changed.subject = simpler.view
        self.__on_loop_fade_changed.subject = simpler.view
        self.__on_env_fade_in_changed.subject = simpler.view
        self.__on_env_fade_out_changed.subject = simpler.view
        self.__on_selected_slice_changed.subject = simpler.view
        self.post_sample_changed()

    def post_sample_changed(self):
        self.__on_start_marker_changed.subject = self._simpler.sample
        self.__on_end_marker_changed.subject = self._simpler.sample
        self.__on_slices_changed.subject = self._simpler.sample
        self.__on_warping_changed.subject = self._simpler.sample
        self.__on_warp_markers_changed.subject = self._simpler.sample
        self.update_all()

    def _convert_sample_time(self, sample_time):
        u"""
        Converts to beat time, if the sample is warped
        """
        sample = self._simpler.sample
        if liveobj_valid(sample) and sample.warping:
            return sample.sample_to_beat_time(sample_time)
        return sample_time

    @listens(u'start_marker')
    def __on_start_marker_changed(self):
        if liveobj_valid(self._simpler.sample):
            self.start_marker = self._convert_sample_time(self._simpler.sample.start_marker)

    @listens(u'end_marker')
    def __on_end_marker_changed(self):
        if liveobj_valid(self._simpler.sample):
            self.end_marker = self._convert_sample_time(self._simpler.sample.end_marker)

    @listens(u'sample_start')
    def __on_active_start_changed(self):
        self.active_start = self._convert_sample_time(self._simpler.view.sample_start)

    @listens(u'sample_end')
    def __on_active_end_changed(self):
        self.active_end = self._convert_sample_time(self._simpler.view.sample_end)

    @listens(u'sample_loop_start')
    def __on_loop_start_changed(self):
        self.loop_start = self._convert_sample_time(self._simpler.view.sample_loop_start)

    @listens(u'sample_loop_end')
    def __on_loop_end_changed(self):
        self.loop_end = self._convert_sample_time(self._simpler.view.sample_loop_end)

    @listens(u'sample_loop_fade')
    def __on_loop_fade_changed(self):
        self.loop_fade_in_samples = self._simpler.view.sample_loop_fade

    @listens(u'sample_env_fade_in')
    def __on_env_fade_in_changed(self):
        if liveobj_valid(self._simpler.sample):
            start_marker = self._simpler.sample.start_marker
            fade_in_end = start_marker + self._simpler.view.sample_env_fade_in
            self.env_fade_in = self._convert_sample_time(fade_in_end) - self._convert_sample_time(start_marker)

    @listens(u'sample_env_fade_out')
    def __on_env_fade_out_changed(self):
        if liveobj_valid(self._simpler.sample):
            end_marker = self._simpler.sample.end_marker
            fade_out_start = end_marker - self._simpler.view.sample_env_fade_out
            self.env_fade_out = self._convert_sample_time(end_marker) - self._convert_sample_time(fade_out_start)

    @listens(u'slices')
    def __on_slices_changed(self):
        if liveobj_valid(self._simpler.sample):
            self.slices = [ SlicePoint(s, self._convert_sample_time(s)) for s in self._simpler.sample.slices ]

    @listens(u'selected_slice')
    def __on_selected_slice_changed(self):
        if liveobj_valid(self._simpler.sample):
            t = self._convert_sample_time(self._simpler.view.selected_slice)
            self.selected_slice = SlicePoint(t, t)

    @listens(u'warping')
    def __on_warping_changed(self):
        self.update_all()

    @listens(u'warp_markers')
    def __on_warp_markers_changed(self):
        self.update_all()
        self.notify_warp_markers()

    def update_all(self):
        if liveobj_valid(self._simpler.sample):
            self.notify_before_update_all()
            self.start = self._convert_sample_time(0)
            self.end = self._convert_sample_time(self._simpler.sample.length)
            self.__on_start_marker_changed()
            self.__on_end_marker_changed()
            self.__on_active_start_changed()
            self.__on_active_end_changed()
            self.__on_loop_start_changed()
            self.__on_loop_end_changed()
            self.__on_loop_fade_changed()
            self.__on_env_fade_in_changed()
            self.__on_env_fade_out_changed()
            self.__on_slices_changed()
            self.__on_selected_slice_changed()
            self.use_beat_time = self._simpler.sample.warping
            self.notify_after_update_all()


def center_point(start, end):
    return int((end - start) / 2.0) + start


def insert_new_slice(simpler):
    sample = simpler.sample
    view = simpler.view
    slices = list(sample.slices) + [sample.end_marker]
    selected_slice = view.selected_slice
    if selected_slice in slices:
        slice_index = slices.index(selected_slice)
        new_slice_point = center_point(selected_slice, slices[slice_index + 1])
        if new_slice_point not in slices:
            sample.insert_slice(new_slice_point)
            view.selected_slice = new_slice_point


class _SimplerDeviceDecorator(SimplerDeviceDecoratorBase, Messenger):
    waveform_real_time_channel_id = u''
    playhead_real_time_channel_id = u''

    def __init__(self, song = None, envelope_types_provider = None, *a, **k):
        self._song = song
        self._envelope_types_provider = envelope_types_provider if envelope_types_provider is not None else EnvelopeTypesList()
        super(_SimplerDeviceDecorator, self).__init__(*a, **k)
        self.setup_options()
        self.register_disconnectables(self.options)
        self.__on_parameters_changed.subject = self._live_object
        self.__on_signature_numerator_changed.subject = song
        self.__on_can_warp_as_changed.subject = self._live_object
        self.__on_can_warp_half_changed.subject = self._live_object
        self.__on_can_warp_double_changed.subject = self._live_object
        self.__on_start_marker_changed.subject = self._live_object.sample
        self.__on_end_marker_changed.subject = self._live_object.sample
        self.__on_selected_slice_changed.subject = self._live_object.view

    def setup_parameters(self):
        super(_SimplerDeviceDecorator, self).setup_parameters()
        self.positions = self.register_disconnectable(SimplerPositions(self))
        self.zoom = WaveformNavigationParameter(name=u'Zoom', parent=self, simpler=self)
        self.zoom.focus_region_of_interest(u'start_end_marker', self.get_parameter_by_name(u'Start'))
        self.zoom.add_waveform_navigation_listener(self.notify_waveform_navigation)
        self.envelope = EnumWrappingParameter(name=u'Env. Type', parent=self, values_host=self._envelope_types_provider, index_property_host=self._envelope_types_provider, values_property=u'available_values', index_property=u'index', value_type=EnvelopeType)
        self._additional_parameters.extend([self.zoom, self.envelope])

    def setup_options(self):

        def get_simpler_flag(name):
            return liveobj_valid(self._live_object) and getattr(self._live_object, name)

        def call_simpler_function(name, *a):
            if liveobj_valid(self._live_object):
                return getattr(self._live_object, name)(*a)

        def sample_available():
            return liveobj_valid(self._live_object) and liveobj_valid(self._live_object.sample)

        def call_sample_function(name, *a):
            if sample_available():
                return getattr(self._live_object.sample, name)(*a)

        def reset_slices():
            call_sample_function(u'reset_slices')
            self.show_notification(RESET_SLICING_NOTIFICATION)

        def split_slice_available():
            if sample_available():
                slices = self._live_object.sample.slices
                return len(slices) != MAX_NUMBER_SLICES or slices[-1] != self._live_object.view.selected_slice
            return False

        self.crop_option = DeviceTriggerOption(name=u'Crop', callback=partial(call_simpler_function, u'crop'))
        self.reverse_option = DeviceTriggerOption(name=u'Reverse', callback=partial(call_simpler_function, u'reverse'))
        self.one_shot_sustain_mode_option = DeviceSwitchOption(name=u'Trigger Mode', parameter=get_parameter_by_name(self, u'Trigger Mode'))
        self.retrigger_option = DeviceOnOffOption(name=u'Retrigger', property_host=self._live_object, property_name=u'retrigger')
        self.warp_as_x_bars_option = DeviceTriggerOption(name=u'Warp as X Bars', default_label=self.get_warp_as_option_label(), callback=lambda : call_simpler_function(u'warp_as', call_simpler_function(u'guess_playback_length')), is_active=lambda : get_simpler_flag(u'can_warp_as'))
        self.warp_half_option = DeviceTriggerOption(name=u':2', callback=partial(call_simpler_function, u'warp_half'), is_active=lambda : get_simpler_flag(u'can_warp_half'))
        self.warp_double_option = DeviceTriggerOption(name=u'x2', callback=partial(call_simpler_function, u'warp_double'), is_active=lambda : get_simpler_flag(u'can_warp_double'))
        self.lfo_sync_option = DeviceSwitchOption(name=u'LFO Sync Type', parameter=get_parameter_by_name(self, u'L Sync'))
        self.loop_option = DeviceOnOffOption(name=u'Loop', property_host=get_parameter_by_name(self, u'S Loop On'), property_name=u'value')
        self.filter_slope_option = DeviceSwitchOption(name=u'Filter Slope', parameter=get_parameter_by_name(self, u'Filter Slope'))
        self.clear_slices_action = DeviceTriggerOption(name=u'Clear Slices', default_label=u'Clear Slices', callback=lambda : call_sample_function(u'clear_slices'), is_active=lambda : sample_available() and len(self._live_object.sample.slices) > 1)
        self.reset_slices_action = DeviceTriggerOption(name=u'Reset Slices', default_label=u'Reset Slices', callback=reset_slices, is_active=lambda : sample_available())
        self.split_slice_action = DeviceTriggerOption(name=u'Split Slice', default_label=u'Split Slice', callback=lambda : insert_new_slice(self._live_object), is_active=split_slice_available)

    def get_parameter_by_name(self, name):
        return find_if(lambda p: p.name == name, self.parameters)

    @property
    def options(self):
        return (self.crop_option,
         self.reverse_option,
         self.one_shot_sustain_mode_option,
         self.retrigger_option,
         self.warp_as_x_bars_option,
         self.warp_half_option,
         self.warp_double_option,
         self.lfo_sync_option,
         self.loop_option,
         self.filter_slope_option,
         self.clear_slices_action,
         self.reset_slices_action,
         self.split_slice_action)

    @listenable_property
    def waveform_navigation(self):
        return self.zoom.waveform_navigation

    @property
    def available_resolutions(self):
        return (u'1 Bar', u'\xbd', u'\xbc', u'\u215b', u'\ue001', u'\ue002', u'Transients')

    @property
    def available_slicing_beat_divisions(self):
        return (u'\ue001', u'\ue001T', u'\u215b', u'\u215bT', u'\xbc', u'\xbcT', u'\xbd', u'\xbdT', u'1 Bar', u'2 Bars', u'4 Bars')

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.lfo_sync_option.set_parameter(get_parameter_by_name(self, u'L Sync'))
        self.filter_slope_option.set_parameter(get_parameter_by_name(self, u'Filter Slope'))

    def _reconnect_sample_listeners(self):
        super(_SimplerDeviceDecorator, self)._reconnect_sample_listeners()
        self._reconnect_to_markers()
        self._update_warp_as_label()
        self.positions.post_sample_changed()
        self.zoom.post_sample_changed()
        self.zoom.focus_region_of_interest(u'start_end_marker', self.get_parameter_by_name(u'Start'))

    def _reconnect_to_markers(self):
        self.__on_start_marker_changed.subject = self._live_object.sample
        self.__on_end_marker_changed.subject = self._live_object.sample

    def _update_warp_as_label(self):
        self.warp_as_x_bars_option.default_label = self.get_warp_as_option_label()

    @listens(u'start_marker')
    def __on_start_marker_changed(self):
        self._update_warp_as_label()

    @listens(u'end_marker')
    def __on_end_marker_changed(self):
        self._update_warp_as_label()

    @listens(u'signature_numerator')
    def __on_signature_numerator_changed(self):
        self._update_warp_as_label()

    @listens(u'can_warp_as')
    def __on_can_warp_as_changed(self):
        self.warp_as_x_bars_option.notify_active()

    @listens(u'can_warp_half')
    def __on_can_warp_half_changed(self):
        self.warp_half_option.notify_active()

    @listens(u'can_warp_double')
    def __on_can_warp_double_changed(self):
        self.warp_double_option.notify_active()

    @listens(u'selected_slice')
    def __on_selected_slice_changed(self):
        self.split_slice_action.notify_active()

    def _on_sample_changed(self):
        super(_SimplerDeviceDecorator, self)._on_sample_changed()
        self.clear_slices_action.notify_active()
        self.reset_slices_action.notify_active()
        self.split_slice_action.notify_active()

    def _on_slices_changed(self):
        super(_SimplerDeviceDecorator, self)._on_slices_changed()
        self.clear_slices_action.notify_active()

    def get_warp_as_option_label(self):
        try:
            bars = int(self._live_object.guess_playback_length() / self._song.signature_numerator)
            return u'Warp as %d Bar%s' % (bars, u's' if bars > 1 else u'')
        except RuntimeError:
            return u'Warp as X Bars'


class _OperatorDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, song = None, osc_types_provider = None, *a, **k):
        super(_OperatorDeviceDecorator, self).__init__(*a, **k)
        self._osc_types_provider = osc_types_provider if osc_types_provider is not None else OscillatorTypesList()
        self.__on_parameters_changed.subject = self._live_object
        self.oscillator = EnumWrappingParameter(name=u'Oscillator', parent=self, values_host=self._osc_types_provider, index_property_host=self._osc_types_provider, values_property=u'available_values', index_property=u'index', value_type=OscillatorType)
        self.filter_slope_option = DeviceSwitchOption(name=u'Filter Slope', parameter=get_parameter_by_name(self, u'Filter Slope'))
        self.register_disconnectables(self.options)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + (self.oscillator,)

    @property
    def options(self):
        return (self.filter_slope_option,)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.filter_slope_option.set_parameter(get_parameter_by_name(self, u'Filter Slope'))


class _SamplerDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, song = None, *a, **k):
        super(_SamplerDeviceDecorator, self).__init__(*a, **k)
        self.__on_parameters_changed.subject = self._live_object
        self.filter_slope_option = DeviceSwitchOption(name=u'Filter Slope', parameter=get_parameter_by_name(self, u'Filter Slope'))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.filter_slope_option,)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.filter_slope_option.set_parameter(get_parameter_by_name(self, u'Filter Slope'))


class _AutoFilterDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, song = None, *a, **k):
        super(_AutoFilterDeviceDecorator, self).__init__(*a, **k)
        self.__on_parameters_changed.subject = self._live_object
        self.slope_option = DeviceSwitchOption(name=u'Slope', parameter=get_parameter_by_name(self, u'Slope'))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.slope_option,)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.slope_option.set_parameter(get_parameter_by_name(self, u'Slope'))


class _Eq8DeviceDecorator(EventObject, LiveObjectDecorator):
    available_band_indices = range(1, 9)
    available_global_modes = [u'Stereo', u'Left/Right', u'Mid/Side']

    def __init__(self, song = None, *a, **k):
        super(_Eq8DeviceDecorator, self).__init__(*a, **k)
        self.band = EnumWrappingParameter(name=u'Band', parent=self, values_host=self, index_property_host=self.view, values_property=u'available_band_indices', index_property=u'selected_band')
        self.mode = EnumWrappingParameter(name=u'Eq Mode', parent=self, values_host=self, index_property_host=self, values_property=u'available_global_modes', index_property=u'global_mode')
        self.edit_switch = BoolWrappingParameter(name=u'Edit Mode', parent=self, property_host=self, source_property=u'edit_mode')
        self.oversampling = BoolWrappingParameter(name=u'Oversampling', parent=self, property_host=self, source_property=u'oversample')
        self.left_right_curve_switch_option = DeviceSwitchOption(name=u'Left/Right', labels=[u'Left', u'Right'], parameter=self.edit_switch)
        self.mid_side_curve_switch_option = DeviceSwitchOption(name=u'Mid/Side', labels=[u'Mid', u'Side'], parameter=self.edit_switch)
        self._additional_parameters = (self.band,
         self.mode,
         self.edit_switch,
         self.oversampling)
        self._additional_options = (self.left_right_curve_switch_option, self.mid_side_curve_switch_option)
        self.register_disconnectables(self._additional_parameters + self._additional_options)
        self.__on_parameters_changed.subject = self

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def options(self):
        return self._additional_options

    @listens(u'parameters')
    def __on_parameters_changed(self):
        edit_mode_parameter = get_parameter_by_name(self, u'Edit Mode')
        self.left_right_curve_switch_option.set_parameter(edit_mode_parameter)
        self.mid_side_curve_switch_option.set_parameter(edit_mode_parameter)


class _CompressorDeviceDecorator(LiveObjectDecorator, EventObject):
    _input_router = None
    _type_list = None
    _channel_list = None
    _position_list = None

    def __init__(self, song = None, *a, **k):
        super(_CompressorDeviceDecorator, self).__init__(*a, **k)
        for event, func in ((u'input_routing_type', self.notify_input_routing_type_index), (u'input_routing_channel', self.notify_input_routing_channel_index)):
            self.register_slot(event_name=event, subject=self._live_object, listener=func)

        make_option = lambda option_name, parameter_name: DeviceOnOffOption(name=option_name, property_host=get_parameter_by_name(self, parameter_name), property_name=u'value')
        self._options = tuple([ self.register_disconnectable(make_option(option_name, param_name)) for option_name, param_name in ((u'Auto Release', u'Auto Release On/Off'),
         (u'Makeup', u'Makeup'),
         (u'Listen', u'S/C Listen'),
         (u'Sidechain', u'S/C On')) ])
        make_parameter = lambda name, values, index: EnumWrappingParameter(name=name, parent=self, values_host=self, index_property_host=self, values_property=values, index_property=index)
        self._position_parameter = make_parameter(u'Position', u'input_channel_positions', u'input_channel_position_index')
        self._additional_parameters = self.register_disconnectables((make_parameter(u'Input Type', u'available_input_routing_types', u'input_routing_type_index'), make_parameter(u'Input Channel', u'available_input_routing_channels', u'input_routing_channel_index'), self._position_parameter))

    def set_routing_infrastructure(self, input_router, type_list, channel_list, position_list):
        self._input_router = input_router
        self._type_list = type_list
        self._channel_list = channel_list
        self._position_list = position_list
        self.__on_has_positions_changed.subject = self._input_router
        self.notify_input_routing_type_index()
        self.notify_input_routing_channel_index()
        self.notify_input_channel_position_index()

    def __setattr__(self, attribute, value):
        selector = dict(input_routing_type_index=self._set_input_routing_type_index, input_routing_channel_index=self._set_input_routing_channel_index, input_channel_position_index=self._set_input_channel_position_index).get(attribute, lambda v: super(_CompressorDeviceDecorator, self).__setattr__(attribute, v))
        selector(value)

    @property
    def available_input_routing_types(self):
        return tuple([ t.name for t in self._type_list.targets ])

    @listenable_property
    def input_routing_type_index(self):
        return self._type_list.selected_index

    def _set_input_routing_type_index(self, index):
        self._type_list.selected_target = self._type_list.targets[index]

    @listenable_property
    def input_routing_channel_index(self):
        return self._channel_list.selected_index

    def _set_input_routing_channel_index(self, index):
        self._channel_list.selected_target = self._channel_list.targets[index]

    @property
    def available_input_routing_channels(self):
        return tuple([ t.name for t in self._channel_list.targets ] or [u''])

    @listens(u'has_input_channel_position')
    def __on_has_positions_changed(self, has_positions):
        self._position_parameter.is_enabled = has_positions
        self.notify_input_channel_position_index()
        self.notify_input_channel_positions()

    @listenable_property
    def input_channel_position_index(self):
        if self._input_router.has_input_channel_position:
            return self._input_router.input_channel_position_index
        return 0

    def _set_input_channel_position_index(self, index):
        if self._input_router.has_input_channel_position:
            self._input_router.input_channel_position_index = index

    @listenable_property
    def input_channel_positions(self):
        return tuple(self._input_router.input_channel_positions if self._input_router.has_input_channel_position else [u''])

    @property
    def options(self):
        return self._options

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def routing_type_list(self):
        return self._type_list

    @property
    def routing_channel_list(self):
        return self._channel_list

    @property
    def routing_channel_position_list(self):
        return self._position_list


class _PedalDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, song = None, *a, **k):
        super(_PedalDeviceDecorator, self).__init__(*a, **k)
        self.__on_parameters_changed.subject = self._live_object
        self.mid_freq_option = DeviceSwitchOption(name=u'Mid Freq', parameter=get_parameter_by_name(self, u'Mid Freq'))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.mid_freq_option,)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.mid_freq_option.set_parameter(get_parameter_by_name(self, u'Mid Freq'))


class _DrumBussDeviceDecorator(LiveObjectDecorator):

    def __init__(self, song = None, *a, **k):
        super(_DrumBussDeviceDecorator, self).__init__(*a, **k)
        self.compressor_option = DeviceOnOffOption(name=u'Compressor', property_host=get_parameter_by_name(self, u'Compressor On'), property_name=u'value')
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.compressor_option,)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.compressor_option.set_parameter(get_parameter_by_name(self, u'Compressor On'))


class _EchoDeviceDecorator(LiveObjectDecorator):

    def __init__(self, song = None, *a, **k):
        super(_EchoDeviceDecorator, self).__init__(*a, **k)
        self.syncL_option = DeviceOnOffOption(name=u'L Sync', property_host=get_parameter_by_name(self, u'L Sync'), property_name=u'value')
        self.syncR_option = DeviceOnOffOption(name=u'R Sync', property_host=get_parameter_by_name(self, u'R Sync'), property_name=u'value')
        self.clipdry_option = DeviceOnOffOption(name=u'Clip Dry', property_host=get_parameter_by_name(self, u'Clip Dry'), property_name=u'value')
        self.feedbackinv_option = DeviceOnOffOption(name=u'Invert', property_host=get_parameter_by_name(self, u'Feedback Inv'), property_name=u'value')
        self.reverb_loc_option = DeviceSwitchOption(name=u'Reverb Loc', parameter=get_parameter_by_name(self, u'Reverb Loc'))
        self.duck_option = DeviceOnOffOption(name=u'Duck', property_host=get_parameter_by_name(self, u'Duck On'), property_name=u'value')
        self.gate_option = DeviceOnOffOption(name=u'Gate', property_host=get_parameter_by_name(self, u'Gate On'), property_name=u'value')
        self.wobble_option = DeviceOnOffOption(name=u'Wobble', property_host=get_parameter_by_name(self, u'Wobble On'), property_name=u'value')
        self.noise_option = DeviceOnOffOption(name=u'Noise', property_host=get_parameter_by_name(self, u'Noise On'), property_name=u'value')
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.syncL_option,
         self.syncR_option,
         self.clipdry_option,
         self.feedbackinv_option,
         self.reverb_loc_option,
         self.duck_option,
         self.gate_option,
         self.wobble_option,
         self.noise_option)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.syncL_option.set_parameter(get_parameter_by_name(self, u'L Sync'))
        self.syncR_option.set_parameter(get_parameter_by_name(self, u'R Sync'))
        self.clipdry_option.set_parameter(get_parameter_by_name(self, u'Clip Dry'))
        self.feedbackinv_option.set_parameter(get_parameter_by_name(self, u'Feedback Inv'))
        self.reverb_loc_option.set_parameter(get_parameter_by_name(self, u'Reverb Loc'))
        self.duck_option.set_parameter(get_parameter_by_name(self, u'Duck On'))
        self.gate_option.set_parameter(get_parameter_by_name(self, u'Gate On'))
        self.wobble_option.set_parameter(get_parameter_by_name(self, u'Wobble On'))
        self.noise_option.set_parameter(get_parameter_by_name(self, u'Noise On'))


class DeviceDecoratorFactory(DecoratorFactory):
    DECORATOR_CLASSES = {u'OriginalSimpler': _SimplerDeviceDecorator,
     u'Operator': _OperatorDeviceDecorator,
     u'MultiSampler': _SamplerDeviceDecorator,
     u'AutoFilter': _AutoFilterDeviceDecorator,
     u'Eq8': _Eq8DeviceDecorator,
     u'Compressor2': _CompressorDeviceDecorator,
     u'Pedal': _PedalDeviceDecorator,
     u'DrumBuss': _DrumBussDeviceDecorator,
     u'Echo': _EchoDeviceDecorator}

    @classmethod
    def generate_decorated_device(cls, device, additional_properties = {}, song = None, *a, **k):
        decorated = cls.DECORATOR_CLASSES[device.class_name](live_object=device, additional_properties=additional_properties, song=song, *a, **k)
        return decorated

    @classmethod
    def _should_be_decorated(cls, device):
        return liveobj_valid(device) and device.class_name in cls.DECORATOR_CLASSES

    @depends(song=None)
    def _get_decorated_object(self, device, additional_properties, song = None, *a, **k):
        return self.generate_decorated_device(device, additional_properties=additional_properties, song=song, *a, **k)


class SimplerDecoratedPropertiesCopier(object):
    ADDITIONAL_PROPERTIES = [u'playhead_real_time_channel_id', u'waveform_real_time_channel_id']

    def __init__(self, decorated_object = None, factory = None, *a, **k):
        raise liveobj_valid(decorated_object) or AssertionError
        raise factory is not None or AssertionError
        raise decorated_object in factory.decorated_objects or AssertionError
        super(SimplerDecoratedPropertiesCopier, self).__init__(*a, **k)
        self._decorated_object = decorated_object
        self._factory = factory
        self._copied_additional_properties = {}
        self._nested_properties = {}
        self.copy_properties({self.ADDITIONAL_PROPERTIES[0]: None,
         self.ADDITIONAL_PROPERTIES[1]: None})

    def copy_properties(self, properties):
        for prop, getter in properties.iteritems():
            if getter:
                self._nested_properties[prop] = getter(self._decorated_object)
            else:
                self._copied_additional_properties[prop] = getattr(self._decorated_object, prop)

    def apply_properties(self, new_object, song):
        decorated = self._factory.decorate(new_object, additional_properties=self._copied_additional_properties, song=song)
        self._apply_nested_properties(decorated)
        return decorated

    def _apply_nested_properties(self, decorated_object):
        if decorated_object.zoom.waveform_navigation is not None and self._decorated_object.zoom.waveform_navigation is not None:
            decorated_object.zoom.waveform_navigation.copy_state(self._decorated_object.zoom.waveform_navigation)