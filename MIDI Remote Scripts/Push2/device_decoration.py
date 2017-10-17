
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
import re
from ableton.v2.base import EventObject, clamp, depends, find_if, listenable_property, listens, liveobj_valid
from pushbase.decoration import LiveObjectDecorator, DecoratorFactory
from pushbase.internal_parameter import EnumWrappingParameter, IntegerParameter, InternalParameter, InternalParameterBase
from pushbase.message_box_component import Messenger
from pushbase.simpler_decoration import BoolWrappingParameter, SimplerDeviceDecorator as SimplerDeviceDecoratorBase
from .device_options import DeviceTriggerOption, DeviceSwitchOption, DeviceOnOffOption
from .timeline_navigation import Region, SimplerWaveformNavigation
import Live
ModulationSource = Live.InstrumentWavetableDevice.ModulationSource
ParameterState = Live.DeviceParameter.ParameterState
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

class InstrumentVectorOscillatorType(int):
    pass


InstrumentVectorOscillatorType.one = InstrumentVectorOscillatorType(0)
InstrumentVectorOscillatorType.two = InstrumentVectorOscillatorType(1)
InstrumentVectorOscillatorType.s = InstrumentVectorOscillatorType(2)
InstrumentVectorOscillatorType.mix = InstrumentVectorOscillatorType(3)

class InstrumentVectorFilterType(int):
    pass


InstrumentVectorFilterType.one = InstrumentVectorFilterType(0)
InstrumentVectorFilterType.two = InstrumentVectorFilterType(1)

class InstrumentVectorEnvelopeType(int):
    pass


InstrumentVectorEnvelopeType.amp = InstrumentVectorEnvelopeType(0)
InstrumentVectorEnvelopeType.env2 = InstrumentVectorEnvelopeType(1)
InstrumentVectorEnvelopeType.env3 = InstrumentVectorEnvelopeType(2)

class InstrumentVectorLfoType(int):
    pass


InstrumentVectorLfoType.one = InstrumentVectorLfoType(0)
InstrumentVectorLfoType.two = InstrumentVectorLfoType(1)

class InstrumentVectorEnvelopeViewType(int):
    pass


InstrumentVectorEnvelopeViewType.time = InstrumentVectorEnvelopeViewType(0)
InstrumentVectorEnvelopeViewType.slope = InstrumentVectorEnvelopeViewType(1)
InstrumentVectorEnvelopeViewType.value = InstrumentVectorEnvelopeViewType(2)

class EnvelopeFeature(int):
    pass


EnvelopeFeature.time = EnvelopeFeature(0)
EnvelopeFeature.level = EnvelopeFeature(1)

class SlopedEnvelopeFeature(int):
    pass


SlopedEnvelopeFeature.time = SlopedEnvelopeFeature(0)
SlopedEnvelopeFeature.slope = SlopedEnvelopeFeature(1)
SlopedEnvelopeFeature.level = SlopedEnvelopeFeature(2)

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


class IndexProvider(EventObject):
    __events__ = (u'index',)

    def __init__(self, *a, **k):
        super(IndexProvider, self).__init__(*a, **k)
        self._index = 0

    def _get_index(self):
        return self._index

    def _set_index(self, value):
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


class EnvelopeFeatureList(NotifyingList):

    def __init__(self):
        super(EnvelopeFeatureList, self).__init__(available_values=[u'Time', u'Level'], default_value=EnvelopeFeature.time)


class SlopedEnvelopeFeatureList(NotifyingList):

    def __init__(self):
        super(SlopedEnvelopeFeatureList, self).__init__(available_values=[u'Time', u'Slope', u'Level'], default_value=SlopedEnvelopeFeature.time)


class InstrumentVectorOscillatorTypesList(NotifyingList):

    def __init__(self):
        super(InstrumentVectorOscillatorTypesList, self).__init__(available_values=[u'1',
         u'2',
         u'S',
         u'Mix'], default_value=InstrumentVectorOscillatorType.one)


class InstrumentVectorFilterTypesList(NotifyingList):

    def __init__(self):
        super(InstrumentVectorFilterTypesList, self).__init__(available_values=[u'1', u'2'], default_value=InstrumentVectorFilterType.one)


class InstrumentVectorEnvelopeTypesList(NotifyingList):

    def __init__(self):
        super(InstrumentVectorEnvelopeTypesList, self).__init__(available_values=[u'AMP', u'ENV2', u'ENV3'], default_value=InstrumentVectorEnvelopeType.amp)


class InstrumentVectorLfoTypesList(NotifyingList):

    def __init__(self):
        super(InstrumentVectorLfoTypesList, self).__init__(available_values=[u'LFO1', u'LFO2'], default_value=InstrumentVectorLfoType.one)


class InstrumentVectorAmpEnvelopeViewTypesList(NotifyingList):

    def __init__(self):
        super(InstrumentVectorAmpEnvelopeViewTypesList, self).__init__(available_values=[u'Time', u'Slope'], default_value=InstrumentVectorEnvelopeViewType.time)


class InstrumentVectorModEnvelopeViewTypesList(NotifyingList):

    def __init__(self):
        super(InstrumentVectorModEnvelopeViewTypesList, self).__init__(available_values=[u'Time', u'Slope', u'Value'], default_value=InstrumentVectorEnvelopeViewType.time)


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
        self.__on_envelope_type_changed.subject = self.envelope

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
        self.retrigger_option = DeviceOnOffOption(name=u'Retrigger', property_host=self._live_object, value_property_name=u'retrigger')
        self.warp_as_x_bars_option = DeviceTriggerOption(name=u'Warp as X Bars', default_label=self.get_warp_as_option_label(), callback=lambda : call_simpler_function(u'warp_as', call_simpler_function(u'guess_playback_length')), is_active=lambda : get_simpler_flag(u'can_warp_as'))
        self.warp_half_option = DeviceTriggerOption(name=u':2', callback=partial(call_simpler_function, u'warp_half'), is_active=lambda : get_simpler_flag(u'can_warp_half'))
        self.warp_double_option = DeviceTriggerOption(name=u'x2', callback=partial(call_simpler_function, u'warp_double'), is_active=lambda : get_simpler_flag(u'can_warp_double'))
        self.lfo_sync_option = DeviceSwitchOption(name=u'LFO Sync Type', parameter=get_parameter_by_name(self, u'L Sync'))
        self.loop_option = DeviceOnOffOption(name=u'Loop', property_host=get_parameter_by_name(self, u'S Loop On'))
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

    @listenable_property
    def envelope_type_index(self):
        return self._envelope_types_provider.index

    @listens(u'value')
    def __on_envelope_type_changed(self):
        self.notify_envelope_type_index()


class _OperatorDeviceDecorator(EventObject, LiveObjectDecorator):

    def __init__(self, song = None, osc_types_provider = None, env_feature_provider = None, sloped_env_feature_provider = None, *a, **k):
        super(_OperatorDeviceDecorator, self).__init__(*a, **k)
        self._osc_types_provider = osc_types_provider if osc_types_provider is not None else OscillatorTypesList()
        self._env_feature_provider = env_feature_provider if env_feature_provider is not None else EnvelopeFeatureList()
        self._sloped_env_feature_provider = sloped_env_feature_provider if sloped_env_feature_provider is not None else SlopedEnvelopeFeatureList()
        self.__on_parameters_changed.subject = self._live_object
        self.oscillator = EnumWrappingParameter(name=u'Oscillator', parent=self, values_host=self._osc_types_provider, index_property_host=self._osc_types_provider, values_property=u'available_values', index_property=u'index', value_type=OscillatorType)
        self.env_feature = EnumWrappingParameter(name=u'Envelope Feature Time/Level', parent=self, values_host=self._env_feature_provider, index_property_host=self._env_feature_provider, values_property=u'available_values', index_property=u'index', value_type=EnvelopeFeature)
        self.sloped_env_feature = EnumWrappingParameter(name=u'Envelope Feature Time/Slope/Level', parent=self, values_host=self._sloped_env_feature_provider, index_property_host=self._sloped_env_feature_provider, values_property=u'available_values', index_property=u'index', value_type=SlopedEnvelopeFeature)
        self.__on_oscillator_switch_value_changed.subject = self.oscillator
        self.filter_slope_option = DeviceSwitchOption(name=u'Filter Slope', parameter=get_parameter_by_name(self, u'Filter Slope'))
        self.register_disconnectables(self.options)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + (self.oscillator, self.env_feature, self.sloped_env_feature)

    @property
    def options(self):
        return (self.filter_slope_option,)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.filter_slope_option.set_parameter(get_parameter_by_name(self, u'Filter Slope'))

    @listenable_property
    def oscillator_index(self):
        return self._osc_types_provider.index

    @listens(u'value')
    def __on_oscillator_switch_value_changed(self):
        self.notify_oscillator_index()


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

        make_option = lambda option_name, parameter_name: DeviceOnOffOption(name=option_name, property_host=get_parameter_by_name(self, parameter_name))
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


class _PedalDeviceDecorator(LiveObjectDecorator):

    def __init__(self, song = None, *a, **k):
        super(_PedalDeviceDecorator, self).__init__(*a, **k)
        self.mid_freq_option = DeviceSwitchOption(name=u'Mid Freq', parameter=get_parameter_by_name(self, u'Mid Freq'))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.mid_freq_option,)


class _DrumBussDeviceDecorator(LiveObjectDecorator):

    def __init__(self, song = None, *a, **k):
        super(_DrumBussDeviceDecorator, self).__init__(*a, **k)
        self.compressor_option = DeviceOnOffOption(name=u'Compressor', property_host=get_parameter_by_name(self, u'Compressor On'))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.compressor_option,)


class _EchoDeviceDecorator(LiveObjectDecorator, EventObject):

    class EchoChannelName(int):
        pass

    EchoChannelName.left = EchoChannelName(0)
    EchoChannelName.right = EchoChannelName(1)

    class EchoChannelNamesList(NotifyingList):

        def __init__(self):
            super(_EchoDeviceDecorator.EchoChannelNamesList, self).__init__(available_values=[u'Left', u'Right'], default_value=_EchoDeviceDecorator.EchoChannelName.left)

    def __init__(self, song = None, *a, **k):
        super(_EchoDeviceDecorator, self).__init__(*a, **k)
        self._channel_names_provider = _EchoDeviceDecorator.EchoChannelNamesList()
        self.channel_switch_parameter = EnumWrappingParameter(name=u'Channel Toggle', parent=self, values_host=self._channel_names_provider, index_property_host=self._channel_names_provider, values_property=u'available_values', index_property=u'index', value_type=_EchoDeviceDecorator.EchoChannelName)
        self._additional_parameters = (self.channel_switch_parameter,)
        self.link_option = DeviceOnOffOption(name=u'Link', property_host=get_parameter_by_name(self, u'Link'))
        self.sync_l_option = DeviceOnOffOption(name=u'L Sync', property_host=get_parameter_by_name(self, u'L Sync'))
        self.sync_r_option = DeviceOnOffOption(name=u'R Sync', property_host=get_parameter_by_name(self, u'R Sync'))
        self.sync_m_option = DeviceOnOffOption(name=u'M Sync', property_host=get_parameter_by_name(self, u'L Sync'))
        self.sync_s_option = DeviceOnOffOption(name=u'S Sync', property_host=get_parameter_by_name(self, u'R Sync'))
        self.clip_dry_option = DeviceOnOffOption(name=u'Clip Dry', property_host=get_parameter_by_name(self, u'Clip Dry'))
        self.filter_on_option = DeviceOnOffOption(name=u'Filter', property_host=get_parameter_by_name(self, u'Filter On'))
        self.feedback_inv_option = DeviceOnOffOption(name=u'Invert', property_host=get_parameter_by_name(self, u'Feedback Inv'))
        self.modulation_times_four_option = DeviceOnOffOption(name=u'Mod 4x', property_host=get_parameter_by_name(self, u'Mod 4x'))
        self.reverb_loc_option = DeviceSwitchOption(name=u'Reverb Loc', parameter=get_parameter_by_name(self, u'Reverb Loc'))
        self.duck_option = DeviceOnOffOption(name=u'Duck', property_host=get_parameter_by_name(self, u'Duck On'))
        self.gate_option = DeviceOnOffOption(name=u'Gate', property_host=get_parameter_by_name(self, u'Gate On'))
        self.wobble_option = DeviceOnOffOption(name=u'Wobble', property_host=get_parameter_by_name(self, u'Wobble On'))
        self.noise_option = DeviceOnOffOption(name=u'Noise', property_host=get_parameter_by_name(self, u'Noise On'))
        self.channel_switch_lr_option = DeviceSwitchOption(name=u'L/R Switch', parameter=self.channel_switch_parameter, labels=[u'Left', u'Right'])
        self.channel_switch_ms_option = DeviceSwitchOption(name=u'M/S Switch', parameter=self.channel_switch_parameter, labels=[u'Mid', u'Side'])
        self.register_disconnectables(self._additional_parameters)
        self.register_disconnectables(self.options)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def options(self):
        return (self.channel_switch_lr_option,
         self.channel_switch_ms_option,
         self.link_option,
         self.sync_l_option,
         self.sync_r_option,
         self.sync_m_option,
         self.sync_s_option,
         self.clip_dry_option,
         self.filter_on_option,
         self.feedback_inv_option,
         self.modulation_times_four_option,
         self.reverb_loc_option,
         self.duck_option,
         self.gate_option,
         self.wobble_option,
         self.noise_option)


class PitchParameter(InternalParameter):

    def __init__(self, integer_value_host = None, decimal_value_host = None, *a, **k):
        super(PitchParameter, self).__init__(*a, **k)
        self._integer_value_host = integer_value_host
        self._decimal_value_host = decimal_value_host
        self._on_integer_value_changed.subject = integer_value_host
        self._on_decimal_value_changed.subject = decimal_value_host
        self._integer_value = getattr(integer_value_host, u'value', 0)
        self._decimal_value = getattr(decimal_value_host, u'value', 0.0)
        self.adjust_finegrain = False

    @listens(u'value')
    def _on_integer_value_changed(self):
        new_integer_value = self._integer_value_host.value
        if self._integer_value != new_integer_value:
            self._integer_value = new_integer_value
            self.notify_value()

    @listens(u'value')
    def _on_decimal_value_changed(self):
        new_decimal_value = self._decimal_value_host.value
        if self._decimal_value != new_decimal_value:
            self._decimal_value = new_decimal_value
            self.notify_value()

    @property
    def _combined_value(self):
        return getattr(self._integer_value_host, u'value', 0) + (getattr(self._decimal_value_host, u'value', 0.0) - 0.5)

    @property
    def value(self):
        return self._combined_value

    def _get_linear_value(self):
        if self.adjust_finegrain:
            return self._decimal_value
        return self._integer_value

    def _set_linear_value(self, new_value):
        if self.adjust_finegrain:
            if self._decimal_value != new_value:
                self._set_finegrain(new_value)
                self.notify_value()
        elif self._integer_value != new_value:
            self._set_coarse(new_value)
            self.notify_value()

    linear_value = listenable_property(_get_linear_value, _set_linear_value)

    def _set_coarse(self, new_value):
        self._integer_value = new_value
        if liveobj_valid(self._integer_value_host):
            self._integer_value_host.value = clamp(new_value, self._integer_value_host.min, self._integer_value_host.max)

    def _set_finegrain(self, new_value):
        if new_value < 0 or new_value > 1:
            offset = 1 if new_value < 0 else -1
            new_value += offset
            self._set_coarse(getattr(self._integer_value_host, u'value', 0) - offset)
        self._decimal_value = new_value
        if liveobj_valid(self._decimal_value_host):
            self._decimal_value_host.value = new_value

    @property
    def decimal_value_host(self):
        return self._decimal_value_host

    @property
    def min(self):
        return getattr(self._integer_value_host, u'min', 0) - getattr(self._decimal_value_host, u'min', 0.0)

    @property
    def max(self):
        return getattr(self._integer_value_host, u'max', 1) + getattr(self._decimal_value_host, u'max', 1.0)

    @property
    def display_value(self):
        return u'{0:.2f}st'.format(self._combined_value)


class ModMatrixParameter(InternalParameter):
    u""" Observe the modulation value for a given source index
    
        This object has a static source index and a dynamic target
        index, i.e. the user can change which modulation target is
        being observed. This object also has a modulation value host
        that it uses to update the _modulation_value whenever the
        _modulation_value_host indicates the modulation_matrix_changed
    """

    def __init__(self, modulation_value_host = None, modulation_target_index_host = None, modulation_source = None, *a, **k):
        super(ModMatrixParameter, self).__init__(*a, **k)
        self._modulation_value_host = modulation_value_host
        self._target_index_host = modulation_target_index_host
        self._source = modulation_source
        self._on_target_index_changed.subject = modulation_target_index_host
        self._on_modulation_matrix_changed.subject = modulation_value_host
        self._modulation_value = 0.0
        self._update_value()

    def _target_index(self):
        return self._target_index_host.index

    def _update_value(self, force_update = False):
        old_value = self._modulation_value
        self._modulation_value = self._modulation_value_host.get_modulation_value(self._target_index(), self._source)
        if old_value != self._modulation_value or force_update:
            self.notify_value()

    @listens(u'index')
    def _on_target_index_changed(self):
        self._update_value(force_update=True)

    @listens(u'modulation_matrix_changed')
    def _on_modulation_matrix_changed(self):
        self._update_value()

    def _get_linear_value(self):
        return self._modulation_value

    def _set_linear_value(self, new_value):
        if new_value != self._modulation_value:
            self._modulation_value_host.set_modulation_value(self._target_index(), self._source, new_value)

    linear_value = property(_get_linear_value, _set_linear_value)

    @property
    def min(self):
        return -1.0

    @property
    def max(self):
        return 1.0

    @property
    def display_value(self):
        percentage = 100.0 * self._modulation_value
        precision = 1 if abs(percentage) < 10.0 else 0
        format_str = u'%.' + str(precision) + u'f'
        return unicode(format_str % percentage)


class _InstrumentVectorDeviceDecorator(LiveObjectDecorator, EventObject):
    MIN_UNISON_VOICE_COUNT = 2
    MAX_UNISON_VOICE_COUNT = 8
    available_effect_modes = (u'None',
     u'Fm',
     u'Classic',
     u'Modern')
    available_filter_curcuit_lp_hp_values = (u'Clean',
     u'OSR',
     u'MS2',
     u'SMP',
     u'PRD')
    available_filter_curcuit_bp_no_morph_values = (u'Clean', u'OSR')
    available_unison_modes = (u'None',
     u'Classic',
     u'Shimmer',
     u'Noise',
     u'Phase Sync',
     u'Position Spread',
     u'Random Note')
    mono_off_on_values = (u'Off', u'On')
    available_filter_routings = (u'Serial', u'Parallel', u'Split')
    __events__ = (u'request_bank_view', u'request_previous_bank_from_mod_matrix')

    def __init__(self, song = None, osc_types_provider = None, filter_types_provider = None, internal_filter_types_provider = None, envelope_types_provider = None, lfo_types_provider = None, amp_envelope_view_types_provider = None, mod_envelope_view_types_provider = None, *a, **k):
        super(_InstrumentVectorDeviceDecorator, self).__init__(*a, **k)
        self._osc_types_provider = osc_types_provider if osc_types_provider is not None else InstrumentVectorOscillatorTypesList()
        self._filter_types_provider = filter_types_provider if filter_types_provider is not None else InstrumentVectorFilterTypesList()
        self._internal_filter_types_provider = internal_filter_types_provider if internal_filter_types_provider is not None else InstrumentVectorFilterTypesList()
        self._envelope_types_provider = envelope_types_provider if envelope_types_provider is not None else InstrumentVectorEnvelopeTypesList()
        self._lfo_types_provider = lfo_types_provider if lfo_types_provider is not None else InstrumentVectorLfoTypesList()
        self._amp_envelope_view_types_provider = amp_envelope_view_types_provider if amp_envelope_view_types_provider is not None else InstrumentVectorAmpEnvelopeViewTypesList()
        self._mod_envelope_view_types_provider = mod_envelope_view_types_provider if mod_envelope_view_types_provider is not None else InstrumentVectorModEnvelopeViewTypesList()
        self.current_mod_target_index = IndexProvider()
        self._single_selected_parameter = None
        self._additional_parameters = self._create_parameters()
        self._options = self._create_options()
        self.register_disconnectables(self._additional_parameters)
        self.register_disconnectables(self._options)
        self.__on_oscillator_switch_value_changed.subject = self.oscillator_switch
        self.__on_internal_filter_switch_value_changed.subject = self.filter_switch_for_filter_switch_option
        self.__on_current_mod_target_index_changed.subject = self.current_mod_target_index
        self.__on_lfo_types_provider_index_changed.subject = self._lfo_types_provider
        self._osc_1_on_parameter = get_parameter_by_name(self, u'Osc 1 On')
        self._osc_2_on_parameter = get_parameter_by_name(self, u'Osc 2 On')
        self.__on_osc_1_on_value_changed.subject = self._osc_1_on_parameter
        self.__on_osc_1_on_value_changed()
        self.__on_osc_2_on_value_changed.subject = self._osc_2_on_parameter
        self.__on_osc_2_on_value_changed()
        self._filter_1_on_parameter = get_parameter_by_name(self, u'Filter 1 On')
        self._filter_2_on_parameter = get_parameter_by_name(self, u'Filter 2 On')
        self.__on_filter_1_on_value_changed.subject = self._filter_1_on_parameter
        self.__on_filter_1_on_value_changed()
        self.__on_filter_2_on_value_changed.subject = self._filter_2_on_parameter
        self.__on_filter_2_on_value_changed()

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def options(self):
        return self._options

    @listenable_property
    def oscillator_index(self):
        return self._osc_types_provider.index

    @listenable_property
    def filter_index(self):
        return self._internal_filter_types_provider.index

    @property
    def single_selected_parameter(self):
        return self._single_selected_parameter

    def set_single_selected_parameter(self, value):
        self._single_selected_parameter = value
        self.add_to_mod_matrix_option.notify_active()

    @listenable_property
    def current_mod_target_parameter(self):
        return self._get_current_mod_target_parameter()

    def _create_parameters(self):
        self.oscillator_switch = EnumWrappingParameter(name=u'Oscillator', parent=self, values_host=self._osc_types_provider, index_property_host=self._osc_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorOscillatorType)
        self.osc_1_pitch = PitchParameter(name=u'Osc 1 Pitch', parent=self, integer_value_host=get_parameter_by_name(self, u'Osc 1 Transp'), decimal_value_host=get_parameter_by_name(self, u'Osc 1 Detune'))
        self.osc_2_pitch = PitchParameter(name=u'Osc 2 Pitch', parent=self, integer_value_host=get_parameter_by_name(self, u'Osc 2 Transp'), decimal_value_host=get_parameter_by_name(self, u'Osc 2 Detune'))
        self.filter_switch_for_filter_switch_option = EnumWrappingParameter(name=u'Internal Filter', parent=self, values_host=self._internal_filter_types_provider, index_property_host=self._internal_filter_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorFilterType)
        self.current_mod_target = InternalParameter(name=u'Current Mod Target', parent=self)
        self.envelope_switch = EnumWrappingParameter(name=u'Envelopes', parent=self, values_host=self._envelope_types_provider, index_property_host=self._envelope_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorEnvelopeType)
        self.lfo_switch = EnumWrappingParameter(name=u'LFOs', parent=self, values_host=self._lfo_types_provider, index_property_host=self._lfo_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorLfoType)
        self._osc_1_category_switch = EnumWrappingParameter(name=u'Osc 1 Category', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_wavetable_categories', index_property=u'oscillator_1_wavetable_category')
        self._osc_2_category_switch = EnumWrappingParameter(name=u'Osc 2 Category', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_wavetable_categories', index_property=u'oscillator_2_wavetable_category')
        self._osc_1_table_switch = EnumWrappingParameter(name=u'Osc 1 Table', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_1_wavetables', index_property=u'oscillator_1_wavetable_index')
        self._osc_2_table_switch = EnumWrappingParameter(name=u'Osc 2 Table', parent=self, values_host=self._live_object, index_property_host=self, values_property=u'oscillator_2_wavetables', index_property=u'oscillator_2_wavetable_index')
        self._osc_1_effect_type_switch = EnumWrappingParameter(name=u'Osc 1 Effect Type', parent=self, values_host=self, index_property_host=self, values_property=u'available_effect_modes', index_property=u'oscillator_1_effect_mode')
        self._osc_2_effect_type_switch = EnumWrappingParameter(name=u'Osc 2 Effect Type', parent=self, values_host=self, index_property_host=self, values_property=u'available_effect_modes', index_property=u'oscillator_2_effect_mode')
        self._filter_1_circuit_lp_hp_switch = EnumWrappingParameter(name=u'Filter 1 Circuit LP/HP', parent=self, values_host=self, index_property_host=get_parameter_by_name(self, u'Filter 1 LP/HP'), values_property=u'available_filter_curcuit_lp_hp_values', index_property=u'value')
        self._filter_2_circuit_lp_hp_switch = EnumWrappingParameter(name=u'Filter 2 Circuit LP/HP', parent=self, values_host=self, index_property_host=get_parameter_by_name(self, u'Filter 2 LP/HP'), values_property=u'available_filter_curcuit_lp_hp_values', index_property=u'value')
        self._filter_1_circuit_bp_no_morph_switch = EnumWrappingParameter(name=u'Filter 1 Circuit BP/NO/Morph', parent=self, values_host=self, index_property_host=get_parameter_by_name(self, u'Filter 1 BP/NO/Morph'), values_property=u'available_filter_curcuit_bp_no_morph_values', index_property=u'value')
        self._filter_2_circuit_bp_no_morph_switch = EnumWrappingParameter(name=u'Filter 2 Circuit BP/NO/Morph', parent=self, values_host=self, index_property_host=get_parameter_by_name(self, u'Filter 2 BP/NO/Morph'), values_property=u'available_filter_curcuit_bp_no_morph_values', index_property=u'value')
        return (EnumWrappingParameter(name=u'Filter', parent=self, values_host=self._filter_types_provider, index_property_host=self._filter_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorFilterType),
         EnumWrappingParameter(name=u'Amp Env View', parent=self, values_host=self._amp_envelope_view_types_provider, index_property_host=self._amp_envelope_view_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorEnvelopeViewType),
         EnumWrappingParameter(name=u'Mod Env View', parent=self, values_host=self._mod_envelope_view_types_provider, index_property_host=self._mod_envelope_view_types_provider, values_property=u'available_values', index_property=u'index', value_type=InstrumentVectorEnvelopeViewType),
         EnumWrappingParameter(name=u'Modulation Target Names', parent=self, values_host=self._live_object, index_property_host=self.current_mod_target_index, values_property=u'visible_modulation_target_names', index_property=u'index'),
         ModMatrixParameter(name=u'Amp Env Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.amp_envelope),
         ModMatrixParameter(name=u'Env 2 Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.envelope_2),
         ModMatrixParameter(name=u'Env 3 Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.envelope_3),
         ModMatrixParameter(name=u'Lfo 1 Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.lfo_1),
         ModMatrixParameter(name=u'Lfo 2 Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.lfo_2),
         ModMatrixParameter(name=u'MIDI Velocity Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_velocity),
         ModMatrixParameter(name=u'MIDI Note Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_note),
         ModMatrixParameter(name=u'MIDI Pitch Bend Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_pitch_bend),
         ModMatrixParameter(name=u'MIDI Aftertouch Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_channel_pressure),
         ModMatrixParameter(name=u'MIDI Mod Wheel Mod Amount', parent=self, modulation_value_host=self._live_object, modulation_target_index_host=self.current_mod_target_index, modulation_source=ModulationSource.midi_mod_wheel),
         EnumWrappingParameter(name=u'Unison Mode', parent=self, values_host=self, index_property_host=self, values_property=u'available_unison_modes', index_property=u'unison_mode'),
         IntegerParameter(name=u'Unison Voices', parent=self, integer_value_host=self._live_object, integer_value_property_name=u'unison_voice_count', min_value=self.MIN_UNISON_VOICE_COUNT, max_value=self.MAX_UNISON_VOICE_COUNT),
         EnumWrappingParameter(name=u'Mono On', parent=self, values_host=self, index_property_host=self, values_property=u'mono_off_on_values', index_property=u'mono_poly', to_index_conversion=lambda index: int(not index), from_index_conversion=lambda index: int(not index)),
         EnumWrappingParameter(name=u'Filter Routing', parent=self, values_host=self, index_property_host=self, values_property=u'available_filter_routings', index_property=u'filter_routing')) + (self.oscillator_switch,
         self.osc_1_pitch,
         self.osc_2_pitch,
         self.filter_switch_for_filter_switch_option,
         self.current_mod_target,
         self.envelope_switch,
         self.lfo_switch,
         self._osc_1_category_switch,
         self._osc_2_category_switch,
         self._osc_1_table_switch,
         self._osc_2_table_switch,
         self._osc_1_effect_type_switch,
         self._osc_2_effect_type_switch,
         self._filter_1_circuit_lp_hp_switch,
         self._filter_2_circuit_lp_hp_switch,
         self._filter_1_circuit_bp_no_morph_switch,
         self._filter_2_circuit_bp_no_morph_switch)

    def _create_options(self):

        def is_selected_parameter_modulatable():
            if self.single_selected_parameter is None:
                return False
            if isinstance(self.single_selected_parameter, PitchParameter):
                return True
            if isinstance(self.single_selected_parameter, InternalParameterBase):
                return False
            return self._live_object.is_parameter_modulatable(self.single_selected_parameter)

        def add_selected_parameter_to_mod_matrix():
            if is_selected_parameter_modulatable():
                param = self.single_selected_parameter.decimal_value_host if isinstance(self.single_selected_parameter, PitchParameter) else self.single_selected_parameter
                self.current_mod_target_index.index = self._live_object.add_parameter_to_modulation_matrix(param)
                self.notify_request_bank_view(u'Matrix')

        def jump_to_bank(bank_name):
            self.notify_request_bank_view(bank_name)

        def choose_envelope(value):
            self.envelope_switch.value = value

        def choose_lfo(value):
            self.lfo_switch.value = value

        self.osc_on_option = DeviceOnOffOption(name=u'Osc', property_host=self._get_osc_on_property_host())
        self.filter_on_option = DeviceOnOffOption(name=u'Filter', property_host=self._get_filter_on_property_host())
        self.lfo_retrigger_option = DeviceOnOffOption(name=u'Retrigger', property_host=self._get_lfo_retrigger_property_host())
        self.add_to_mod_matrix_option = DeviceTriggerOption(name=u'Add to Matrix', callback=add_selected_parameter_to_mod_matrix, is_active=is_selected_parameter_modulatable)
        return (DeviceOnOffOption(name=u'Sub', property_host=get_parameter_by_name(self, u'Sub On')),
         DeviceSwitchOption(name=u'Filter 1 Slope', parameter=get_parameter_by_name(self, u'Filter 1 Slope'), labels=[u'12dB', u'24dB']),
         DeviceSwitchOption(name=u'Filter 2 Slope', parameter=get_parameter_by_name(self, u'Filter 2 Slope'), labels=[u'12dB', u'24dB']),
         DeviceSwitchOption(name=u'Filter Switch', parameter=self.filter_switch_for_filter_switch_option, labels=[u'Filter 1', u'Filter 2']),
         DeviceSwitchOption(name=u'LFO 1 Sync', parameter=get_parameter_by_name(self, u'LFO 1 Sync'), labels=[u'Hz', u'Sync']),
         DeviceSwitchOption(name=u'LFO 2 Sync', parameter=get_parameter_by_name(self, u'LFO 2 Sync'), labels=[u'Hz', u'Sync']),
         DeviceTriggerOption(name=u'Go to Amp Env', callback=lambda : (choose_envelope(InstrumentVectorEnvelopeType.amp), jump_to_bank(u'Envelopes'))),
         DeviceTriggerOption(name=u'Go to Env 2', callback=lambda : (choose_envelope(InstrumentVectorEnvelopeType.env2), jump_to_bank(u'Envelopes'))),
         DeviceTriggerOption(name=u'Go to Env 3', callback=lambda : (choose_envelope(InstrumentVectorEnvelopeType.env3), jump_to_bank(u'Envelopes'))),
         DeviceTriggerOption(name=u'Go to LFO 1', callback=lambda : (choose_lfo(InstrumentVectorLfoType.one), jump_to_bank(u'LFOs'))),
         DeviceTriggerOption(name=u'Go to LFO 2', callback=lambda : (choose_lfo(InstrumentVectorLfoType.two), jump_to_bank(u'LFOs'))),
         DeviceTriggerOption(name=u'Back', callback=self.notify_request_previous_bank_from_mod_matrix)) + (self.osc_on_option,
         self.filter_on_option,
         self.lfo_retrigger_option,
         self.add_to_mod_matrix_option)

    def _get_parameter_by_name(self, name):
        return find_if(lambda p: p.name == name, self.parameters)

    def _get_osc_on_property_host(self):
        return get_parameter_by_name(self, u'Osc {} On'.format(2 if self.oscillator_switch.value else 1))

    def _get_filter_on_property_host(self):
        return get_parameter_by_name(self, u'Filter {} On'.format(self.filter_switch_for_filter_switch_option.value + 1))

    def _get_lfo_retrigger_property_host(self):
        return get_parameter_by_name(self, u'LFO {} Retrigger'.format(self._lfo_types_provider.index + 1))

    def _get_current_mod_target_parameter(self):
        target_parameter_name = self.get_modulation_target_parameter_name(self.current_mod_target_index.index)
        if re.match(u'^Osc (1|2) Transp$', target_parameter_name):
            target_parameter_name = target_parameter_name.replace(u'Transp', u'Pitch')
        return self._get_parameter_by_name(target_parameter_name)

    def _get_parameter_enabled_state(self, parameter):
        if parameter.value:
            return ParameterState.enabled
        return ParameterState.disabled

    @listens(u'value')
    def __on_oscillator_switch_value_changed(self):
        self.osc_on_option.set_property_host(self._get_osc_on_property_host())
        self.notify_oscillator_index()

    @listens(u'value')
    def __on_internal_filter_switch_value_changed(self):
        self.filter_on_option.set_property_host(self._get_filter_on_property_host())
        self.notify_filter_index()

    @listens(u'index')
    def __on_current_mod_target_index_changed(self):
        self.notify_current_mod_target_parameter()

    @listens(u'index')
    def __on_lfo_types_provider_index_changed(self):
        self.lfo_retrigger_option.set_property_host(self._get_lfo_retrigger_property_host())

    @listens(u'value')
    def __on_osc_1_on_value_changed(self):
        if liveobj_valid(self._osc_1_on_parameter):
            state = self._get_parameter_enabled_state(self._osc_1_on_parameter)
            self._osc_1_category_switch.state = state
            self._osc_1_table_switch.state = state
            self._osc_1_effect_type_switch.state = state
            self.osc_1_pitch.state = state

    @listens(u'value')
    def __on_osc_2_on_value_changed(self):
        if liveobj_valid(self._osc_2_on_parameter):
            state = self._get_parameter_enabled_state(self._osc_2_on_parameter)
            self._osc_2_category_switch.state = state
            self._osc_2_table_switch.state = state
            self._osc_2_effect_type_switch.state = state
            self.osc_2_pitch.state = state

    @listens(u'value')
    def __on_filter_1_on_value_changed(self):
        if liveobj_valid(self._filter_1_on_parameter):
            state = self._get_parameter_enabled_state(self._filter_1_on_parameter)
            self._filter_1_circuit_lp_hp_switch.state = state
            self._filter_1_circuit_bp_no_morph_switch.state = state

    @listens(u'value')
    def __on_filter_2_on_value_changed(self):
        if liveobj_valid(self._filter_2_on_parameter):
            state = self._get_parameter_enabled_state(self._filter_2_on_parameter)
            self._filter_2_circuit_lp_hp_switch.state = state
            self._filter_2_circuit_bp_no_morph_switch.state = state


class _UtilityDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, song = None, *a, **k):
        super(_UtilityDeviceDecorator, self).__init__(*a, **k)
        self.__on_parameters_changed.subject = self._live_object
        self.mono_option = DeviceOnOffOption(name=u'Mono', property_host=get_parameter_by_name(self, u'Mono'))
        self.bass_mono_option = DeviceOnOffOption(name=u'Bass Mono', property_host=get_parameter_by_name(self, u'Bass Mono'))
        self.dc_filter_option = DeviceOnOffOption(name=u'DC Filter', property_host=get_parameter_by_name(self, u'DC Filter'))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.mono_option, self.bass_mono_option, self.dc_filter_option)

    @listens(u'parameters')
    def __on_parameters_changed(self):
        self.mono_option.set_property_host(get_parameter_by_name(self, u'Mono'))
        self.bass_mono_option.set_property_host(get_parameter_by_name(self, u'Bass Mono'))


class DeviceDecoratorFactory(DecoratorFactory):
    DECORATOR_CLASSES = {u'OriginalSimpler': _SimplerDeviceDecorator,
     u'Operator': _OperatorDeviceDecorator,
     u'MultiSampler': _SamplerDeviceDecorator,
     u'AutoFilter': _AutoFilterDeviceDecorator,
     u'Eq8': _Eq8DeviceDecorator,
     u'Compressor2': _CompressorDeviceDecorator,
     u'Pedal': _PedalDeviceDecorator,
     u'DrumBuss': _DrumBussDeviceDecorator,
     u'Echo': _EchoDeviceDecorator,
     u'InstrumentVector': _InstrumentVectorDeviceDecorator,
     u'StereoGain': _UtilityDeviceDecorator}

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