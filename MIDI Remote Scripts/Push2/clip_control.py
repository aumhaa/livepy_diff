
from __future__ import absolute_import, print_function, unicode_literals
from MidiRemoteScript import MutableVector
from ableton.v2.base import listens, listens_group, liveobj_valid, listenable_property
from ableton.v2.control_surface import Component, CompoundComponent
from ableton.v2.control_surface.control import ButtonControl, EncoderControl, ToggleButtonControl
from pushbase.clip_control_component import convert_beat_length_to_bars_beats_sixteenths, convert_beat_time_to_bars_beats_sixteenths, LoopSettingsControllerComponent as LoopSettingsControllerComponentBase, AudioClipSettingsControllerComponent as AudioClipSettingsControllerComponentBase, ONE_YEAR_AT_120BPM_IN_BEATS, WARP_MODE_NAMES
from pushbase.internal_parameter import WrappingParameter
from pushbase.mapped_control import MappedControl
from pushbase.note_editor_component import DEFAULT_START_NOTE
from .clip_decoration import ClipDecoratorFactory
from .colors import COLOR_INDEX_TO_SCREEN_COLOR
from .decoration import find_decorated_object
from .real_time_channel import RealTimeDataComponent
from .timeline_navigation import ObjectDescription
PARAMETERS_LOOPED = (u'Loop position', u'Loop length', u'Start offset')
PARAMETERS_NOT_LOOPED = (u'Start', u'End')
PARAMETERS_AUDIO = (u'Warp',
 u'Transpose',
 u'Detune',
 u'Gain')

def make_color_vector(color_indices):
    color_vector = MutableVector()
    for color_index in color_indices:
        color_vector.append(COLOR_INDEX_TO_SCREEN_COLOR[color_index].as_remote_script_color())

    return color_vector


def make_vector(items):
    vector = MutableVector()
    for item in items:
        vector.append(item)

    return vector


class LoopSetting(WrappingParameter):
    min = -ONE_YEAR_AT_120BPM_IN_BEATS
    max = ONE_YEAR_AT_120BPM_IN_BEATS

    def __init__(self, use_length_conversion = False, *a, **k):
        super(LoopSetting, self).__init__(*a, **k)
        raise self.canonical_parent is not None or AssertionError
        self._conversion = convert_beat_length_to_bars_beats_sixteenths if use_length_conversion else convert_beat_time_to_bars_beats_sixteenths
        self._recording = False
        self.set_property_host(self._parent)
        self.__on_clip_changed.subject = self.canonical_parent
        self.__on_clip_changed()

    @property
    def recording(self):
        return self._recording

    @recording.setter
    def recording(self, value):
        self._recording = value
        self.notify_value()

    @listens(u'clip')
    def __on_clip_changed(self):
        self.__on_signature_numerator_changed.subject = self.canonical_parent.clip
        self.__on_signature_denominator_changed.subject = self.canonical_parent.clip

    @listens(u'signature_numerator')
    def __on_signature_numerator_changed(self):
        self.notify_value()

    @listens(u'signature_denominator')
    def __on_signature_denominator_changed(self):
        self.notify_value()

    @property
    def display_value(self):
        if not liveobj_valid(self.canonical_parent.clip):
            return unicode(u'-')
        if self.recording:
            return unicode(u'...')
        return unicode(self._conversion((self.canonical_parent.clip.signature_numerator, self.canonical_parent.clip.signature_denominator), self._get_property_value()))


class LoopSettingsControllerComponent(LoopSettingsControllerComponentBase):
    __events__ = (u'looping', u'loop_parameters', u'zoom', u'clip')
    ZOOM_DEFAULT_SENSITIVITY = MappedControl.DEFAULT_SENSITIVITY
    ZOOM_FINE_SENSITIVITY = MappedControl.FINE_SENSITIVITY
    zoom_encoder = MappedControl()
    zoom_touch_encoder = EncoderControl()
    loop_button = ToggleButtonControl(toggled_color=u'Clip.Option', untoggled_color=u'Clip.OptionDisabled')
    crop_button = ButtonControl(color=u'Clip.Action')

    def __init__(self, *a, **k):
        super(LoopSettingsControllerComponent, self).__init__(*a, **k)
        self._looping_settings = [LoopSetting(name=PARAMETERS_LOOPED[0], parent=self._loop_model, source_property=u'position'), LoopSetting(name=PARAMETERS_LOOPED[1], parent=self._loop_model, use_length_conversion=True, source_property=u'loop_length'), LoopSetting(name=PARAMETERS_LOOPED[2], parent=self._loop_model, source_property=u'start_marker')]
        self._non_looping_settings = [LoopSetting(name=PARAMETERS_NOT_LOOPED[0], parent=self._loop_model, source_property=u'loop_start'), LoopSetting(name=PARAMETERS_NOT_LOOPED[1], parent=self._loop_model, source_property=u'loop_end')]
        for setting in self._looping_settings + self._non_looping_settings:
            self.register_disconnectable(setting)

        self.__on_looping_changed.subject = self._loop_model
        self.__on_looping_changed()

    def update(self):
        super(LoopSettingsControllerComponent, self).update()
        if self.is_enabled():
            self.notify_timeline_navigation()
            self.notify_clip()

    @loop_button.toggled
    def loop_button(self, toggled, button):
        self._loop_model.looping = toggled

    @crop_button.pressed
    def crop_button(self, button):
        if liveobj_valid(self.clip):
            self.clip.crop()

    @property
    def looping(self):
        if self.clip:
            return self._loop_model.looping
        return False

    @property
    def loop_parameters(self):
        if not liveobj_valid(self.clip):
            return []
        parameters = self._looping_settings if self.looping else self._non_looping_settings
        if self.zoom:
            return [self.zoom] + parameters
        return parameters

    @property
    def zoom(self):
        if liveobj_valid(self.clip):
            return getattr(self.clip, u'zoom', None)

    @listenable_property
    def timeline_navigation(self):
        if liveobj_valid(self.clip):
            return getattr(self.clip, u'timeline_navigation', None)

    @listens(u'is_recording')
    def __on_is_recording_changed(self):
        self._update_recording_state()

    @listens(u'is_overdubbing')
    def __on_is_overdubbing_changed(self):
        self._update_recording_state()

    def _update_recording_state(self):
        clip = self._loop_model.clip
        if liveobj_valid(clip):
            recording = clip.is_recording and not clip.is_overdubbing
            self._looping_settings[1].recording = recording
            self._non_looping_settings[1].recording = recording

    @listens(u'looping')
    def __on_looping_changed(self):
        self._update_and_notify()

    def _update_loop_button(self):
        self.loop_button.enabled = liveobj_valid(self.clip)
        if liveobj_valid(self.clip):
            self.loop_button.is_toggled = self._loop_model.looping

    def _on_clip_changed(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.reset_focus_and_animation()
        self._update_and_notify()
        self.__on_is_recording_changed.subject = self._loop_model.clip
        self.__on_is_overdubbing_changed.subject = self._loop_model.clip
        self._update_recording_state()
        self.crop_button.enabled = liveobj_valid(self.clip) and self.clip.is_midi_clip
        self._connect_encoder()
        if self.is_enabled():
            self.notify_timeline_navigation()

    def _on_clip_start_marker_touched(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.touch_object(self.timeline_navigation.start_marker_focus)

    def _on_clip_position_touched(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.touch_object(self.timeline_navigation.loop_start_focus)

    def _on_clip_end_touched(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.touch_object(self.timeline_navigation.loop_end_focus)

    def _on_clip_start_marker_released(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.release_object(self.timeline_navigation.start_marker_focus)

    def _on_clip_position_released(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.release_object(self.timeline_navigation.loop_start_focus)

    def _on_clip_end_released(self):
        if self.timeline_navigation is not None:
            self.timeline_navigation.release_object(self.timeline_navigation.loop_end_focus)

    @zoom_touch_encoder.touched
    def zoom_touch_encoder(self, encoder):
        if self.timeline_navigation is not None:
            self.timeline_navigation.touch_object(self.timeline_navigation.zoom_focus)

    @zoom_touch_encoder.released
    def zoom_touch_encoder(self, encoder):
        if self.timeline_navigation is not None:
            self.timeline_navigation.release_object(self.timeline_navigation.zoom_focus)

    def _update_and_notify(self):
        self._update_loop_button()
        self.notify_looping()
        self.notify_loop_parameters()
        self.notify_zoom()

    def _connect_encoder(self):
        self.zoom_encoder.mapped_parameter = self.zoom
        self.zoom_encoder.update_sensitivities(self.ZOOM_DEFAULT_SENSITIVITY, self.ZOOM_FINE_SENSITIVITY)

    def set_zoom_encoder(self, encoder):
        self.zoom_encoder.set_control_element(encoder)
        self.zoom_touch_encoder.set_control_element(encoder)
        self._connect_encoder()


class GainSetting(WrappingParameter):

    def __init__(self, *a, **k):
        super(GainSetting, self).__init__(*a, **k)
        self.set_property_host(self._parent)

    @property
    def display_value(self):
        return unicode(self._property_host.clip.gain_display_string if self._property_host.clip else u'')


class PitchSetting(WrappingParameter):

    def __init__(self, min_value, max_value, unit, *a, **k):
        super(PitchSetting, self).__init__(*a, **k)
        self._min = min_value
        self._max = max_value
        self._unit = unit
        self.set_property_host(self._parent)

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def display_value(self):
        value = int(round(float(self._get_property_value())))
        positive_indicator = u'+' if value > 0 else u''
        return positive_indicator + str(value) + self._unit


class WarpSetting(WrappingParameter):

    def __init__(self, *a, **k):
        super(WarpSetting, self).__init__(*a, **k)
        self.set_property_host(self._parent)

    @property
    def max(self):
        return len(self._property_host.available_warp_modes) - 1

    @property
    def is_quantized(self):
        return True

    @property
    def value_items(self):
        return map(lambda x: unicode(WARP_MODE_NAMES[x]), self._property_host.available_warp_modes)

    def _get_property_value(self):
        return self._property_host.available_warp_modes.index(getattr(self._property_host, self._source_property))


class AudioClipSettingsControllerComponent(AudioClipSettingsControllerComponentBase, CompoundComponent):
    __events__ = (u'audio_parameters', u'warping', u'gain')

    def __init__(self, *a, **k):
        super(AudioClipSettingsControllerComponent, self).__init__(*a, **k)
        self._audio_clip_parameters = [WarpSetting(name=PARAMETERS_AUDIO[0], parent=self._audio_clip_model, source_property=u'warp_mode'),
         PitchSetting(name=PARAMETERS_AUDIO[1], parent=self._audio_clip_model, source_property=u'pitch_coarse', min_value=-49.0, max_value=49.0, unit=u'st'),
         PitchSetting(name=PARAMETERS_AUDIO[2], parent=self._audio_clip_model, source_property=u'pitch_fine', min_value=-51.0, max_value=51.0, unit=u'ct'),
         GainSetting(name=PARAMETERS_AUDIO[3], parent=self._audio_clip_model, source_property=u'gain')]
        self._playhead_real_time_data = self.register_component(RealTimeDataComponent(channel_type=u'playhead'))
        self._waveform_real_time_data = self.register_component(RealTimeDataComponent(channel_type=u'waveform'))
        for parameter in self._audio_clip_parameters:
            self.register_disconnectable(parameter)

        self.__on_warping_changed.subject = self._audio_clip_model
        self.__on_gain_changed.subject = self._audio_clip_model
        self.__on_warping_changed()
        self.__on_gain_changed()

    def disconnect(self):
        super(AudioClipSettingsControllerComponent, self).disconnect()
        self._playhead_real_time_data.set_data(None)
        self._waveform_real_time_data.set_data(None)

    @property
    def audio_parameters(self):
        if liveobj_valid(self.clip):
            return self._audio_clip_parameters
        return []

    @property
    def warping(self):
        if liveobj_valid(self.clip):
            return self._audio_clip_model.warping
        return False

    @property
    def gain(self):
        if liveobj_valid(self.clip):
            return self._audio_clip_model.gain
        return 0.0

    @property
    def waveform_real_time_channel_id(self):
        return self._waveform_real_time_data.channel_id

    @property
    def playhead_real_time_channel_id(self):
        return self._playhead_real_time_data.channel_id

    def _on_clip_changed(self):
        self._playhead_real_time_data.set_data(self.clip)
        self._waveform_real_time_data.set_data(self.clip)
        self.__on_file_path_changed.subject = self.clip
        self.notify_audio_parameters()
        self.notify_warping()
        self.notify_gain()

    def _on_transpose_encoder_value(self, value):
        self._audio_clip_model.set_clip_pitch_coarse(value, False)

    def _on_detune_encoder_value(self, value):
        self._audio_clip_model.set_clip_pitch_fine(value, False)

    @listens(u'warping')
    def __on_warping_changed(self):
        self.notify_warping()

    @listens(u'gain')
    def __on_gain_changed(self):
        self.notify_gain()

    @listens(u'file_path')
    def __on_file_path_changed(self):
        self._waveform_real_time_data.invalidate()


def register_matrix_mode(matrix_map, name, modes_component = None, parent_path = None):

    def find_leaf(tree, path):
        key_name, rest = path[0], path[1:]
        if key_name not in tree:
            tree[key_name] = dict(modes_component=None, children={})
        sub_tree = tree[key_name][u'children']
        if len(rest) == 0:
            return sub_tree
        return find_leaf(sub_tree, rest)

    matrix_map_to_edit = matrix_map if parent_path is None else find_leaf(matrix_map, parent_path)
    children_to_add_to_map = matrix_map_to_edit[name].get(u'children', {}) if name in matrix_map_to_edit else {}
    matrix_map_to_edit[name] = dict(modes_component=modes_component, children=children_to_add_to_map)


class MatrixModeWatcherComponent(Component):

    def __init__(self, matrix_mode_map = None, *a, **k):
        super(MatrixModeWatcherComponent, self).__init__(*a, **k)
        self._matrix_mode_map = matrix_mode_map

        def connect_listeners(dct):
            for key, value in dct.iteritems():
                if key == u'modes_component':
                    self.register_slot(value, self.__on_matrix_mode_changed, u'selected_mode')
                else:
                    connect_listeners(value)

        connect_listeners(matrix_mode_map)
        self._matrix_mode_path = None
        self.matrix_mode_path = self.create_mode_path(matrix_mode_map)

    @staticmethod
    def create_mode_path(initial_mode_map):
        mode_path = []

        def create_mode_path_recursive(mode_map):
            mode_entry = mode_map.keys()[0]
            mode_path.append(mode_entry)
            parent = mode_map[mode_entry]
            children = parent[u'children']
            modes_comp = parent[u'modes_component']
            selected_mode = modes_comp.selected_mode
            if selected_mode in children:
                if len(children[selected_mode][u'children'].keys()) > 0:
                    return create_mode_path_recursive({selected_mode: children[selected_mode]})
                mode_path.append(selected_mode)
            return mode_path

        return u'.'.join(create_mode_path_recursive(initial_mode_map))

    @listenable_property
    def matrix_mode_path(self):
        return self._matrix_mode_path

    @matrix_mode_path.setter
    def matrix_mode_path(self, mode):
        if self._matrix_mode_path != mode:
            self._matrix_mode_path = mode
            self.notify_matrix_mode_path()

    def __on_matrix_mode_changed(self, mode):
        if mode is not None:
            self.matrix_mode_path = self.create_mode_path(self._matrix_mode_map)


_MATRIX_MODE_PATH_TO_DATA = {u'matrix_modes.note.instrument.play': {u'Fold': True,
                                        u'NumDisplayKeys': 0,
                                        u'ShowGridWindow': False,
                                        u'ShowScrollbarCursor': False,
                                        u'NumPitches': 128,
                                        u'PitchOffset': 0,
                                        u'ShowStepLengthGrid': False},
 u'matrix_modes.note.instrument.sequence': {u'Fold': False,
                                            u'NumDisplayKeys': 23,
                                            u'ShowGridWindow': True,
                                            u'ShowScrollbarCursor': True,
                                            u'NumPitches': 128,
                                            u'PitchOffset': 0,
                                            u'ShowStepLengthGrid': True},
 u'matrix_modes.note.instrument.split_melodic_sequencer': {u'Fold': False,
                                                           u'NumDisplayKeys': 32,
                                                           u'ShowGridWindow': True,
                                                           u'ShowScrollbarCursor': True,
                                                           u'NumPitches': 128,
                                                           u'PitchOffset': 0,
                                                           u'ShowStepLengthGrid': True},
 u'matrix_modes.note.drums.64pads': {u'Fold': True,
                                     u'NumDisplayKeys': 0,
                                     u'ShowGridWindow': False,
                                     u'ShowScrollbarCursor': False,
                                     u'NumPitches': 128,
                                     u'PitchOffset': 0,
                                     u'ShowStepLengthGrid': False},
 u'matrix_modes.note.drums.sequencer_loop': {u'Fold': False,
                                             u'NumDisplayKeys': 17,
                                             u'ShowGridWindow': True,
                                             u'ShowScrollbarCursor': True,
                                             u'NumPitches': 128,
                                             u'PitchOffset': 0,
                                             u'ShowStepLengthGrid': True},
 u'matrix_modes.note.drums.sequencer_velocity_levels': {u'Fold': False,
                                                        u'NumDisplayKeys': 17,
                                                        u'ShowGridWindow': True,
                                                        u'ShowScrollbarCursor': True,
                                                        u'NumPitches': 128,
                                                        u'PitchOffset': 0,
                                                        u'ShowStepLengthGrid': True},
 u'matrix_modes.note.slicing.64pads': {u'Fold': True,
                                       u'NumDisplayKeys': 0,
                                       u'ShowGridWindow': False,
                                       u'ShowScrollbarCursor': False,
                                       u'NumPitches': 64,
                                       u'PitchOffset': 36,
                                       u'ShowStepLengthGrid': False},
 u'matrix_modes.note.slicing.sequencer_loop': {u'Fold': False,
                                               u'NumDisplayKeys': 17,
                                               u'ShowGridWindow': True,
                                               u'ShowScrollbarCursor': True,
                                               u'NumPitches': 64,
                                               u'PitchOffset': 36,
                                               u'ShowStepLengthGrid': True},
 u'matrix_modes.note.slicing.sequencer_velocity_levels': {u'Fold': False,
                                                          u'NumDisplayKeys': 17,
                                                          u'ShowGridWindow': True,
                                                          u'ShowScrollbarCursor': True,
                                                          u'NumPitches': 64,
                                                          u'PitchOffset': 36,
                                                          u'ShowStepLengthGrid': True},
 u'matrix_modes.session': {u'Fold': True,
                           u'NumDisplayKeys': 0,
                           u'ShowGridWindow': False,
                           u'ShowScrollbarCursor': False,
                           u'NumPitches': 128,
                           u'PitchOffset': 0,
                           u'ShowStepLengthGrid': False}}
_DEFAULT_VIEW_DATA = {u'Fold': True,
 u'NumDisplayKeys': 0,
 u'ShowGridWindow': False,
 u'ShowScrollbarCursor': False,
 u'MinPitch': DEFAULT_START_NOTE,
 u'MaxSequenceablePitch': DEFAULT_START_NOTE,
 u'MinSequenceablePitch': DEFAULT_START_NOTE,
 u'PageIndex': 0,
 u'PageLength': 1.0,
 u'MinGridWindowPitch': DEFAULT_START_NOTE,
 u'MaxGridWindowPitch': DEFAULT_START_NOTE,
 u'NumPitches': 128,
 u'PitchOffset': 0,
 u'ShowStepLengthGrid': False,
 u'IsRecording': False}

def get_static_view_data(matrix_mode_path):
    return _MATRIX_MODE_PATH_TO_DATA.get(matrix_mode_path, _DEFAULT_VIEW_DATA)


class MidiClipControllerComponent(CompoundComponent):
    grid_window_focus = u'grid_window_start'

    def __init__(self, *a, **k):
        super(MidiClipControllerComponent, self).__init__(*a, **k)
        self._clip = None
        self._matrix_mode_watcher = None
        self._most_recent_base_note = DEFAULT_START_NOTE
        self._most_recent_max_note = DEFAULT_START_NOTE
        self._loose_follow_base_note = DEFAULT_START_NOTE
        self._most_recent_editable_pitches = (DEFAULT_START_NOTE, DEFAULT_START_NOTE)
        self._most_recent_row_start_times = []
        self._most_recent_step_length = 1.0
        self._most_recent_page_index = 0
        self._most_recent_page_length = 1.0
        self._most_recent_editing_note_regions = []
        self._visualisation_real_time_data = self.register_component(RealTimeDataComponent(channel_type=u'visualisation'))
        self.__on_visualisation_channel_changed.subject = self._visualisation_real_time_data
        self.__on_visualisation_attached.subject = self._visualisation_real_time_data
        self._instruments_with_note_colors = []
        self._sequencers = []
        self._note_settings_component = None
        self._note_editor_settings_component = None

    @property
    def clip(self):
        return self._clip

    @clip.setter
    def clip(self, clip):
        self._clip = clip
        self._on_clip_changed()

    @listenable_property
    def visualisation_real_time_channel_id(self):
        return self._visualisation_real_time_data.channel_id

    def set_matrix_mode_watcher(self, watcher):
        self._matrix_mode_watcher = watcher
        self.__on_matrix_mode_changed.subject = watcher

    def external_regions_of_interest_creator(self, region_of_interest_creator):

        def grid_start_time():
            return self._most_recent_page_index * self._most_recent_page_length

        return {u'grid_window': region_of_interest_creator(start_identifier=self.grid_window_focus, getter=lambda : (grid_start_time(), grid_start_time() + self._most_recent_page_length))}

    @property
    def external_focusable_object_descriptions(self):
        return {self.grid_window_focus: ObjectDescription((u'start_end', u'loop', u'grid_window'), self.grid_window_focus)}

    def set_note_settings_component(self, note_settings_component):
        self._note_settings_component = note_settings_component
        self.__on_note_settings_enabled_changed.subject = note_settings_component

    def set_note_editor_settings_component(self, note_editor_settings_component):
        self._note_editor_settings_component = note_editor_settings_component
        self.__on_note_editor_settings_touched_changed.subject = note_editor_settings_component

    def add_instrument_component(self, instrument):
        self.__on_instrument_position_changed.add_subject(instrument)
        if hasattr(instrument, u'note_colors'):
            self.__on_note_colors_changed.add_subject(instrument)
            self._instruments_with_note_colors.append(instrument)

    def add_paginator(self, paginator):
        self.__on_paginator_page_index_changed.add_subject(paginator)
        self.__on_paginator_page_length_changed.add_subject(paginator)

    def add_sequencer(self, sequencer):
        self.__on_editable_pitch_range_changed.add_subject(sequencer)
        self.__on_row_start_times_changed.add_subject(sequencer)
        self.__on_step_length_changed.add_subject(sequencer)
        self.__on_selected_notes_changed.add_subject(sequencer)
        self._sequencers.append(sequencer)

    def disconnect(self):
        super(MidiClipControllerComponent, self).disconnect()
        self._visualisation_real_time_data.set_data(None)

    def update(self):
        super(MidiClipControllerComponent, self).update()
        if self.is_enabled():
            self.__on_matrix_mode_changed()

    def _on_clip_changed(self):
        self._visualisation_real_time_data.set_data(getattr(self.clip, u'proxied_object', self.clip))
        self.__on_clip_color_changed.subject = self.clip
        self.__on_visible_region_changed.subject = getattr(self.clip, u'timeline_navigation', None)

    def _focus_grid_window(self):
        if liveobj_valid(self.clip) and self.get_static_view_data()[u'ShowGridWindow']:
            self.clip.timeline_navigation.change_object(self.grid_window_focus)

    @listens(u'enabled')
    def __on_note_settings_enabled_changed(self, _):
        self._configure_visualisation()

    @listens(u'is_touched')
    def __on_note_editor_settings_touched_changed(self):
        self._configure_visualisation()

    @listens_group(u'editing_note_regions')
    def __on_selected_notes_changed(self, sequencer):
        self._most_recent_editing_note_regions = sequencer.editing_note_regions
        self._configure_visualisation()

    @listens(u'channel_id')
    def __on_visualisation_channel_changed(self):
        self.notify_visualisation_real_time_channel_id()

    @listens(u'attached')
    def __on_visualisation_attached(self):
        self._configure_visualisation()

    @listens(u'color_index')
    def __on_clip_color_changed(self):
        self._configure_visualisation()

    @listens(u'visible_region')
    def __on_visible_region_changed(self, *a):
        self._configure_visualisation()

    @listens(u'matrix_mode_path')
    def __on_matrix_mode_changed(self):
        if self.is_enabled():
            static_view_data = self.get_static_view_data()
            if self.matrix_mode_path() == u'matrix_modes.note.instrument.sequence':
                num_visible_keys = static_view_data[u'NumDisplayKeys']
                lower, upper = self._most_recent_editable_pitches
                self._loose_follow_base_note = (lower + upper) // 2 - num_visible_keys // 2
            if static_view_data[u'ShowGridWindow']:
                self._focus_grid_window()
            elif liveobj_valid(self.clip):
                nav = self.clip.timeline_navigation
                nav.set_focus_marker_without_updating_visible_region(u'start_marker')
            self._configure_visualisation()

    @listens_group(u'position')
    def __on_instrument_position_changed(self, instrument):
        self._most_recent_base_note = instrument.min_pitch
        self._most_recent_max_note = instrument.max_pitch
        self._configure_visualisation()

    @listens_group(u'note_colors')
    def __on_note_colors_changed(self, instrument):
        self._configure_visualisation()

    @listens_group(u'editable_pitch_range')
    def __on_editable_pitch_range_changed(self, sequencer):
        self._most_recent_editable_pitches = sequencer.editable_pitch_range
        self._configure_visualisation()

    def __update_row_start_times(self):
        enabled_sequencers = filter(lambda s: s.is_enabled(), self._sequencers)
        if len(enabled_sequencers) == 1:
            self._most_recent_row_start_times = enabled_sequencers[0].row_start_times

    @listens_group(u'row_start_times')
    def __on_row_start_times_changed(self, sequencer):
        if sequencer.is_enabled():
            self.__update_row_start_times()
            self._configure_visualisation()

    @listens_group(u'step_length')
    def __on_step_length_changed(self, sequencer):
        if sequencer.is_enabled():
            self._most_recent_step_length = sequencer.step_length
            self._configure_visualisation()

    @listens_group(u'page_index')
    def __on_paginator_page_index_changed(self, paginator):
        self._most_recent_page_index = paginator.page_index
        self._focus_grid_window()
        self._configure_visualisation()

    @listens_group(u'page_length')
    def __on_paginator_page_length_changed(self, paginator):
        self._most_recent_page_length = paginator.page_length
        self._focus_grid_window()
        self._configure_visualisation()

    def get_static_view_data(self):
        return get_static_view_data(self._matrix_mode_watcher.matrix_mode_path)

    def _add_items_to_view_data(self, view_data):
        for key, value in self.get_static_view_data().iteritems():
            view_data[key] = value

    def matrix_mode_path(self):
        if self._matrix_mode_watcher is not None:
            return self._matrix_mode_watcher.matrix_mode_path

    def _update_grid_window_pitch_range(self, view_data):
        if self.matrix_mode_path() == u'matrix_modes.note.instrument.split_melodic_sequencer':
            view_data[u'MinGridWindowPitch'] = self._most_recent_base_note
            view_data[u'MaxGridWindowPitch'] = self._most_recent_max_note
        else:
            view_data[u'MinGridWindowPitch'] = self._most_recent_editable_pitches[0]
            view_data[u'MaxGridWindowPitch'] = self._most_recent_editable_pitches[1]

    def _update_minimum_pitch(self, view_data):
        if self.matrix_mode_path() == u'matrix_modes.note.instrument.sequence':
            num_visible_keys = self.get_static_view_data()[u'NumDisplayKeys']
            lower, upper = self._most_recent_editable_pitches
            window_size = upper - lower
            base_note = self._loose_follow_base_note
            if window_size >= num_visible_keys / 3:
                base_note = (lower + upper) / 2 - num_visible_keys / 2
            else:
                if lower - window_size < base_note:
                    base_note = lower - window_size
                if upper + window_size > base_note + num_visible_keys:
                    base_note = upper + window_size - num_visible_keys
            self._loose_follow_base_note = max(0, min(127 - num_visible_keys, base_note))
            view_data[u'MinPitch'] = self._loose_follow_base_note
        else:
            view_data[u'MinPitch'] = self._most_recent_base_note

    def _update_maximum_sequenceable_pitch(self, view_data):
        if self.matrix_mode_path() == u'matrix_modes.note.instrument.sequence':
            view_data[u'MaxSequenceablePitch'] = self._most_recent_editable_pitches[1]
        else:
            view_data[u'MaxSequenceablePitch'] = self._most_recent_max_note

    def _update_minimum_sequenceable_pitch(self, view_data):
        view_data[u'MinSequenceablePitch'] = self._most_recent_editable_pitches[0] if self.matrix_mode_path() == u'matrix_modes.note.instrument.sequence' else self._most_recent_base_note

    def _update_note_colors(self, view_data):
        note_colors = []
        matrix_mode = self.matrix_mode_path()
        if matrix_mode is not None and matrix_mode.startswith(u'matrix_modes.note.drums'):
            enabled_instruments = filter(lambda instrument: instrument.is_enabled(), self._instruments_with_note_colors)
            if len(enabled_instruments) == 1:
                note_colors = enabled_instruments[0].note_colors
        view_data[u'NoteColors'] = make_color_vector(note_colors)

    def _configure_visualisation(self):
        visualisation = self._visualisation_real_time_data.device_visualisation()
        if liveobj_valid(visualisation) and liveobj_valid(self.clip):
            view_data = visualisation.get_view_data()
            color = COLOR_INDEX_TO_SCREEN_COLOR[self.clip.color_index]
            view_data[u'ClipColor'] = color.as_remote_script_color()
            view_data[u'PageIndex'] = self._most_recent_page_index
            view_data[u'PageLength'] = self._most_recent_page_length
            view_data[u'RowStartTimes'] = make_vector(self._most_recent_row_start_times)
            view_data[u'StepLength'] = self._most_recent_step_length
            self._update_grid_window_pitch_range(view_data)
            self._update_minimum_pitch(view_data)
            self._update_maximum_sequenceable_pitch(view_data)
            self._update_minimum_sequenceable_pitch(view_data)
            self._update_note_colors(view_data)
            view_data[u'IsRecording'] = liveobj_valid(self.clip) and self.clip.is_recording and not self.clip.is_overdubbing
            if hasattr(self.clip, u'zoom'):
                visible_region = self.clip.zoom.visible_region
                view_data[u'DisplayStartTime'] = visible_region.start
                view_data[u'DisplayEndTime'] = visible_region.end
            view_data[u'NoteSettingsMode'] = self._note_settings_component is not None and self._note_settings_component.is_enabled()
            view_data[u'NoteSettingsTouched'] = self._note_editor_settings_component is not None and self._note_editor_settings_component.is_enabled() and self._note_editor_settings_component.is_touched
            view_data[u'EditingNotePitches'] = make_vector([ pitch for pitch, (start, end) in self._most_recent_editing_note_regions ])
            view_data[u'EditingNoteStarts'] = make_vector([ float(start) for pitch, (start, end) in self._most_recent_editing_note_regions ])
            view_data[u'EditingNoteEnds'] = make_vector([ float(end) for pitch, (start, end) in self._most_recent_editing_note_regions ])
            if self._matrix_mode_watcher is not None:
                self._add_items_to_view_data(view_data)
            visualisation.set_view_data(view_data)


class ClipControlComponent(CompoundComponent):
    __events__ = (u'clip',)

    def __init__(self, midi_loop_controller = None, audio_loop_controller = None, audio_clip_controller = None, midi_clip_controller = None, mode_selector = None, decorator_factory = None, *a, **k):
        raise audio_loop_controller is not None or AssertionError
        raise midi_loop_controller is not None or AssertionError
        raise audio_clip_controller is not None or AssertionError
        raise midi_clip_controller is not None or AssertionError
        raise mode_selector is not None or AssertionError
        super(ClipControlComponent, self).__init__(*a, **k)
        self._clip = None
        self._midi_loop_controller = self.register_component(midi_loop_controller)
        self._audio_loop_controller = self.register_component(audio_loop_controller)
        self._audio_clip_controller = self.register_component(audio_clip_controller)
        self._midi_clip_controller = self.register_component(midi_clip_controller)
        self._mode_selector = self.register_component(mode_selector)
        self._decorator_factory = decorator_factory or ClipDecoratorFactory()
        self.__on_selected_scene_changed.subject = self.song.view
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_clip_changed.subject = self.song.view
        self.__on_has_clip_changed.subject = self.song.view.highlighted_clip_slot
        self._update_controller()

    @listens(u'selected_scene')
    def __on_selected_scene_changed(self):
        self._update_controller()

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._update_controller()

    @listens(u'detail_clip')
    def __on_selected_clip_changed(self):
        self._update_controller()

    def on_enabled_changed(self):
        super(ClipControlComponent, self).on_enabled_changed()
        self._update_controller()

    def _decorate_clip(self, clip):
        return find_decorated_object(clip, self._decorator_factory) or self._decorator_factory.decorate(clip)

    @listens(u'has_clip')
    def __on_has_clip_changed(self):
        self._update_controller()

    def _update_controller(self):
        if self.is_enabled():
            clip = self.song.view.detail_clip
            track = None
            if liveobj_valid(clip):
                if clip.is_arrangement_clip:
                    track = clip.canonical_parent
                else:
                    clip_slot = clip.canonical_parent
                    track = clip_slot.canonical_parent if clip_slot else None
            if track != self.song.view.selected_track:
                clip = None
            self._update_selected_mode(clip)
            audio_clip = None
            midi_clip = None
            if liveobj_valid(clip) and clip.is_audio_clip:
                audio_clip = clip
            else:
                midi_clip = clip
            self._audio_clip_controller.clip = audio_clip
            self._audio_loop_controller.clip = self._decorate_clip(audio_clip)
            decorated_midi_clip = self._decorate_clip(midi_clip)
            self._midi_clip_controller.clip = decorated_midi_clip
            self._midi_loop_controller.clip = decorated_midi_clip
            self.__on_has_clip_changed.subject = self.song.view.highlighted_clip_slot
            self._clip = clip
            self.notify_clip()

    def _update_selected_mode(self, clip):
        if liveobj_valid(clip):
            self._mode_selector.selected_mode = u'audio' if clip.is_audio_clip else u'midi'
        else:
            self._mode_selector.selected_mode = u'no_clip'

    @property
    def clip(self):
        return self._clip