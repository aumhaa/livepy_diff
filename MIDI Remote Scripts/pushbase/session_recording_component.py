
from __future__ import absolute_import, print_function
import Live
from ableton.v2.base import listens, EventObject
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.components import SessionRecordingComponent
from .consts import MessageBoxText
from .message_box_component import Messenger
Quantization = Live.Song.Quantization

def track_can_overdub(track):
    return not track.has_audio_input


def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


class FixedLengthRecording(EventObject):

    def __init__(self, song = None, clip_creator = None, fixed_length_setting = None, *a, **k):
        raise song is not None or AssertionError
        raise clip_creator is not None or AssertionError
        raise fixed_length_setting is not None or AssertionError
        super(FixedLengthRecording, self).__init__(*a, **k)
        self._song = song
        self._clip_creator = clip_creator
        self._fixed_length_setting = fixed_length_setting
        self._clip_creator.fixed_length = 8.0
        self._clip_creator.legato_launch = self._fixed_length_setting.legato_launch
        self.__on_setting_selected_index_changes.subject = self._fixed_length_setting
        self.__on_setting_legato_launch_changes.subject = self._fixed_length_setting

    def should_start_fixed_length_recording(self, clip_slot):
        return track_can_record(clip_slot.canonical_parent) and not clip_slot.is_recording and not clip_slot.has_clip and self._fixed_length_setting.enabled

    def start_recording_in_slot(self, track, clip_slot_index):
        song = self._song
        song.overdub = True
        if track_can_record(track):
            self._record_in_slot(track, track.clip_slots[clip_slot_index])
        if not song.is_playing:
            song.is_playing = True

    def _is_infinite_recording(self, clip):
        return not clip.is_overdubbing

    def stop_recording(self, clip):
        if not self._is_infinite_recording(clip):
            self._song.overdub = False
        else:
            self._song.session_record = False

    def _record_in_slot(self, track, clip_slot):
        if self.should_start_fixed_length_recording(clip_slot):
            length, quant = self._fixed_length_setting.get_selected_length(self._song)
            if track_can_overdub(track):
                self._clip_creator.create(clip_slot, length=length, launch_quantization=self._song.clip_trigger_quantization)
            else:
                clip_slot.fire(record_length=length, launch_quantization=quant)
        elif not clip_slot.is_playing or not self._song.is_playing:
            if clip_slot.has_clip:
                clip_slot.fire(force_legato=True, launch_quantization=Quantization.q_no_q)
            else:
                clip_slot.fire()

    @listens('selected_index')
    def __on_setting_selected_index_changes(self, _):
        length, _ = self._fixed_length_setting.get_selected_length(self._song)
        self._clip_creator.fixed_length = length

    @listens('legato_launch')
    def __on_setting_legato_launch_changes(self, value):
        self._clip_creator.legato_launch = value


class FixedLengthSessionRecordingComponent(SessionRecordingComponent, Messenger):
    foot_switch_button = ButtonControl()
    arrangement_record_button = ButtonControl()

    def __init__(self, clip_creator = None, fixed_length_setting = None, *a, **k):
        raise clip_creator is not None or AssertionError
        raise fixed_length_setting is not None or AssertionError
        super(FixedLengthSessionRecordingComponent, self).__init__(*a, **k)
        self._fixed_length_recording = self.register_disconnectable(FixedLengthRecording(song=self.song, clip_creator=clip_creator, fixed_length_setting=fixed_length_setting))
        self.footswitch_toggles_arrangement_recording = False
        self.__on_record_mode_changed.subject = self.song
        self.__on_record_mode_changed()

    @foot_switch_button.pressed
    def foot_switch_button(self, button):
        if self.footswitch_toggles_arrangement_recording:
            self._toggle_arrangement_recording()
        else:
            self._trigger_recording()

    @arrangement_record_button.pressed
    def arrangement_record_button(self, button):
        self._toggle_arrangement_recording()

    def _toggle_arrangement_recording(self):
        self.song.record_mode = not self.song.record_mode

    def _clip_slot_index_to_record_into(self):
        song = self.song
        selected_scene = song.view.selected_scene
        return list(song.scenes).index(selected_scene)

    def _update_record_button(self):
        if self.is_enabled():
            if self.song.record_mode:
                self._record_button.color = 'Recording.ArrangementRecordingOn'
            else:
                super(FixedLengthSessionRecordingComponent, self)._update_record_button()
            self.arrangement_record_button.color = self._record_button.color

    @listens('record_mode')
    def __on_record_mode_changed(self):
        self._update_record_button()

    def _start_recording(self):
        track = self.song.view.selected_track
        clip_slot_index = self._clip_slot_index_to_record_into()
        self._fixed_length_recording.start_recording_in_slot(track, clip_slot_index)
        if track_can_record(track):
            self._ensure_slot_is_visible(self.song.view.selected_track, clip_slot_index)

    def _ensure_slot_is_visible(self, track, scene_index):
        song = self.song
        if song.view.selected_track == track:
            song.view.selected_scene = song.scenes[scene_index]
        self._view_selected_clip_detail()

    def _handle_limitation_error_on_scene_creation(self):
        self.expect_dialog(MessageBoxText.SCENE_LIMIT_REACHED)