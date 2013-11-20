#Embedded file name: /Applications/Ableton Live 9 Standard.app/Contents/App-Resources/MIDI Remote Scripts/Livid_Base/Base.py
from __future__ import with_statement
import Live
import math
import sys
from _Tools.re import *
from itertools import imap, chain, starmap
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.NotifyingControlElement import NotifyingControlElement
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.SliderElement import SliderElement
from _Framework.TrackEQComponent import TrackEQComponent
from _Framework.TrackFilterComponent import TrackFilterComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.Layer import Layer
from _Mono_Framework.MonoButtonElement import *
from _Mono_Framework.MonoEncoderElement import MonoEncoderElement
from _Mono_Framework.MonoBridgeElement import MonoBridgeElement
from _Mono_Framework.MonoDeviceComponent import MonoDeviceComponent
from _Mono_Framework.ModDevices import *
from _Mono_Framework.Mod import *
import sys
import _Mono_Framework.modRemixNet as RemixNet
import _Mono_Framework.modOSC
from Push.Skin import *
from Push.SessionRecordingComponent import *
from Push.ClipCreator import ClipCreator
from Push.ViewControlComponent import ViewControlComponent
from Push.DrumGroupComponent import DrumGroupComponent
from Push.StepSeqComponent import StepSeqComponent
from Push.PlayheadElement import PlayheadElement
from Push.PlayheadComponent import PlayheadComponent
from Push.GridResolution import GridResolution
from Push.ConfigurableButtonElement import ConfigurableButtonElement
from Push.LoopSelectorComponent import LoopSelectorComponent
from Push.ComboElement import ComboElement, DoublePressElement, MultiElement, DoublePressContext
from Push.Actions import CreateInstrumentTrackComponent, CreateDefaultTrackComponent, CaptureAndInsertSceneComponent, DuplicateDetailClipComponent, DuplicateLoopComponent, SelectComponent, DeleteComponent, DeleteSelectedClipComponent, DeleteSelectedSceneComponent, CreateDeviceComponent
from Push.M4LInterfaceComponent import M4LInterfaceComponent
DIRS = [47,
 48,
 50,
 49]
_NOTENAMES = ['C',
 'Db',
 'D',
 'Eb',
 'E',
 'F',
 'Gb',
 'G',
 'Ab',
 'A',
 'Bb',
 'B']
NOTENAMES = [ _NOTENAMES[index % 12] + ' ' + str(int(index / 12)) for index in range(128) ]
SCALENAMES = None
SCALEABBREVS = None
from Map import *
_base_translations = {'0': 0,
 '1': 1,
 '2': 2,
 '3': 3,
 '4': 4,
 '5': 5,
 '6': 6,
 '7': 7,
 '8': 8,
 '9': 9,
 'A': 10,
 'B': 11,
 'C': 12,
 'D': 13,
 'E': 14,
 'F': 15,
 'G': 16,
 'H': 17,
 'I': 18,
 'J': 19,
 'K': 20,
 'L': 21,
 'M': 22,
 'N': 23,
 'O': 24,
 'P': 25,
 'Q': 26,
 'R': 27,
 'S': 28,
 'T': 29,
 'U': 30,
 'V': 31,
 'W': 32,
 'X': 33,
 'Y': 34,
 'Z': 35,
 'a': 10,
 'b': 11,
 'c': 12,
 'd': 13,
 'e': 14,
 'f': 15,
 'g': 16,
 'h': 17,
 'i': 18,
 'j': 19,
 'k': 20,
 'l': 21,
 'm': 22,
 'n': 23,
 'o': 24,
 'p': 25,
 'q': 26,
 'r': 27,
 's': 28,
 't': 29,
 'u': 30,
 'v': 31,
 'w': 32,
 'x': 33,
 'y': 34,
 'z': 35,
 '_': 39,
 '-': 42}
PAD_TRANSLATIONS = [[0, 0, 16],
 [1, 0, 17],
 [2, 0, 18],
 [3, 0, 19],
 [0, 1, 20],
 [1, 1, 21],
 [2, 1, 22],
 [3, 1, 23],
 [0, 2, 24],
 [1, 2, 25],
 [2, 2, 26],
 [3, 2, 27],
 [0, 3, 28],
 [1, 3, 29],
 [2, 3, 30],
 [3, 3, 31]]
FADER_COLORS = [96,
 124,
 108,
 120,
 116,
 100,
 104,
 112]
DEFAULT_MIDI_ASSIGNMENTS = {'mode': 'chromatic',
 'offset': 36,
 'vertoffset': 12,
 'scale': 'Chromatic',
 'drumoffset': 0,
 'split': False,
 'sequencer': True}
LAYERSPLASH = [63,
 69,
 70,
 65]
USERBUTTONMODE = (240, 0, 1, 97, 12, 66, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 247)
MIDIBUTTONMODE = (240, 0, 1, 97, 12, 66, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 247)
LIVEBUTTONMODE = (240, 0, 1, 97, 12, 66, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 247)
SPLITBUTTONMODE = (240, 0, 1, 97, 12, 66, 3, 3, 3, 3, 5, 5, 5, 5, 3, 3, 3, 3, 5, 5, 5, 5, 3, 3, 3, 3, 5, 5, 5, 5, 3, 3, 3, 3, 5, 5, 5, 5, 247)
STREAMINGON = (240, 0, 1, 97, 12, 62, 127, 247)
STREAMINGOFF = (240, 0, 1, 97, 12, 62, 0, 247)
LINKFUNCBUTTONS = (240, 0, 1, 97, 12, 68, 1, 247)
DISABLECAPFADERNOTES = (240, 0, 1, 97, 12, 69, 1, 247)
QUERYSURFACE = (240, 126, 127, 6, 1, 247)
CHANNELS = ['Ch. 2',
 'Ch. 3',
 'Ch. 4',
 'Ch. 5',
 'Ch. 6',
 'Ch. 7',
 'Ch. 8',
 'Ch. 9',
 'Ch. 10',
 'Ch. 11',
 'Ch. 12',
 'Ch. 13',
 'Ch. 14',
 'Ch. 15',
 'Ch. 16',
 'All Channels']
MODES = ['chromatic',
 'drumpad',
 'scale',
 'user']
INITIAL_SCROLLING_DELAY = 5
INTERVAL_SCROLLING_DELAY = 1
if SCALENAMES is None:
    SCALENAMES = [ scale for scale in sorted(SCALES.iterkeys()) ]
if SCALEABBREVS is None:
    SCALEABBREVS = []
MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_MSG_TYPES = (MIDI_NOTE_TYPE, MIDI_CC_TYPE, MIDI_PB_TYPE)
MIDI_NOTE_ON_STATUS = 144
MIDI_NOTE_OFF_STATUS = 128
MIDI_CC_STATUS = 176
MIDI_PB_STATUS = 224
_Q = Live.Song.Quantization
LAUNCH_QUANTIZATION = (_Q.q_quarter,
 _Q.q_half,
 _Q.q_bar,
 _Q.q_2_bars,
 _Q.q_4_bars,
 _Q.q_8_bars,
 _Q.q_8_bars,
 _Q.q_8_bars)

def is_device(device):
    return device is not None and isinstance(device, Live.Device.Device) and hasattr(device, 'name')


def make_pad_translations(chan):
    return tuple(((x % 4,
     int(x / 4),
     x + 16,
     chan) for x in range(16)))


class BaseSessionRecordingComponent(SessionRecordingComponent):

    def __init__(self, *a, **k):
        self._length_value = 1
        super(BaseSessionRecordingComponent, self).__init__(*a, **k)
        self._length_buttons = []

    def _get_selected_length(self):
        song = self.song()
        length = 2.0 ** LENGTH_VALUES[self._length_value]
        quant = LAUNCH_QUANTIZATION[LENGTH_VALUES[self._length_value]]
        length = length * song.signature_numerator / song.signature_denominator
        return (length, quant)

    def set_length_buttons(self, buttons):
        if buttons != self._length_buttons:
            for button in self._length_buttons:
                if button.value_has_listener(self._on_length_button):
                    button.remove_value_listener(self._on_length_button)

            if buttons == None:
                buttons = []
            self._length_buttons = buttons
            for button in self._length_buttons:
                button.add_value_listener(self._on_length_button, True)

            self.update_length_buttons()

    def _on_length_button(self, value, sender):
        if value > 0:
            self._length_value = self._length_buttons.index(sender)
            self.update_length_buttons()

    def update(self, *a, **k):
        super(BaseSessionRecordingComponent, self).update(*a, **k)
        if self.is_enabled():
            self.update_length_buttons()

    def update_length_buttons(self):
        for button in self._length_buttons:
            if self._length_buttons.index(button) == self._length_value:
                button.turn_on()
            else:
                button.turn_off()


class BlockingMonoButtonElement(MonoButtonElement):

    def __init__(self, *a, **k):
        super(BlockingMonoButtonElement, self).__init__(*a, **k)
        self._is_held = False
        self._held_value = 1
        self.display_press = False
        self._last_flash = 0
        self.scale_color = 0
        self._skin_colors = {'NoteEditor.Step.Low': 3,
         'NoteEditor.Step.High': 1,
         'NoteEditor.Step.Full': 2,
         'NoteEditor.Step.Muted': 3,
         'NoteEditor.Step.Empty': 0,
         'NoteEditor.StepLow': 3,
         'NoteEditor.StepHigh': 1,
         'NoteEditor.StepFull': 2,
         'NoteEditor.StepMuted': 3,
         'NoteEditor.StepEmpty': 0,
         'NoteEditor.StepEditing.High': 6,
         'NoteEditor.StepEmptyBase': 0,
         'NoteEditor.StepEmptyScale': 0,
         'NoteEditor.StepDisabled': 0,
         'NoteEditor.Playhead': 2,
         'NoteEditor.StepSelected': 6,
         'NoteEditor.PlayheadRecord': 5,
         'NoteEditor.QuantizationSelected': 5,
         'NoteEditor.QuantizationUnselected': 4,
         'LoopSelector.Playhead': 2,
         'LoopSelector.OutsideLoop': 7,
         'LoopSelector.InsideLoopStartBar': 3,
         'LoopSelector.SelectedPage': 1,
         'LoopSelector.InsideLoop': 3,
         'LoopSelector.PlayheadRecord': 5,
         'DrumGroup.PadAction': 1,
         'DrumGroup.PadFilled': 6,
         'DrumGroup.PadSelected': 1,
         'DrumGroup.PadEmpty': 0,
         'DrumGroup.PadMuted': 2,
         'DrumGroup.PadSoloed': 3,
         'DrumGroup.PadMutedSelected': 7,
         'DrumGroup.PadSoloedSelected': 7}

    def press_flash(self, value, force = False):
        raise value != None or AssertionError
        raise isinstance(value, int) or AssertionError
        raise value in range(128) or AssertionError
        if self.display_press and (value is not self._last_flash or force):
            data_byte1 = self._original_identifier
            if value == 0:
                if self.scale_color is 127:
                    data_byte2 = COLOR_MAP[-1]
                elif self.scale_color is 0:
                    data_byte2 = 0
                else:
                    data_byte2 = COLOR_MAP[max(0, (self.scale_color - 1) % 7)]
            else:
                data_byte2 = 1
            status_byte = self._original_channel
            status_byte += 144
            self.send_midi((status_byte, data_byte1, data_byte2))
            self._last_flash = value

    def set_light(self, value):
        if value is True:
            self.send_value(self._on_value)
        elif value is False:
            self.send_value(self._off_value)
        elif value in self._skin_colors.keys():
            self.send_value(self._skin_colors[value])
        else:
            self._script.log_message('skin color: ' + str(value))
            self.send_value(len(value))

    def set_on_off_values(self, on_value, off_value):
        if on_value not in range(128):
            if on_value in self._skin_colors.keys():
                on_value = self._skin_colors[on_value]
            else:
                self._script.log_message('on_value skin color: ' + str(on_value))
                on_value = len(on_value)
        if off_value not in range(128):
            if off_value in self._skin_colors.keys():
                off_value = self._skin_colors[off_value]
            else:
                self._script.log_message('off_value skin color: ' + str(off_value))
                off_value = len(off_value)
        super(BlockingMonoButtonElement, self).set_on_off_values(on_value, off_value)


class BaseMixerComponent(MixerComponent):

    def __init__(self, script, *a, **k):
        super(BaseMixerComponent, self).__init__(*a, **k)
        self._script = script
        self._held = None
        for strip in self._channel_strips:
            strip._select_value = self._strip_select_value(strip)

    def shifted(self):
        return self._held is not None

    def _strip_select_value(self, strip):

        def _select_value(value):
            ChannelStripComponent._select_value(strip, value)
            if value is not 0:
                self._held = strip
                self._script._select_update(self._held)
            elif self._held is strip:
                self._held = None
                self._script._select_update(self._held)

        return _select_value

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def deassign_all(self):
        self.set_bank_buttons(None, None)
        self.set_select_buttons(None, None)
        self.set_prehear_volume_control(None)
        self.set_crossfader_control(None)
        for component in self._sub_components:
            if isinstance(component, ChannelStripComponent):
                component.set_pan_control(None)
                component.set_volume_control(None)
                component.set_select_button(None)
                if component in self._channel_strips or component in self._return_strips:
                    component.set_mute_button(None)
                    component.set_send_controls(None)
                    component.set_solo_button(None)
                    component.set_shift_button(None)
                    component.set_crossfade_toggle(None)
                    if component in self._channel_strips:
                        component.set_arm_button(None)


class BaseModeSelector(ModeSelectorComponent):

    def __init__(self, script):
        super(BaseModeSelector, self).__init__()
        self._held = None
        self._script = script
        self._set_protected_mode_index(0)

    def number_of_modes(self):
        return 4

    def _mode_value(self, value, sender):
        if sender is not self._held:
            if not self._script.pad_held() or sender in (self._modes_buttons[1], self._modes_buttons[2]):
                if value:
                    super(BaseModeSelector, self)._mode_value(value, sender)
                    self._held = sender
                    self._script._shift_update(self._mode_index, self._held is not None)
                    self._script.schedule_message(3, self._script._check_mode_shift, self._held)
        elif value is 0:
            self._held = None
            self._script._shift_update(self._mode_index, self._held is not None)

    def update(self):
        if self._is_enabled:
            buttons = self._modes_buttons
            for index in range(len(buttons)):
                if index == self._mode_index:
                    buttons[index].turn_on(True)
                else:
                    buttons[index].turn_off(True)

    def is_shifted(self):
        return self._held is not None


class BaseUserModeSelector(ModeSelectorComponent):

    def __init__(self, script):
        super(BaseUserModeSelector, self).__init__()
        self._held = None
        self._script = script
        self._set_protected_mode_index(0)

    def number_of_modes(self):
        return 8

    def _mode_value(self, value, sender):
        if self._is_enabled:
            if sender is not self._held:
                super(BaseUserModeSelector, self)._mode_value(value, sender)
                self._held = sender
            elif value is 0:
                self._held = None
            self._script._user_shift_update(self._mode_index, self._held is not None)

    def update(self):
        if self._is_enabled:
            buttons = self._modes_buttons
            for index in range(len(buttons)):
                if index == self._mode_index:
                    buttons[index].turn_on(True)
                else:
                    buttons[index].turn_off(True)

    def is_shifted(self):
        return self._held is not None


class BaseMidiModeSelector(ModeSelectorComponent):

    def __init__(self, callback):
        super(BaseMidiModeSelector, self).__init__()
        self._report_mode = callback
        self._set_protected_mode_index(0)

    def number_of_modes(self):
        return 2

    def _mode_value(self, value, sender):
        if self._is_enabled:
            super(BaseMidiModeSelector, self)._mode_value(value, sender)
            self._report_mode(self._mode_index)

    def update(self):
        if self._is_enabled:
            for index in range(len(self._modes_buttons)):
                if self._mode_index == index:
                    self._modes_buttons[index].turn_on(True)
                else:
                    self._modes_buttons[index].turn_off(True)


class BaseSplitModeSelector(ModeSelectorComponent):

    def __init__(self, callback):
        super(BaseSplitModeSelector, self).__init__()
        self._report_mode = callback
        self._modes_buttons = []
        self._set_protected_mode_index(0)

    def number_of_modes(self):
        return 2

    def _mode_value(self, value, sender):
        if self._is_enabled:
            super(BaseSplitModeSelector, self)._mode_value(value, sender)
            self._report_mode(self._mode_index)

    def _toggle_value(self, value):
        if self._is_enabled:
            super(BaseSplitModeSelector, self)._toggle_value(value)
            self._report_mode(self._mode_index)

    def update(self):
        if self._is_enabled:
            if len(self._modes_buttons) > 0:
                for index in range(len(self._modes_buttons)):
                    if self._mode_index == index:
                        self._modes_buttons[index].turn_on(True)
                    else:
                        self._modes_buttons[index].turn_off(True)

            if self._mode_toggle is not None:
                if self._mode_index > 0:
                    self._mode_toggle.turn_on(True)
                else:
                    self._mode_toggle.turn_off(True)


class BaseSequencerModeSelector(ModeSelectorComponent):

    def __init__(self, callback):
        super(BaseSequencerModeSelector, self).__init__()
        self._report_mode = callback
        self._modes_buttons = []
        self._set_protected_mode_index(0)

    def number_of_modes(self):
        return 2

    def _mode_value(self, value, sender):
        if self._is_enabled:
            super(BaseSequencerModeSelector, self)._mode_value(value, sender)
            self._report_mode(self._mode_index)

    def _toggle_value(self, value):
        if self._is_enabled:
            super(BaseSequencerModeSelector, self)._toggle_value(value)
            self._report_mode(self._mode_index)

    def update(self):
        if self._is_enabled:
            if len(self._modes_buttons) > 0:
                for index in range(len(self._modes_buttons)):
                    if self._mode_index == index:
                        self._modes_buttons[index].turn_on(True)
                    else:
                        self._modes_buttons[index].turn_off(True)

            if self._mode_toggle is not None:
                if self._mode_index > 0:
                    self._mode_toggle.turn_on(True)
                else:
                    self._mode_toggle.turn_off(True)


class BaseSessionComponent(SessionComponent):

    def __init__(self, num_tracks, num_scenes, script):
        super(BaseSessionComponent, self).__init__(num_tracks, num_scenes)
        self._shifted = False
        self._script = script

    def deassign_all(self):
        self._shifted = False
        self.set_scene_bank_buttons(None, None)
        self.set_track_bank_buttons(None, None)
        self.set_stop_all_clips_button(None)
        self.set_stop_track_clip_buttons(None)
        self.set_select_buttons(None, None)
        for scene in self._scenes:
            scene.set_launch_button(None)
            for slot in scene._clip_slots:
                slot.set_launch_button(None)

    def _bank_up_value(self, value):
        if not value in range(128):
            raise AssertionError
            if not self._bank_up_button != None:
                raise AssertionError
                if self.is_enabled():
                    button_is_momentary = self._bank_up_button.is_momentary()
                    if button_is_momentary:
                        self._scroll_up_ticks_delay = value != 0 and INITIAL_SCROLLING_DELAY
                    else:
                        self._scroll_up_ticks_delay = -1
                not self._is_scrolling() and (value is not 0 or not button_is_momentary) and self.set_offsets(self._track_offset, self._scene_offset + (1 + self._shifted * 3))

    def _bank_down_value(self, value):
        if not value in range(128):
            raise AssertionError
            if not self._bank_down_button != None:
                raise AssertionError
                if self.is_enabled():
                    button_is_momentary = self._bank_down_button.is_momentary()
                    if button_is_momentary:
                        self._scroll_down_ticks_delay = value != 0 and INITIAL_SCROLLING_DELAY
                    else:
                        self._scroll_down_ticks_delay = -1
                not self._is_scrolling() and (value is not 0 or not button_is_momentary) and self.set_offsets(self._track_offset, max(0, self._scene_offset - (1 + self._shifted * 3)))

    def _bank_right_value(self, value):
        if not value in range(128):
            raise AssertionError
            if not self._bank_right_button != None:
                raise AssertionError
                if self.is_enabled():
                    button_is_momentary = self._bank_right_button.is_momentary()
                    if button_is_momentary:
                        self._scroll_right_ticks_delay = value != 0 and INITIAL_SCROLLING_DELAY
                    else:
                        self._scroll_right_ticks_delay = -1
                not self._is_scrolling() and (value is not 0 or not button_is_momentary) and self.set_offsets(self._track_offset + (1 + self._shifted * 7), self._scene_offset)

    def _bank_left_value(self, value):
        if not isinstance(value, int):
            raise AssertionError
            if not self._bank_left_button != None:
                raise AssertionError
                if self.is_enabled():
                    button_is_momentary = self._bank_left_button.is_momentary()
                    if button_is_momentary:
                        self._scroll_left_ticks_delay = value != 0 and INITIAL_SCROLLING_DELAY
                    else:
                        self._scroll_left_ticks_delay = -1
                not self._is_scrolling() and (value is not 0 or not button_is_momentary) and self.set_offsets(max(0, self._track_offset - (1 + self._shifted * 7)), self._scene_offset)


class BaseDeviceComponent(DeviceComponent):

    def __init__(self, script, *a, **k):
        super(BaseDeviceComponent, self).__init__(*a, **k)
        self._script = script

    def deassign_all(self):
        self.set_parameter_controls(None)
        self.set_bank_nav_buttons(None, None)
        self.set_bank_buttons(None)

    def set_parameter_controls(self, controls):
        raise controls is None or isinstance(controls, tuple) or AssertionError
        if self._device != None and self._parameter_controls != None:
            for control in self._parameter_controls:
                control.release_parameter()

        if controls is not None:
            for control in controls:
                raise control != None or AssertionError
                raise isinstance(control, EncoderElement) or AssertionError

        self._parameter_controls = controls
        self.update()

    def _is_banking_enabled(self):
        return True

    def _on_device_bank_changed(self, *a, **k):
        super(BaseDeviceComponent, self)._on_device_bank_changed(*a, **k)
        self._script._on_device_bank_changed()


class DeviceNavigator(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Component that can toggle the device chain- and clip view of the selected track '

    def __init__(self, device_component, mixer, script):
        super(DeviceNavigator, self).__init__()
        self._prev_button = None
        self._next_button = None
        self._enter_button = None
        self._exit_button = None
        self._chain_prev_button = None
        self._chain_next_button = None
        self._device = device_component
        self._mixer = mixer
        self._script = script

    def deassign_all(self):
        self.set_nav_buttons(None, None)
        self.set_layer_buttons(None, None)
        self.set_chain_nav_buttons(None, None)

    def set_nav_buttons(self, prev_button, next_button):
        identify_sender = True
        if self._prev_button != None:
            if self._prev_button.value_has_listener(self._nav_value):
                self._prev_button.remove_value_listener(self._nav_value)
        self._prev_button = prev_button
        if self._prev_button != None:
            self._prev_button.add_value_listener(self._nav_value, identify_sender)
        if self._next_button != None:
            if self._next_button.value_has_listener(self._nav_value):
                self._next_button.remove_value_listener(self._nav_value)
        self._next_button = next_button
        if self._next_button != None:
            self._next_button.add_value_listener(self._nav_value, identify_sender)
        self.update()

    def set_chain_nav_buttons(self, chain_prev_button, chain_next_button):
        identify_sender = True
        if self._chain_prev_button != None:
            if self._chain_prev_button.value_has_listener(self._chain_nav_value):
                self._chain_prev_button.remove_value_listener(self._chain_nav_value)
        self._chain_prev_button = chain_prev_button
        if self._chain_prev_button != None:
            self._chain_prev_button.add_value_listener(self._chain_nav_value, identify_sender)
        if self._chain_next_button != None:
            if self._chain_next_button.value_has_listener(self._chain_nav_value):
                self._chain_next_button.remove_value_listener(self._chain_nav_value)
        self._chain_next_button = chain_next_button
        if self._chain_next_button != None:
            self._chain_next_button.add_value_listener(self._chain_nav_value, identify_sender)
        self.update()

    def set_layer_buttons(self, enter_button, exit_button):
        identify_sender = True
        if self._enter_button != None:
            if self._enter_button.value_has_listener(self._enter_value):
                self._enter_button.remove_value_listener(self._enter_value)
        self._enter_button = enter_button
        if self._enter_button != None:
            self._enter_button.add_value_listener(self._enter_value)
        if self._exit_button != None:
            if self._exit_button.value_has_listener(self._exit_value):
                self._exit_button.remove_value_listener(self._exit_value)
        self._exit_button = exit_button
        if self._exit_button != None:
            self._exit_button.add_value_listener(self._exit_value)
        self.update()

    def update(self):
        track = self._mixer.selected_strip()._track
        if self._device._device and isinstance(self._device._device.canonical_parent, Live.Chain.Chain):
            track = self._device._device.canonical_parent
        if track != None:
            if self._prev_button is not None:
                if self._device._device:
                    if len(track.devices) > 0:
                        if self._device._device in track.devices and [ t for t in track.devices ].index(self._device._device) > 0:
                            self._prev_button.turn_on()
                            self._prev_button.turn_off()
                        if self._next_button is not None:
                            if self._device._device:
                                if len(track.devices) > 0:
                                    if self._device._device in track.devices and [ t for t in track.devices ].index(self._device._device) < len(track.devices) - 1:
                                        self._next_button.turn_on()
                                        self._next_button.turn_off()
                                    if self._chain_prev_button is not None:
                                        if self._device._device and isinstance(self._device._device.canonical_parent, Live.Chain.Chain):
                                            parent_chain = self._device._device.canonical_parent
                                            parent = parent_chain.canonical_parent
                                            len(parent.chains) > 0 and parent_chain in parent.chains and [ c for c in parent.chains ].index(parent_chain) > 0 and self._chain_prev_button.turn_on()
                                            self._chain_prev_button.turn_off()
                                    parent_chain = self._chain_next_button is not None and self._device._device and isinstance(self._device._device.canonical_parent, Live.Chain.Chain) and self._device._device.canonical_parent
                                    parent = parent_chain.canonical_parent
                                    len(parent.chains) > 0 and parent_chain in parent.chains and [ c for c in parent.chains ].index(parent_chain) < len(parent.chains) - 1 and self._chain_next_button.turn_on()
                                    self._chain_next_button.turn_off()
                            self._enter_button is not None and self._device._device and self._device._device.can_have_chains and len(self._device._device.chains) and self._enter_button.turn_on()
                        else:
                            self._enter_button.turn_off()
                    self._exit_button is not None and self._device._device and self._device._device.canonical_parent and isinstance(self._device._device.canonical_parent, Live.Chain.Chain) and self._exit_button.turn_on()
                else:
                    self._exit_button.turn_off()

    def _nav_value(self, value, sender):
        if self.is_enabled() and (not sender.is_momentary() or value != 0):
            track = self._mixer.selected_strip()._track
            if self._device._device and isinstance(self._device._device.canonical_parent, Live.Chain.Chain):
                track = self._device._device.canonical_parent
            if track != None:
                if sender == self._prev_button:
                    if self._device._device and self._device._device in track.devices:
                        device = track.devices[min(len(track.devices) - 1, max(0, [ item for item in track.devices ].index(self._device._device) - 1))]
                        self._script.set_appointed_device(device)
                        self.song().view.select_device(device)
                elif sender == self._next_button:
                    if self._device._device and self._device._device in track.devices:
                        device = track.devices[min(len(track.devices) - 1, max(0, [ item for item in track.devices ].index(self._device._device) + 1))]
                        self._script.set_appointed_device(device)
                        self.song().view.select_device(device)

    def _chain_nav_value(self, value, sender):
        if self.is_enabled() and (not sender.is_momentary() or value != 0):
            track = self._mixer.selected_strip()._track
            if track != None:
                if sender == self._chain_prev_button:
                    if self._device._device and isinstance(self._device._device.canonical_parent, Live.Chain.Chain):
                        parent_chain = self._device._device.canonical_parent
                        parent = parent_chain.canonical_parent
                        device = parent.chains[min(len(parent.chains) - 1, max(0, [ item for item in parent.chains ].index(parent_chain) - 1))].devices[0]
                        self._script.set_appointed_device(device)
                        self.song().view.select_device(device)
                elif sender == self._chain_next_button:
                    if self._device._device and isinstance(self._device._device.canonical_parent, Live.Chain.Chain):
                        parent_chain = self._device._device.canonical_parent
                        parent = parent_chain.canonical_parent
                        device = parent.chains[min(len(parent.chains) - 1, max(0, [ item for item in parent.chains ].index(parent_chain) + 1))].devices[0]
                        self._script.set_appointed_device(device)
                        self.song().view.select_device(device)

    def _enter_value(self, value):
        if value:
            if self._device._device and self._device._device.can_have_chains and len(self._device._device.chains):
                device = self._device._device.chains[0].devices[0]
                self._script.set_appointed_device(device)
                self.song().view.select_device(device)

    def _exit_value(self, value):
        if value:
            if self._device._device and self._device._device.canonical_parent and isinstance(self._device._device.canonical_parent, Live.Chain.Chain):
                device = self._device._device.canonical_parent.canonical_parent
                self._script.set_appointed_device(device)
                self.song().view.select_device(device)

    def disconnect(self):
        if self._prev_button != None:
            if self._prev_button.value_has_listener(self._nav_value):
                self._prev_button.remove_value_listener(self._nav_value)
        if self._next_button != None:
            if self._next_button.value_has_listener(self._nav_value):
                self._next_button.remove_value_listener(self._nav_value)

    def _find_track(self, obj):
        if type(obj.canonical_parent) == type(self.song().tracks[0]):
            return obj.canonical_parent
        elif type(obj.canonical_parent) == type(None) or type(obj.canonical_parent) == type(self.song()):
            return
        else:
            return self.find_track(obj.canonical_parent)

    def on_enabled_changed(self):
        pass


class ScaleModeComponent(ModeSelectorComponent):
    __module__ = __name__
    __doc__ = ' Class for switching between modes, handle several functions with few controls '

    def __init__(self, script):
        super(ScaleModeComponent, self).__init__()
        self._script = script
        self._set_protected_mode_index(0)

    def set_mode_buttons(self, buttons):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                raise isinstance(button, MonoButtonElement) or AssertionError
                identify_sender = True
                button.add_value_listener(self._mode_value, identify_sender)
                self._modes_buttons.append(button)

            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()

    def set_mode_toggle(self, button):
        if not (button == None or isinstance(button, MonoButtonElement)):
            raise AssertionError
            if self._mode_toggle != None:
                self._mode_toggle.remove_value_listener(self._toggle_value)
            self._mode_toggle = button
            self._mode_toggle != None and self._mode_toggle.add_value_listener(self._toggle_value)

    def number_of_modes(self):
        return 8

    def update(self):
        if self.is_enabled():
            scales = SCALES.keys()
            self._script._offsets['scale'] = scales[self._mode_index % len(scales)]
            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()


class ScrollingOffsetComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Class for handling held buttons for continued value changes '

    def __init__(self, callback):
        super(ScrollingOffsetComponent, self).__init__()
        self._report_change = callback
        self._offset = 0
        self._maximum = 127
        self._minimum = 0
        self._shifted = False
        self._shifted_value = 11
        self._scroll_up_ticks_delay = -1
        self._scroll_down_ticks_delay = -1
        self._scroll_up_button = None
        self._scroll_down_button = None
        self._shift_button = None
        self._shift_is_momentary = True
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        if self._scroll_up_button != None:
            self._scroll_up_button.remove_value_listener(self._scroll_up_value)
            self._scroll_up_button = None
        if self._scroll_down_button != None:
            self._scroll_down_button.remove_value_listener(self._scroll_down_value)
            self._scroll_down_button = None

    def on_enabled_changed(self):
        self._scroll_up_ticks_delay = -1
        self._scroll_down_ticks_delay = -1
        self.update()

    def set_offset_change_buttons(self, up_button, down_button):
        if not (up_button == None or isinstance(up_button, ButtonElement)):
            raise AssertionError
            if not (down_button == None or isinstance(down_button, ButtonElement)):
                raise AssertionError
                do_update = False
                if up_button is not self._scroll_up_button:
                    do_update = True
                    if self._scroll_up_button != None:
                        self._scroll_up_button.remove_value_listener(self._scroll_up_value)
                    self._scroll_up_button = up_button
                    if self._scroll_up_button != None:
                        self._scroll_up_button.add_value_listener(self._scroll_up_value)
                if down_button is not self._scroll_down_button:
                    do_update = True
                    if self._scroll_down_button != None:
                        self._scroll_down_button.remove_value_listener(self._scroll_down_value)
                    self._scroll_down_button = down_button
                    self._scroll_down_button != None and self._scroll_down_button.add_value_listener(self._scroll_down_value)
            do_update and self.update()

    def _scroll_up_value(self, value):
        if not value in range(128):
            raise AssertionError
            if not self._scroll_up_button != None:
                raise AssertionError
                if self.is_enabled():
                    button_is_momentary = self._scroll_up_button.is_momentary()
                    if button_is_momentary:
                        self._scroll_up_ticks_delay = value != 0 and INITIAL_SCROLLING_DELAY
                    else:
                        self._scroll_up_ticks_delay = -1
                self._offset = not self._is_scrolling() and (value is not 0 or not button_is_momentary) and max(self._minimum, min(self._maximum, self._offset + (1 + self._shifted * self._shifted_value)))
                self.update()
                self._report_change(self._offset)

    def _scroll_down_value(self, value):
        if not value in range(128):
            raise AssertionError
            if not self._scroll_down_button != None:
                raise AssertionError
                if self.is_enabled():
                    button_is_momentary = self._scroll_down_button.is_momentary()
                    if button_is_momentary:
                        self._scroll_down_ticks_delay = value != 0 and INITIAL_SCROLLING_DELAY
                    else:
                        self._scroll_down_ticks_delay = -1
                self._offset = not self._is_scrolling() and (value is not 0 or not button_is_momentary) and max(self._minimum, min(self._maximum, self._offset - (1 + self._shifted * self._shifted_value)))
                self.update()
                self._report_change(self._offset)

    def set_shift_button(self, shift_button):
        if self._shift_button != None:
            if self._shift_button.value_has_listener(self._shift_value):
                self._shift_button.remove_value_listener(self._shift_value)
        self._shift_button = shift_button
        if self._shift_button != None:
            self._shift_button.add_value_listener(self._shift_value)
            self.update()

    def _shift_value(self, value):
        if self._shift_is_momentary:
            self._shifted = value > 0
            self.update()
        elif value > 0:
            self._shifted = not self._shifted
            self.update()

    def _on_timer(self):
        if self.is_enabled():
            scroll_delays = [self._scroll_up_ticks_delay, self._scroll_down_ticks_delay]
            if scroll_delays.count(-1) < 2:
                offset_increment = 0
                if self._scroll_down_ticks_delay > -1:
                    if self._is_scrolling():
                        offset_increment -= 1
                        self._scroll_down_ticks_delay = INTERVAL_SCROLLING_DELAY
                    self._scroll_down_ticks_delay -= 1
                if self._scroll_up_ticks_delay > -1:
                    if self._is_scrolling():
                        offset_increment += 1
                        self._scroll_up_ticks_delay = INTERVAL_SCROLLING_DELAY
                    self._scroll_up_ticks_delay -= 1
                new_offset = max(self._minimum, min(self._maximum, self._offset + offset_increment))
                if new_offset != self._offset:
                    self._offset = new_offset
                    self.update()
                    self._report_change(self._offset)

    def _is_scrolling(self):
        return 0 in (self._scroll_up_ticks_delay, self._scroll_down_ticks_delay)

    def update(self):
        if self._scroll_down_button != None:
            if self._offset > self._minimum:
                self._scroll_down_button.turn_on(True)
            else:
                self._scroll_down_button.turn_off(True)
        if self._scroll_up_button != None:
            if self._offset < self._maximum:
                self._scroll_up_button.turn_on(True)
            else:
                self._scroll_up_button.turn_off(True)
        if self._shift_button != None:
            if self._shifted:
                self._shift_button.turn_on(True)
            else:
                self._shift_button.turn_off(True)

    def deassign_all(self):
        self.set_offset_change_buttons(None, None)
        self.set_shift_button(None)
        self.on_enabled_changed()


class BaseFaderArray(Array):

    def __init__(self, active_handlers, name, size):
        self._active_handlers = active_handlers
        self._name = name
        self._cell = [ StoredElement(self._name + '_' + str(num), _num=num, _mode=1, _value=7) for num in range(size) ]

    def value(self, num, value = 0):
        element = self._cell[num]
        element._value = value % 8
        self.update_element(element)

    def mode(self, num, mode = 0):
        element = self._cell[num]
        element._mode = mode % 4
        self.update_element(element)

    def update_element(self, element):
        for handler in self._active_handlers():
            handler.receive_address(self._name, element._num, FADER_COLORS[element._value] + element._mode)


class BaseGrid(Grid):

    def __init__(self, active_handlers, name, width, height):
        self._active_handlers = active_handlers
        self._name = name
        self._cell = [ [ StoredElement(active_handlers, _name=self._name + '_' + str(x) + '_' + str(y), _x=x, _y=y, _id=-1, _channel=-1) for y in range(height) ] for x in range(width) ]

    def restore(self):
        for column in self._cell:
            for element in column:
                self.update_element(element)
                for handler in self._active_handlers():
                    handler.receive_address(self._name, element._x, element._y, element, True)

    def identifier(self, x, y, identifier = -1):
        element = self._cell[x][y]
        element._id = min(127, max(-1, identifier))
        for handler in self._active_handlers():
            handler.receive_address(self._name, element._x, element._y, element, True)

    def channel(self, x, y, channel = -1):
        element = self._cell[x][y]
        element._channel = min(15, max(-1, channel))
        for handler in self._active_handlers():
            handler.receive_address(self._name, element._x, element._y, element, True)


class BaseModHandler(ModHandler):

    def __init__(self, *a, **k):
        super(BaseModHandler, self).__init__(*a, **k)
        self._base_grid = None
        self._base_grid_CC = None
        self._keys = None
        self._shift = None
        self._alt = None
        self._fader_color_override = False
        self._receive_methods = {'grid': self._receive_grid,
         'base_grid': self._receive_base_grid,
         'key': self._receive_key,
         'base_fader': self._receive_base_fader,
         'shift': self._receive_shift,
         'alt': self._receive_alt}
        self._shifted = False

    def _register_addresses(self, client):
        if 'base_grid' not in client._addresses:
            client._addresses['base_grid'] = BaseGrid(client.active_handlers, 'base_grid', 8, 4)
        if 'key' not in client._addresses:
            client._addresses['key'] = Array(client.active_handlers, 'key', 8)
        if 'base_fader' not in client._addresses:
            client._addresses['base_fader'] = BaseFaderArray(client.active_handlers, 'base_fader', 8)
        if 'shift' not in client._addresses:
            client._addresses['shift'] = StoredElement(client.active_handlers, _name='shift')
        if 'alt' not in client._addresses:
            client._addresses['alt'] = StoredElement(client.active_handlers, _name='alt')

    def _receive_base_grid(self, x, y, value, is_id = False):
        if self._base_grid is not None:
            if is_id:
                button = self._base_grid.get_button(x, y)
                if value._id is -1 and value._channel is -1:
                    button.use_default_message()
                    button.set_enabled(True)
                else:
                    identifier = value._id
                    if identifier < 0:
                        identifier = button._original_identifier
                    channel = value._channel
                    if channel < 0:
                        channel = button._original_channel
                    button.set_identifier(identifier)
                    button.set_channel(channel)
                    button.set_enabled(False)
            else:
                self._base_grid.send_value(x, y, value, True)

    def _receive_key(self, x, value):
        if self._keys is not None:
            self._keys.send_value(x, 0, value, True)

    def _receive_base_fader(self, num, value):
        if self._fader_color_override:
            self._script._send_midi((191, num + 10, value))

    def _receive_shift(self, value):
        pass

    def _receive_alt(self, value):
        if self._alt is not None:
            self._alt.send_value(value)

    def _receive_grid(self, x, y, value, is_id = False):
        if self._base_grid is not None:
            if x - self.x_offset in range(8) and y - self.y_offset in range(4):
                self._base_grid.send_value(x - self.x_offset, y - self.y_offset, value)

    def _assign_base_grid(self, grid):
        self._base_grid = grid
        self._base_grid_value.subject = self._base_grid

    def _assign_base_grid_CC(self, grid):
        self._base_grid_CC = grid
        self._base_grid_CC_value.subject = self._base_grid_CC

    def _assign_keys(self, keys):
        self._keys = keys
        self._keys_value.subject = self._keys

    def set_shift_button(self, button):
        self._shift = button
        self._shift_value.subject = self._shift

    def set_alt_button(self, button):
        self._alt = button
        self._alt_value.subject = self._alt

    @subject_slot('value')
    def _keys_value(self, value, x, y, *a, **k):
        if self._active_mod:
            self._active_mod.send('key', x, value)

    @subject_slot('value')
    def _base_grid_value(self, value, x, y, *a, **k):
        if self._active_mod:
            if self._active_mod.legacy:
                if self._shift_value.subject.is_pressed():
                    if value > 0 and x in range(3, 5) and y in range(0, 4):
                        self.set_offset((x - 3) * 8, y * 4)
                else:
                    self._active_mod.send('grid', x + self.x_offset, y + self.y_offset, value)
            else:
                self._active_mod.send('base_grid', x, y, value)

    @subject_slot('value')
    def _base_grid_CC_value(self, value, x, y, *a, **k):
        if self._active_mod:
            if self._active_mod.legacy:
                self._active_mod.send('grid_CC', x + self.x_offset, y + self.y_offset, value)
            else:
                self._active_mod.send('base_grid_CC', x, y, value)

    @subject_slot('value')
    def _shift_value(self, value, *a, **k):
        if self._active_mod:
            self._active_mod.send('shift', value)
            if self._active_mod.legacy:
                self._display_nav_box()

    @subject_slot('value')
    def _alt_value(self, value, *a, **k):
        if self._active_mod:
            self._active_mod.send('alt', value)

    def _display_nav_box(self):
        if self._base_grid_value.subject:
            if self._shift_value.subject and self._shift_value.subject.is_pressed():
                for column in range(2):
                    for row in range(4):
                        if column == int(self.x_offset / 8) and row == int(self.y_offset / 4):
                            self._base_grid_value.subject.get_button(column + 3, row).send_value(self.navbox_selected)
                        else:
                            self._base_grid_value.subject.get_button(column + 3, row).send_value(self.navbox_unselected)

    def update(self, *a, **k):
        if self._active_mod:
            if self._active_mod.legacy and self._shift_value.subject and self._shift_value.subject.is_pressed():
                self._display_nav_box()
            else:
                self._active_mod.restore()
        else:
            if self._base_grid_value.subject is not None:
                self._base_grid_value.subject.reset()
            if self._keys_value.subject is not None:
                self._keys_value.subject.reset()


class Base(ControlSurface):
    __module__ = __name__
    __doc__ = ' Base controller script '

    def __init__(self, c_instance):
        super(Base, self).__init__(c_instance)
        self._connected = False
        self._host_name = 'Base'
        self._color_type = 'OhmRGB'
        self.monomodular = None
        self.oscServer = None
        self.log_message('<<<<<<<<<<<<<<<<<= Base log opened =>>>>>>>>>>>>>>>>>>>>>')
        self._rgb = 0
        self._timer = 0
        self._current_nav_buttons = []
        self.flash_status = 1
        self._clutch_device_selection = False
        self._touched = 0
        self._update_linked_device_selection = None
        self._offsets = [ {'offset': DEFAULT_OFFSET,
         'vertoffset': DEFAULT_VERTOFFSET,
         'drumoffset': DEFAULT_DRUMOFFSET,
         'scale': DEFAULT_SCALE,
         'split': DEFAULT_SPLIT,
         'sequencer': True} for index in range(16) ]
        self._device_offsets = {}
        self._last_selected_track = None
        self._last_selected_track_arm = False
        self._last_pad_stream = [ 0 for i in range(0, 32) ]
        self._layer = 0
        self._user_layer = 0
        self._layers = [self._set_layer0,
         self._set_layer1,
         self._set_layer2,
         self._set_layer3]
        with self.component_guard():
            self.set_pad_translations(make_pad_translations(15))
            self._setup_monobridge()
            if OSC_TRANSMIT:
                self._setup_OSC_layer()
            self._setup_controls()
            self._setup_mixer_control()
            self._setup_session_control()
            self._setup_transport_control()
            self._setup_selected_session_control()
            self._setup_device_control()
            self._setup_mode_select()
            self._setup_user_mode_select()
            self._setup_midi_mode_select()
            self._setup_split_mode_select()
            self._setup_sequencer_mode_select()
            self._setup_offset_component()
            self._setup_vertical_offset_component()
            self._setup_scale_offset_component()
            self._setup_session_recording_component()
            self._setup_m4l_interface()
            self._setup_drumgroup()
            self._setup_step_sequencer()
            self._device.add_device_listener(self._on_new_device_set)
            self.set_feedback_channels(range(14, 15))
        self.schedule_message(3, self._check_connection)

    def _initialize_hardware(self):
        self._send_midi(STREAMINGON)
        self._send_midi(LINKFUNCBUTTONS)
        self._send_midi(DISABLECAPFADERNOTES)
        self._send_midi((191, 122, 64))
        self._layers[0]()

    def _check_connection(self):
        if not self._connected:
            self._send_midi(QUERYSURFACE)
            self.schedule_message(100, self._check_connection)

    def _setup_monobridge(self):
        self._monobridge = MonoBridgeElement(self)
        self._monobridge.name = 'MonoBridge'

    def _setup_controls(self):
        is_momentary = True
        self._fader = [ MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, BASE_TOUCHSTRIPS[index], Live.MidiMap.MapMode.absolute, 'Fader_' + str(index), index, self) for index in range(9) ]
        for fader in self._fader:
            fader._mapping_feedback_delay = -1

        self._button = [ MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, BASE_BUTTONS[index], 'Button_' + str(index), self) for index in range(8) ]
        self._pad = [ BlockingMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, BASE_PADS[index], 'Pad_' + str(index), self) for index in range(32) ]
        self._pad_doublepress = [ DoublePressElement(pad) for pad in self._pad ]
        self._pad_CC = [ MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, BASE_PADS[index], Live.MidiMap.MapMode.absolute, 'Pad_CC_' + str(index), index, self) for index in range(32) ]
        self._touchpad = [ MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, BASE_TOUCHPADS[index], 'TouchPad_' + str(index), self) for index in range(8) ]
        self._runner = [ MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, BASE_RUNNERS[index], 'Runner_' + str(index), self) for index in range(8) ]
        self._stream_pads = [ self._pad[index % 8 + abs(index / 8 - 3) * 8] for index in range(32) ]
        self._nav_buttons = ButtonMatrixElement(name='nav_buttons')
        self._nav_buttons.add_row(self._button[4:8])
        self._on_nav_button_value.subject = self._nav_buttons
        self._base_grid = ButtonMatrixElement()
        self._base_grid_CC = ButtonMatrixElement()
        self._keys = ButtonMatrixElement()
        self._keys_display = ButtonMatrixElement()
        for index in range(4):
            self._base_grid.add_row(self._pad[index * 8:index * 8 + 8])
            self._base_grid_CC.add_row(self._pad_CC[index * 8:index * 8 + 8])

        self._base_doublepress_grid = ButtonMatrixElement(name='doublepress_matrix', rows=[ [ self._pad_doublepress[column + row * 8] for column in range(8) ] for row in range(4) ])
        self._keys.add_row(self._touchpad[0:8])
        self._keys_display.add_row(self._runner[0:8])
        self._drumpad_grid = ButtonMatrixElement()
        for index in range(4):
            self._drumpad_grid.add_row(self._pad[index * 8:index * 8 + 4])

        self._up_button = self._nav_buttons[UDLR[0]]
        self._dn_button = self._nav_buttons[UDLR[1]]
        self._lt_button = self._nav_buttons[UDLR[2]]
        self._rt_button = self._nav_buttons[UDLR[3]]
        for button in self._button:
            button._descriptor = 'None'

        for touchpad in self._touchpad:
            touchpad._descriptor = 'None'

        for pad in self._pad:
            pad._descriptor = 'None'

    def _setup_mixer_control(self):
        is_momentary = True
        self._num_tracks = 8
        self._mixer = BaseMixerComponent(self, 8, 4, False, False)
        self._mixer.name = 'Mixer'
        self._mixer.set_track_offset(0)
        for index in range(8):
            self._mixer.channel_strip(index)._invert_mute_feedback = True
            self._mixer.channel_strip(index).name = 'Mixer_ChannelStrip_' + str(index)

        for index in range(4):
            self._mixer.return_strip(index).name = 'Mixer_ReturnStrip_' + str(index)

        self._mixer.selected_strip().name = 'Mixer_SelectedStrip'
        self.song().view.selected_track = self._mixer.channel_strip(0)._track

    def _setup_session_control(self):
        self._session = BaseSessionComponent(8, 4, self)
        self._session.name = 'Session'
        self._session.set_offsets(0, 0)
        self._session.set_stop_track_clip_value(STOP_CLIP)
        self._scene = [ None for index in range(4) ]
        for row in range(4):
            self._scene[row] = self._session.scene(row)
            self._scene[row].name = 'Scene_' + str(row)
            for column in range(8):
                clip_slot = self._scene[row].clip_slot(column)
                clip_slot.name = str(column) + '_Clip_Slot_' + str(row)
                clip_slot.set_triggered_to_play_value(CLIP_TRG_PLAY)
                clip_slot.set_triggered_to_record_value(CLIP_TRG_REC)
                clip_slot.set_stopped_value(CLIP_STOP)
                clip_slot.set_started_value(CLIP_STARTED)
                clip_slot.set_recording_value(CLIP_RECORDING)

        self._session.set_mixer(self._mixer)
        self._session.set_track_banking_increment(TRACK_BANKING_INCREMENT)
        self.set_highlighting_session_component(self._session)
        self._session._do_show_highlight()

    def _setup_selected_session_control(self):
        self._selected_session = BaseSessionComponent(1, 16, self)
        self._selected_session.name = 'SelectedSession'
        self._selected_session.set_offsets(0, 0)
        self._selected_session.set_stop_track_clip_value(STOP_CLIP)
        self._selected_scene = [ None for index in range(16) ]
        for row in range(16):
            self._selected_scene[row] = self._selected_session.scene(row)
            self._selected_scene[row].name = 'SelectedScene_' + str(row)
            clip_slot = self._selected_scene[row].clip_slot(0)
            clip_slot.name = 'Selected_Clip_Slot_' + str(row)
            clip_slot.set_triggered_to_play_value(CLIP_TRG_PLAY)
            clip_slot.set_triggered_to_record_value(CLIP_TRG_REC)
            clip_slot.set_stopped_value(CLIP_STOP)
            clip_slot.set_started_value(CLIP_STARTED)
            clip_slot.set_recording_value(CLIP_RECORDING)

    def _setup_transport_control(self):
        self._transport = TransportComponent()

    def _setup_device_control(self):
        self._device = BaseDeviceComponent(self)
        self._device.name = 'Device_Component'
        self._device.update = self._device_update(self._device)
        self._device._current_bank_details = self._make_current_bank_details(self._device)
        self.set_device_component(self._device)
        self._device_navigator = DeviceNavigator(self._device, self._mixer, self)
        self._device_navigator.name = 'Device_Navigator'
        self._device_selection_follows_track_selection = FOLLOW
        self._device.device_name_data_source().set_update_callback(self._on_device_name_changed)

    def _make_current_bank_details(self, device_component):

        def _current_bank_details():
            if self._is_mod(device_component.device()) is not None:
                if self.modhandler.active_mod() and self.modhandler.active_mod()._param_component._device_parent != None:
                    bank_name = self.modhandler.active_mod()._param_component._bank_name
                    bank = [ param._parameter for param in self.modhandler.active_mod()._param_component._params ]
                    if self.modhandler._shift_value.subject and self.modhandler._shift_value.subject.is_pressed():
                        bank = bank[8:]
                    return (bank_name, bank)
                else:
                    return DeviceComponent._current_bank_details(device_component)
            else:
                return DeviceComponent._current_bank_details(device_component)

        return _current_bank_details

    def _setup_mode_select(self):
        self._mode_selector = BaseModeSelector(self)
        self._mode_selector.set_mode_buttons(tuple(self._button[0:4]))
        self._button[0].set_on_off_values(1, 0)
        self._button[1].set_on_off_values(4, 0)
        self._button[2].set_on_off_values(3, 0)
        self._button[3].set_on_off_values(5, 0)

    def _setup_user_mode_select(self):
        self._user_mode_selector = BaseUserModeSelector(self)
        self._user_mode_selector.set_mode_buttons(tuple(self._button[4:8]))
        self._user_mode_selector.set_enabled(False)

    def _setup_midi_mode_select(self):
        self._midi_mode_selector = BaseMidiModeSelector(self._midi_mode_value)
        self._midi_mode_selector.set_mode_buttons(tuple(self._button[4:6]))
        self._midi_mode_selector.set_enabled(False)

    def _setup_split_mode_select(self):
        self._split_mode_selector = BaseSplitModeSelector(self._split_mode_value)
        self._split_mode_selector.set_mode_toggle(self._touchpad[0])
        self._split_mode_selector.set_enabled(False)

    def _setup_sequencer_mode_select(self):
        self._sequencer_mode_selector = BaseSequencerModeSelector(self._sequencer_mode_value)
        self._sequencer_mode_selector.set_mode_toggle(self._touchpad[1])
        self._sequencer_mode_selector.set_enabled(False)

    def _setup_offset_component(self):
        self._offset_component = ScrollingOffsetComponent(self._offset_value)
        self._offset_component._shifted_value = 11
        self._shift_is_momentary = OFFSET_SHIFT_IS_MOMENTARY

    def _setup_vertical_offset_component(self):
        self._vertical_offset_component = ScrollingOffsetComponent(self._vertical_offset_value)

    def _setup_scale_offset_component(self):
        self._scale_offset_component = ScrollingOffsetComponent(self._scale_offset_value)
        self._scale_offset_component._minimum = 0
        self._scale_offset_component._maximum = len(SCALES.keys()) - 1

    def _setup_session_recording_component(self):
        self._clip_creator = ClipCreator()
        self._recorder = BaseSessionRecordingComponent(self._clip_creator, ViewControlComponent())

    def _setup_m4l_interface(self):
        self._m4l_interface = M4LInterfaceComponent(controls=self.controls, component_guard=self.component_guard)
        self.get_control_names = self._m4l_interface.get_control_names
        self.get_control = self._m4l_interface.get_control
        self.grab_control = self._m4l_interface.grab_control
        self.release_control = self._m4l_interface.release_control

    def _setup_drumgroup(self):
        self._drumgroup = DrumGroupComponent()

    def _setup_mod(self):
        if isinstance(__builtins__, dict):
            if 'monomodular' not in __builtins__.keys() or not isinstance(__builtins__['monomodular'], ModRouter):
                __builtins__['monomodular'] = ModRouter()
        elif not hasattr(__builtins__, 'monomodular') or not isinstance(__builtins__['monomodular'], ModRouter):
            setattr(__builtins__, 'monomodular', ModRouter())
        self.monomodular = __builtins__['monomodular']
        if not self.monomodular.has_host():
            self.monomodular.set_host(self)
        self.monomodular.name = 'monomodular_switcher'
        self.modhandler = BaseModHandler(script=self, detect_mod=self._on_new_device_set)
        self.modhandler.name = 'ModHandler'

    def _setup_OSC_layer(self):
        self._OSC_id = 0
        if hasattr(__builtins__, 'control_surfaces') or isinstance(__builtins__, dict) and 'control_surfaces' in __builtins__.keys():
            for cs in __builtins__['control_surfaces']:
                if cs is self:
                    break
                elif isinstance(cs, Base):
                    self._OSC_id += 1

        self._prefix = '/Live/Base/' + str(self._OSC_id)
        self._outPrt = OSC_OUTPORT
        if self.oscServer is not None:
            self.oscServer.shutdown()
        self.oscServer = RemixNet.OSCServer('localhost', self._outPrt, 'localhost', 10001)

    def _setup_step_sequencer(self):
        self._grid_resolution = self.register_disconnectable(GridResolution())
        self._playhead_element = PlayheadElement(self._c_instance.playhead)
        self._playhead_element.reset()
        self._skin = make_default_skin()
        self._note_sequencer = StepSeqComponent(self._clip_creator, self._skin, grid_resolution=self._grid_resolution, name='Note_Sequencer')
        self._note_sequencer._playhead_component._notes = tuple(range(16))
        self._note_sequencer._playhead_component._triplet_notes = tuple(chain(*starmap(range, ((0, 6), (8, 14)))))
        self._note_sequencer.set_enabled(True)
        self._step_sequencer = StepSeqComponent(self._clip_creator, self._skin, grid_resolution=self._grid_resolution, name='Step_Sequencer')
        self._step_sequencer._note_editor._visible_steps = self._visible_steps
        self._step_sequencer._drum_group._update_pad_led = self._drum_group_update_pad_led
        self._step_sequencer._drum_group._update_control_from_script = self._update_control_from_script
        self._step_sequencer._playhead_component._notes = tuple(range(16))
        self._step_sequencer._playhead_component._triplet_notes = tuple(chain(*starmap(range, ((0, 3),
         (4, 7),
         (8, 11),
         (12, 15)))))
        self._step_sequencer.set_enabled(True)
        self._on_detail_clip_changed.subject = self.song().view

    def _visible_steps(self):
        first_time = self._step_sequencer._note_editor.page_length * self._step_sequencer._note_editor._page_index
        steps_per_page = self._step_sequencer._note_editor._get_step_count()
        step_length = self._step_sequencer._note_editor._get_step_length()
        indices = range(steps_per_page)
        if self._step_sequencer._note_editor._is_triplet_quantization():
            indices = filter(lambda k: k % 4 != 3, indices)
        return [ (self._step_sequencer._note_editor._time_step(first_time + k * step_length), index) for k, index in enumerate(indices) ]

    def _drum_group_update_pad_led(self, pad, button, soloed_pads):
        DrumGroupComponent._update_pad_led(self._step_sequencer._drum_group, pad, button, soloed_pads)
        button.send_value(button._off_value, True)

    def _update_control_from_script(self):
        takeover_drums = self._step_sequencer._drum_group._takeover_drums or self._step_sequencer._drum_group._selected_pads
        profile = 'default' if takeover_drums else 'drums'
        if self._step_sequencer._drum_group._drum_matrix:
            for button, _ in self._step_sequencer._drum_group._drum_matrix.iterbuttons():
                if button:
                    translation_channel = self._current_channel()
                    button.set_channel(translation_channel)
                    button.set_enabled(takeover_drums)
                    button.sensitivity_profile = profile

    @subject_slot('value')
    def _on_note_matrix_pressed(self, value, x, y, *a):
        new_note = self._base_grid.get_button(x, y)._msg_identifier
        if y > 1 and value:
            self._note_sequencer._note_editor.editing_note = self._base_grid.get_button(x, y)._stored_note
            self._assign_midi_shift_layer()

    @subject_slot('detail_clip')
    def _on_detail_clip_changed(self):
        clip = self.song().view.detail_clip
        clip = clip if clip and clip.is_midi_clip else None

    def _current_channel(self):
        cur_track = self._mixer._selected_strip._track
        cur_chan = cur_track.current_input_sub_routing
        if len(cur_chan) == 0:
            cur_chan = 'All Channels'
        if cur_chan in CHANNELS:
            cur_chan = CHANNELS.index(cur_chan) % 15 + 1
        return cur_chan

    def pad_held(self):
        return sum(self._last_pad_stream) > 0

    def shift_pressed(self):
        return self._mode_selector._held is not None

    def select_pressed(self):
        return self._mixer._held is not None

    def _shift_update(self, mode, shifted = False):
        if not isinstance(mode, int):
            raise AssertionError
            if not self.pad_held() or mode in (1, 2) and self._layer in (1, 2):
                shifted = mode is not self._layer and False
            self._layer = mode
            self._deassign_all()
            self._layers[self._layer](shifted)

    def _check_mode_shift(self, held_key = None):
        if held_key is self._mode_selector._held:
            self._shift_update(self._mode_selector._mode_index, True)

    def _select_update(self, held_strip = None):
        if not self.shift_pressed() and not self.pad_held():
            if self.select_pressed():
                self._delayed_select_update(held_strip)
            else:
                self._shift_update(self._mode_selector._mode_index, False)

    def _delayed_select_update(self, held_strip = None):
        self._display_mode()
        if self._mixer._held is held_strip:
            with self.component_guard():
                self._session.set_scene_bank_buttons(None, None)
                self._session.set_track_bank_buttons(None, None)
                for pad in self._touchpad:
                    pad.set_on_off_values(127, 0)
                    pad.release_parameter()
                    pad.use_default_message()
                    pad.reset(True)
                    pad.set_enabled(True)

                for pad in self._pad:
                    pad.set_on_off_values(127, 0)
                    pad.release_parameter()
                    pad.use_default_message()
                    pad.reset(True)
                    pad.set_enabled(True)
                    pad.set_force_next_value()

                for pad in self._pad_CC:
                    pad.release_parameter()
                    pad.use_default_message()
                    pad.set_enabled(True)

                for button in self._button[4:8]:
                    button.release_parameter()

                self._send_midi(LIVEBUTTONMODE)
                for column in range(7):
                    for row in range(4):
                        self._scene[row].clip_slot(column).set_launch_button(self._pad[column + row * 8])

                for row in range(4):
                    self._scene[row].set_launch_button(self._pad[7 + row * 8])
                    self._pad[7 + row * 8]._descriptor = 'Scene'
                    self._pad[7 + row * 8].set_on_off_values(7, 3)
                    self._pad[7 + row * 8].turn_off()

                self._session.set_scene_bank_buttons(self._dn_button, self._up_button)
                self._dn_button._descriptor = 'SceneDn'
                self._up_button._descriptor = 'SceneUp'
                self._session.set_track_bank_buttons(self._lt_button, self._rt_button)
                self._lt_button._descriptor = 'TrackLeft'
                self._rt_button._descriptor = 'TrackRight'
                self._current_nav_buttons = self._button[4:8]
                for index in range(4):
                    self._button[index + 4].set_on_off_values(SESSION_NAV[0], 0)

                self._session.update()
                self.request_rebuild_midi_map()
            self.schedule_message(1, self._session._reassign_scenes)

    def _check_select_shift(self, held_strip = None):
        if held_strip is self._mixer._held and held_strip is not None:
            if self._mode_selector._held is not None:
                cur_track = self._mixer._selected_strip._track
                if cur_track.has_midi_input:
                    cur_chan = cur_track.current_input_sub_routing
                    if len(cur_chan) == 0:
                        cur_chan = 'All Channels'
                    if cur_chan in CHANNELS:
                        cur_chan = CHANNELS.index(cur_chan) % 15 + 1
                        self._offsets[cur_chan]['split'] = not self._offsets[cur_chan]['split']
                self._shift_update(self._mode_selector._mode_index, True)
            else:
                with self.component_guard():
                    for column in range(7):
                        for row in range(4):
                            self._pad[column + row * 8].set_force_next_value()
                            self._scene[row].clip_slot(column).set_launch_button(self._pad[column + row * 8])
                            self._pad[column + row * 8]._descriptor = 'Launch'

                    for row in range(4):
                        self._scene[row].set_launch_button(self._pad[7 + row * 8])
                        self._pad[7 + row * 8]._descriptor = 'Scene'

                self._notify_desciptors()
                self.request_rebuild_midi_map()
        else:
            self._shift_update(self._mode_selector._mode_index, False)

    def _user_shift_update(self, mode, shifted = False):
        if self._user_mode_selector._is_enabled:
            if mode is not self._user_layer:
                shifted = False
            self._user_layer = mode
            self._set_layer3(shifted)

    def _mode_update(self, mode):
        pass

    def _midi_mode_value(self, mode):
        cur_track = self._mixer._selected_strip._track
        if cur_track.has_midi_input:
            cur_chan = cur_track.current_input_sub_routing
            if len(cur_chan) == 0:
                cur_chan = 'All Channels'
            if cur_chan in CHANNELS:
                cur_chan = CHANNELS.index(cur_chan) % 15 + 1
                self._offsets[cur_chan]['mode'] = MODES[mode]

    def _offset_value(self, offset):
        if not self.pad_held():
            cur_track = self._mixer._selected_strip._track
            if cur_track.has_midi_input:
                cur_chan = cur_track.current_input_sub_routing
                if len(cur_chan) == 0:
                    cur_chan = 'All Channels'
                if cur_chan in CHANNELS:
                    cur_chan = CHANNELS.index(cur_chan) % 15 + 1
                    offsets = self._current_device_offsets(self._offsets[cur_chan])
                    scale = offsets['scale']
                    if scale is 'Auto':
                        scale = self._detect_instrument_type(cur_track)
                    if scale is 'DrumPad':
                        old_offset = offsets['drumoffset']
                        self._offsets[cur_chan]['drumoffset'] = offset
                        self._set_device_attribute(self._top_device(), 'drumoffset', offset)
                        self.show_message('New drum root is ' + str(self._offsets[cur_chan]['drumoffset']))
                        if OSC_TRANSMIT:
                            self.oscServer.sendOSC(self._prefix + '/glob/offset/', str(self.generate_strip_string(offset)))
                        newval = list(str(offset))
                        if len(newval) == 2:
                            self._display_chars(newval[0], newval[1])
                        elif len(newval) == 1:
                            self._display_chars('-', newval[0])
                    else:
                        self._offsets[cur_chan]['offset'] = offset
                        self._set_device_attribute(self._top_device(), 'offset', offset)
                        self.show_message('New root is Note# ' + str(self._offsets[cur_chan]['offset']) + ', ' + str(NOTENAMES[self._offsets[cur_chan]['offset']]))
                        if OSC_TRANSMIT:
                            self.oscServer.sendOSC(self._prefix + '/glob/offset/', str(self.generate_strip_string(offset)))
                        newval = list(str(offset))
                        if len(newval) >= 2:
                            self._display_chars(newval[0], newval[1])
                        elif len(newval) == 1:
                            self._display_chars('-', newval[0])
                    self._assign_midi_layer()

    def _vertical_offset_value(self, offset):
        if not self.pad_held():
            cur_track = self._mixer._selected_strip._track
            if cur_track.has_midi_input:
                cur_chan = cur_track.current_input_sub_routing
                if len(cur_chan) == 0:
                    cur_chan = 'All Channels'
                if cur_chan in CHANNELS:
                    cur_chan = CHANNELS.index(cur_chan) % 15 + 1
                    offsets = self._current_device_offsets(self._offsets[cur_chan])
                    self._offsets[cur_chan]['vertoffset'] = offset
                    self._set_device_attribute(self._top_device(), 'vertoffset', offset)
                    self.show_message('New vertical offset is ' + str(self._offsets[cur_chan]['vertoffset']))
                    if OSC_TRANSMIT:
                        self.oscServer.sendOSC(self._prefix + '/glob/vertoffset/', str(self.generate_strip_string(offset)))
                    newval = list(str(offset))
                    if len(newval) >= 2:
                        self._display_chars(newval[0], newval[1])
                    elif len(newval) == 1:
                        self._display_chars('-', newval[0])
                    self._assign_midi_layer()

    def _scale_offset_value(self, offset):
        if not self.pad_held():
            cur_track = self._mixer._selected_strip._track
            if cur_track.has_midi_input:
                cur_chan = cur_track.current_input_sub_routing
                if len(cur_chan) == 0:
                    cur_chan = 'All Channels'
                if cur_chan in CHANNELS:
                    cur_chan = CHANNELS.index(cur_chan) % 15 + 1
                    offsets = self._current_device_offsets(self._offsets[cur_chan])
                    self._offsets[cur_chan]['scale'] = SCALENAMES[offset]
                    self._set_device_attribute(self._top_device(), 'scale', SCALENAMES[offset])
                    self.show_message('New scale is ' + str(self._offsets[cur_chan]['scale']))
                    if OSC_TRANSMIT:
                        self.oscServer.sendOSC(self._prefix + '/glob/offset/scale/', str(self.generate_strip_string(SCALENAMES[offset])))
                    if str(SCALENAMES[offset]) in SCALEABBREVS.keys():
                        newval = list(str(SCALEABBREVS[str(SCALENAMES[offset])]))
                    else:
                        newval = list(str(SCALENAMES[offset]))
                    if len(newval) >= 2:
                        self._display_chars(newval[0], newval[1])
                    if len(SCALES[self._offsets[cur_chan]['scale']]) > 8:
                        self._offsets[cur_chan]['vert_offset'] = 8
                    self._assign_midi_layer()

    def _split_mode_value(self, mode):
        if not self.pad_held():
            if self.shift_pressed():
                cur_track = self._mixer._selected_strip._track
                if cur_track.has_midi_input:
                    cur_chan = cur_track.current_input_sub_routing
                    if len(cur_chan) == 0:
                        cur_chan = 'All Channels'
                    if cur_chan in CHANNELS:
                        cur_chan = CHANNELS.index(cur_chan) % 15 + 1
                        self._offsets[cur_chan]['split'] = bool(mode)
                        self._set_device_attribute(self._top_device(), 'split', bool(mode))

    def _sequencer_mode_value(self, mode):
        if not self.pad_held():
            if self.shift_pressed():
                cur_track = self._mixer._selected_strip._track
                if cur_track.has_midi_input:
                    cur_chan = cur_track.current_input_sub_routing
                    if len(cur_chan) == 0:
                        cur_chan = 'All Channels'
                    if cur_chan in CHANNELS:
                        cur_chan = CHANNELS.index(cur_chan) % 15 + 1
                        self._offsets[cur_chan]['sequencer'] = bool(mode)
                        self._set_device_attribute(self._top_device(), 'sequencer', bool(mode))

    def _deassign_all(self):
        self.modhandler._fader_color_override = False
        self._send_midi(tuple([240,
         0,
         1,
         97,
         12,
         50,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         1,
         247]))
        self._send_midi(tuple([191, 122, 64]))
        self._current_nav_buttons = []
        with self.component_guard():
            self.release_controlled_track()
            self._step_sequencer.set_loop_selector_matrix(None)
            self._step_sequencer.set_quantization_buttons(None)
            self._step_sequencer.set_follow_button(None)
            self._step_sequencer.set_button_matrix(None)
            self._step_sequencer.set_drum_matrix(None)
            self._step_sequencer.set_drum_bank_up_button(None)
            self._step_sequencer.set_drum_bank_down_button(None)
            self._step_sequencer.set_mute_button(None)
            self._step_sequencer.set_solo_button(None)
            self._step_sequencer.set_playhead(None)
            self._on_note_matrix_pressed.subject = None
            self._note_sequencer.set_loop_selector_matrix(None)
            self._note_sequencer.set_quantization_buttons(None)
            self._note_sequencer.set_follow_button(None)
            self._note_sequencer.set_button_matrix(None)
            self._note_sequencer.set_playhead(None)
            self._drumgroup.set_drum_matrix(None)
            self.modhandler._assign_keys(None)
            self.modhandler._assign_base_grid(None)
            self.modhandler._assign_base_grid_CC(None)
            self.modhandler.set_shift_button(None)
            self.modhandler.set_device_component(None)
            self._transport.set_overdub_button(None)
            self._recorder.set_new_button(None)
            self._recorder.set_record_button(None)
            self._recorder.set_length_button(None)
            self._recorder.set_length_buttons(None)
            self._offset_component.deassign_all()
            self._vertical_offset_component.deassign_all()
            self._scale_offset_component.deassign_all()
            self._device_navigator.deassign_all()
            self._device.deassign_all()
            self._mixer.deassign_all()
            self._selected_session.deassign_all()
            self._session.deassign_all()
            self.set_highlighting_session_component(self._session)
            self._session._do_show_highlight()
            self._user_mode_selector.set_enabled(False)
            self._midi_mode_selector.set_enabled(False)
            self._split_mode_selector.set_enabled(False)
            self._sequencer_mode_selector.set_enabled(False)
            for pad in self._touchpad:
                pad.set_on_off_values(127, 0)
                pad.release_parameter()
                pad.use_default_message()
                pad.reset(True)
                pad.set_enabled(True)
                pad._descriptor = '_'

            for pad in self._pad:
                pad.display_press = False
                pad.set_on_off_values(127, 0)
                pad.release_parameter()
                pad.use_default_message()
                pad.reset(True)
                pad.set_enabled(True)
                pad._descriptor = '_'
                pad.set_force_next_value()

            for pad in self._pad_CC:
                pad.release_parameter()
                pad.use_default_message()
                pad.set_enabled(True)

            for button in self._button[4:8]:
                button.set_on_off_values(127, 0)
                button.release_parameter()
                button.use_default_message()
                button.reset(True)
                button.set_enabled(True)
                button._descriptor = '_'

            for fader in self._fader[0:8]:
                fader.release_parameter()
                fader.use_default_message()
                fader.send_value(0, True)
                fader.set_enabled(True)

            for runner in self._runner:
                runner.release_parameter()
                runner.reset(True)

    def _set_layer0(self, shifted = False):
        with self.component_guard():
            self._display_mode()
            self._send_midi(LIVEBUTTONMODE)
            self._mixer.master_strip().set_volume_control(self._fader[8])
            self._send_midi(tuple([240,
             0,
             1,
             97,
             12,
             61,
             7,
             7,
             7,
             7,
             7,
             7,
             7,
             7,
             2,
             247]))
            for index in range(8):
                self._touchpad[index].set_on_off_values(CHAN_SELECT, 0)
                self._mixer.channel_strip(index).set_select_button(self._touchpad[index])
                self._touchpad[index]._descriptor = 'Select'
                self._mixer.channel_strip(index).set_volume_control(self._fader[index])

            self._session.set_scene_bank_buttons(self._dn_button, self._up_button)
            self._dn_button._descriptor = 'SceneDn'
            self._up_button._descriptor = 'SceneUp'
            self._session.set_track_bank_buttons(self._lt_button, self._rt_button)
            self._lt_button._descriptor = 'TrackDn'
            self._rt_button._descriptor = 'TrackUp'
            self._current_nav_buttons = self._button[4:8]
            for index in range(4):
                self._button[index + 4].set_on_off_values(SESSION_NAV[shifted], 0)

            self._session.update()
            if not shifted:
                for column in range(8):
                    for row in range(4):
                        self._scene[row].clip_slot(column).set_launch_button(self._pad[column + row * 8])
                        self._pad[column + row * 8]._descriptor = 'Clip'

            else:
                self._send_midi(tuple([240,
                 0,
                 1,
                 97,
                 12,
                 61,
                 7,
                 7,
                 7,
                 7,
                 7,
                 7,
                 7,
                 7,
                 2,
                 247]))
                self._session._shifted = True
                for index in range(8):
                    self._pad[index].set_on_off_values(TRACK_MUTE, 0)
                    self._pad[index]._descriptor = 'Mute'
                    self._mixer.channel_strip(index).set_mute_button(self._pad[index])
                    self._pad[index + 8].set_on_off_values(TRACK_SOLO, 0)
                    self._pad[index + 8]._descriptor = 'Solo'
                    self._mixer.channel_strip(index).set_solo_button(self._pad[index + 8])
                    self._pad[index + 16].set_on_off_values(TRACK_ARM, 0)
                    self._pad[index + 16]._descriptor = 'Arm'
                    self._mixer.channel_strip(index).set_arm_button(self._pad[index + 16])
                    self._pad[index + 24].set_on_off_values(TRACK_STOP, TRACK_STOP)
                    self._pad[index + 24].send_value(TRACK_STOP)
                    self._pad[index + 24]._descriptor = 'Stop'

                self._session.set_stop_track_clip_buttons(tuple(self._pad[24:32]))
            self._mixer.update()
            self._notify_descriptors()
        self.request_rebuild_midi_map()

    def _set_layer1(self, shifted = False):
        with self.component_guard():
            self._display_mode()
            for index in range(4):
                self._mixer.return_strip(index).set_volume_control(self._fader[index + 4])

            self._mixer._selected_strip.set_send_controls(tuple(self._fader[0:4]))
            self._mixer.master_strip().set_volume_control(self._fader[8])
            if not shifted:
                self._send_midi(tuple([240,
                 0,
                 1,
                 97,
                 12,
                 61,
                 5,
                 5,
                 5,
                 5,
                 4,
                 4,
                 4,
                 4,
                 2,
                 247]))
                for index in range(8):
                    self._touchpad[index].set_on_off_values(CHAN_SELECT, 0)
                    self._mixer.channel_strip(index).set_select_button(self._touchpad[index])
                    self._touchpad[index]._descriptor = 'Select'

                if self._mixer.shifted() or not self._assign_midi_layer():
                    self._send_midi(LIVEBUTTONMODE)
                    for column in range(8):
                        for row in range(4):
                            self._scene[row].clip_slot(column).set_launch_button(self._pad[column + row * 8])

                    self._session.set_scene_bank_buttons(self._dn_button, self._up_button)
                    self._dn_button._descriptor = 'SceneDn'
                    self._up_button._descriptor = 'SceneUp'
                    self._session.set_track_bank_buttons(self._lt_button, self._rt_button)
                    self._lt_button._descriptor = 'TrackLeft'
                    self._rt_button._descriptor = 'TrackRight'
                    for index in range(4):
                        self._button[index + 4].set_on_off_values(SESSION_NAV[shifted], 0)

                    self._current_nav_buttons = self._button[4:8]
                    self._session.set_show_highlight(True)
                    self._session.update()
                else:
                    self._button[4].set_on_off_values(OVERDUB + 7, OVERDUB)
                    self._button[4]._descriptor = 'Overdub'
                    self._button[5].set_on_off_values(NEW + 7, NEW)
                    self._button[5]._descriptor = 'New'
                    self._button[6].set_on_off_values(RECORD + 7, RECORD)
                    self._button[6]._descriptor = 'Record'
                    self._button[7].set_on_off_values(LENGTH + 7, LENGTH)
                    self._button[7]._descriptor = 'Length'
                    self._transport.set_overdub_button(self._button[4])
                    self._recorder.set_new_button(self._button[5])
                    self._recorder.set_record_button(self._button[6])
                    self._recorder.set_length_button(self._button[7])
            else:
                is_midi = self._assign_midi_shift_layer()
                if not is_midi:
                    for index in range(8):
                        self._touchpad[index].set_on_off_values(CHAN_SELECT, 0)
                        self._mixer.channel_strip(index).set_select_button(self._touchpad[index])

                    self._send_midi(LIVEBUTTONMODE)
                    self._session._shifted = True
                    self._session.set_scene_bank_buttons(self._dn_button, self._up_button)
                    self._dn_button._descriptor = 'SceneDn'
                    self._up_button._descriptor = 'SceneUp'
                    self._session.set_track_bank_buttons(self._lt_button, self._rt_button)
                    self._lt_button._descriptor = 'TrackDn'
                    self._lt_button._descriptor = 'TrackUp'
                    self._current_nav_buttons = self._button[4:8]
                    for index in range(4):
                        self._button[index + 4].set_on_off_values(SESSION_NAV[shifted], 0)

                    self._session.update()
                else:
                    self._button[4].set_on_off_values(24, 0)
                    self._offset_component.set_shift_button(self._button[4])
                    for button in self._button[5:8]:
                        button.set_on_off_values(16, 15)

                    self._recorder.set_length_buttons(self._button[5:8])
                for index in range(8):
                    self._send_midi(tuple([191, index + 10, 125]))

                for index in range(8):
                    self._mixer.channel_strip(index).set_volume_control(self._fader[index])

                if is_midi not in ('Mod', 'DrumSequencer', 'NoteSequencer'):
                    if not self.pad_held():
                        for index in range(8):
                            self._pad[index].set_on_off_values(TRACK_MUTE, 0)
                            self._pad[index]._descriptor = 'Mute'
                            self._mixer.channel_strip(index).set_mute_button(self._pad[index])
                            self._pad[index + 8]._descriptor = 'Solo'
                            self._pad[index + 8].set_on_off_values(TRACK_SOLO, 0)
                            self._mixer.channel_strip(index).set_solo_button(self._pad[index + 8])
                            self._pad[index + 16]._descriptor = 'Arm'
                            self._pad[index + 16].set_on_off_values(TRACK_ARM, 0)
                            self._mixer.channel_strip(index).set_arm_button(self._pad[index + 16])
                            self._pad[index + 24].set_on_off_values(TRACK_STOP, TRACK_STOP)
                            self._pad[index + 24].send_value(TRACK_STOP)
                            self._pad[index + 24]._descriptor = 'Stop'

                        self._session.set_stop_track_clip_buttons(tuple(self._pad[24:32]))
                    else:
                        self._assign_midi_layer()
            self._mixer.update()
            self._notify_descriptors()
        self.request_rebuild_midi_map()

    def _set_layer2(self, shifted = False):
        with self.component_guard():
            self._display_mode()
            self._device.set_parameter_controls(tuple(self._fader[0:8]))
            self._device.set_enabled(True)
            self._mixer.master_strip().set_volume_control(self._fader[8])
            if not shifted:
                self._send_midi(tuple([240,
                 0,
                 1,
                 97,
                 12,
                 61,
                 6,
                 6,
                 6,
                 6,
                 6,
                 6,
                 6,
                 6,
                 2,
                 247]))
                for index in range(8):
                    self._touchpad[index].set_on_off_values(CHAN_SELECT, 0)
                    self._touchpad[index]._descriptor = 'Select'
                    self._mixer.channel_strip(index).set_select_button(self._touchpad[index])

                if self._mixer.shifted() or not self._assign_midi_layer():
                    self._send_midi(LIVEBUTTONMODE)
                    for column in range(8):
                        for row in range(4):
                            self._scene[row].clip_slot(column).set_launch_button(self._pad[column + row * 8])
                            self._pad[column + row * 8]._descriptor = 'Clip'

                self._device.set_bank_nav_buttons(self._up_button, self._dn_button)
                self._device_navigator.set_nav_buttons(self._rt_button, self._lt_button)
                self._current_nav_buttons = self._button[4:8]
                self._up_button.set_on_off_values(BANK_NAV, 0)
                self._dn_button.set_on_off_values(BANK_NAV, 0)
                self._dn_button._descriptor = 'BankDn'
                self._up_button._descriptor = 'BankUp'
                self._lt_button.set_on_off_values(DEVICE_NAV, 0)
                self._rt_button.set_on_off_values(DEVICE_NAV, 0)
                self._lt_button._descriptor = 'DeviceLeft'
                self._rt_button._descriptor = 'DeviceRight'
                self._device.update()
                self._device_navigator.update()
            else:
                is_midi = self._assign_midi_shift_layer()
                if not is_midi:
                    for index in range(8):
                        self._touchpad[index].set_on_off_values(CHAN_SELECT, 0)
                        self._touchpad[index]._descriptor = 'Select'
                        self._mixer.channel_strip(index).set_select_button(self._touchpad[index])

                    self._send_midi(LIVEBUTTONMODE)
                    self._session._shifted = True
                    for index in range(4):
                        self._button[index + 4].set_on_off_values(DEVICE_NAV, 0)

                    self._device.deassign_all()
                    self._send_midi(tuple([240,
                     0,
                     1,
                     97,
                     12,
                     61,
                     7,
                     7,
                     7,
                     7,
                     7,
                     7,
                     7,
                     7,
                     2,
                     247]))
                    for index in range(8):
                        self._mixer.channel_strip(index).set_volume_control(self._fader[index])

                if is_midi not in ('Mod', 'DrumSequencer', 'NoteSequencer'):
                    if not self.pad_held():
                        for index in range(8):
                            self._pad[index].set_on_off_values(TRACK_MUTE, 0)
                            self._pad[index]._descriptor = 'Mute'
                            self._mixer.channel_strip(index).set_mute_button(self._pad[index])
                            self._pad[index + 8].set_on_off_values(TRACK_SOLO, 0)
                            self._pad[index + 8]._descriptor = 'Solo'
                            self._mixer.channel_strip(index).set_solo_button(self._pad[index + 8])
                            self._pad[index + 16].set_on_off_values(TRACK_ARM, 0)
                            self._pad[index + 16]._descriptor = 'Arm'
                            self._mixer.channel_strip(index).set_arm_button(self._pad[index + 16])
                            self._pad[index + 24].set_on_off_values(TRACK_STOP, TRACK_STOP)
                            self._pad[index + 24].send_value(TRACK_STOP)
                            self._pad[index + 24]._descriptor = 'Stop'

                        self._session.set_stop_track_clip_buttons(tuple(self._pad[24:32]))
                    else:
                        self._assign_midi_layer()
                self._device_navigator.set_layer_buttons(self._rt_button, self._lt_button)
                self._rt_button._descriptor = 'BankUp'
                self._lt_button._descriptor = 'BankDn'
                self._device_navigator.set_chain_nav_buttons(self._up_button, self._dn_button)
                self._up_button._descriptor = 'ChainUp'
                self._dn_button._descriptor = 'ChainDn'
                self._current_nav_buttons = self._button[4:8]
                self._up_button.set_on_off_values(CHAIN_NAV, 0)
                self._dn_button.set_on_off_values(CHAIN_NAV, 0)
                self._lt_button.set_on_off_values(DEVICE_LAYER, 0)
                self._rt_button.set_on_off_values(DEVICE_LAYER, 0)
                self._device.update()
                self._device_navigator.update()
            self._mixer.update()
        self.schedule_message(2, self._step_sequencer._drum_group._update_drum_pad_leds)
        self._notify_descriptors()
        self.request_rebuild_midi_map()

    def _set_layer3(self, shifted = False):
        with self.component_guard():
            for pad in self._pad:
                pad.send_value(0, True)

            self._display_mode()
            self._deassign_all()
            self._send_midi(USERBUTTONMODE)
            for index in range(8):
                self._mixer.channel_strip(index).set_select_button(self._touchpad[index])
                self._touchpad[index]._descriptor = 'Select'
                self._touchpad[index].set_on_off_values(CHAN_SELECT, 0)

            self._mixer.master_strip().set_volume_control(self._fader[8])
            for button in self._button[4:8]:
                button.set_on_off_values(USERMODE, 0)

            self._user_mode_selector.set_enabled(True)
            self._assign_alternate_mappings(self._user_layer + 12)
            self._send_midi(tuple([240,
             0,
             1,
             97,
             12,
             61,
             1,
             1,
             1,
             1,
             1,
             1,
             1,
             1,
             2,
             247]))
            self._send_midi(tuple([191, 122, 72]))
            self._notify_descriptors()

    def set_chain_selector(self, mode):
        key = str('@userChain')
        preset = None
        for track in range(len(self.song().tracks)):
            for device in range(len(self.song().tracks[track].devices)):
                if match(key, str(self.song().tracks[track].devices[device].name)) != None:
                    preset = self.song().tracks[track].devices[device]

        for return_track in range(len(self.song().return_tracks)):
            for device in range(len(self.song().return_tracks[return_track].devices)):
                if match(key, str(self.song().return_tracks[return_track].devices[device].name)) != None:
                    preset = self.song().return_tracks[return_track].devices[device]

        for device in range(len(self.song().master_track.devices)):
            if match(key, str(self.song().master_track.devices[device].name)) != None:
                preset = self.song().master_track.devices[device]

        if preset != None:
            for parameter in preset.parameters:
                if parameter.name == 'Chain Selector':
                    parameter.value = max(min(128 / 3 * mode, 127), 0)
                    break

    def _assign_midi_layer(self):
        cur_track = self._mixer._selected_strip._track
        is_midi = False
        scale, offset, vertoffset = (' ', ' ', ' ')
        if cur_track.has_midi_input:
            if AUTO_ARM_SELECTED:
                if not cur_track.arm:
                    self.schedule_message(1, self._arm_current_track, cur_track)
            is_midi = True
            cur_chan = cur_track.current_input_sub_routing
            if len(cur_chan) == 0:
                cur_chan = 'All Channels'
            if cur_chan in CHANNELS:
                cur_chan = CHANNELS.index(cur_chan) % 15 + 1
                offsets = self._current_device_offsets(self._offsets[cur_chan])
                offset, vertoffset, scale, split, sequencer = (offsets['offset'],
                 offsets['vertoffset'],
                 offsets['scale'],
                 offsets['split'],
                 offsets['sequencer'])
                if scale == 'Auto':
                    scale = self._detect_instrument_type(cur_track)
                if scale == 'Session':
                    is_midi = False
                elif scale == 'Mod':
                    is_midi = True
                elif scale in SPLIT_SCALES or split:
                    self._send_midi(SPLITBUTTONMODE)
                    scale_len = len(SCALES[scale])
                    if scale is 'DrumPad':
                        for row in range(4):
                            for column in range(4):
                                self._pad[column + row * 8].set_identifier((DRUMNOTES[column + row * 8] + self._offsets[cur_chan]['drumoffset'] * 4) % 127)
                                self._pad[column + row * 8].scale_color = DRUMCOLORS[0]
                                self._pad[column + row * 8].display_press = True
                                self._pad[column + row * 8].press_flash(0, True)
                                self._pad_CC[column + row * 8].set_identifier((DRUMNOTES[column + row * 8] + self._offsets[cur_chan]['drumoffset'] * 4) % 127)
                                self._offset_component._shifted_value = 3
                                self._pad[column + row * 8].set_enabled(False)
                                self._pad[column + row * 8].set_channel(cur_chan)
                                self._pad[column + row * 8]._descriptor = str(NOTENAMES[self._pad[column + row * 8]._msg_identifier])
                                self._pad_CC[column + row * 8].set_enabled(False)
                                self._pad_CC[column + row * 8].set_channel(cur_chan)
                                if not sequencer:
                                    self._selected_scene[column + row * 4].clip_slot(0).set_launch_button(self._pad[column + 4 + row * 8])

                    else:
                        current_note = self._note_sequencer._note_editor.editing_note
                        for row in range(2, 4):
                            for column in range(8):
                                note_pos = column + abs(3 - row) * int(vertoffset)
                                note = offset + SCALES[scale][note_pos % scale_len] + 12 * int(note_pos / scale_len)
                                self._pad[column + row * 8].set_identifier(note % 127)
                                self._pad[column + row * 8].scale_color = KEYCOLORS[(note % 12 in WHITEKEYS) + (note_pos % scale_len == 0) * 2]
                                if note is current_note and sequencer:
                                    self._pad[column + row * 8].scale_color = SELECTED_NOTE
                                self._pad[column + row * 8].display_press = True
                                self._pad[column + row * 8].press_flash(0, True)
                                self._pad_CC[column + row * 8].set_identifier(note % 127)
                                self._offset_component._shifted_value = 11
                                self._pad[column + row * 8].set_enabled(False)
                                self._pad[column + row * 8].set_channel(cur_chan)
                                self._pad[column + row * 8]._descriptor = str(NOTENAMES[self._pad[column + row * 8]._msg_identifier])
                                self._pad_CC[column + row * 8].set_enabled(False)
                                self._pad_CC[column + row * 8].set_channel(cur_chan)
                                if not sequencer:
                                    self._selected_scene[column + (row - 2) * 4].clip_slot(0).set_launch_button(self._pad[column + (row - 2) * 8])

                    if sequencer:
                        self.set_feedback_channels(range(cur_chan, cur_chan + 1))
                        if scale is 'DrumPad':
                            self.set_pad_translations(make_pad_translations(cur_chan))
                            self._step_sequencer.set_playhead(self._playhead_element)
                            self._step_sequencer._drum_group.set_select_button(self._button[self._layer])
                            self._step_sequencer.set_button_matrix(self._base_grid.submatrix[4:8, :4])
                            self._step_sequencer.set_drum_matrix(self._base_grid.submatrix[:4, :4])
                            vals = [-1,
                             -1,
                             -1,
                             -1,
                             0,
                             1,
                             2,
                             3,
                             -1,
                             -1,
                             -1,
                             -1,
                             4,
                             5,
                             6,
                             7,
                             -1,
                             -1,
                             -1,
                             -1,
                             8,
                             9,
                             10,
                             11,
                             -1,
                             -1,
                             -1,
                             -1,
                             12,
                             13,
                             14,
                             15]
                            for x, pad in enumerate(self._pad):
                                pad.display_press = False
                                if vals[x] > -1:
                                    pad.set_channel(cur_chan)
                                    pad.set_identifier(vals[x])
                                else:
                                    pad.set_identifier(vals[x + 4] + 16)
                                    pad.set_channel(cur_chan)

                        else:
                            self._note_sequencer.set_playhead(self._playhead_element)
                            self._note_sequencer.set_button_matrix(self._base_grid.submatrix[:8, :2])
                            for x, pad in enumerate(self._pad):
                                pad.display_press = False
                                if x < 16:
                                    pad.set_channel(cur_chan)
                                    pad.set_identifier(x)

                            self._on_note_matrix_pressed.subject = self._base_grid
                        self.reset_controlled_track()
                    else:
                        self.set_highlighting_session_component(self._selected_session)
                        self._selected_session._do_show_highlight()
                else:
                    self._send_midi(MIDIBUTTONMODE)
                    scale_len = len(SCALES[scale])
                    for row in range(4):
                        for column in range(8):
                            if scale is 'DrumPad':
                                self._pad[column + row * 8].set_identifier((DRUMNOTES[column + row * 8] + self._offsets[cur_chan]['drumoffset'] * 4) % 127)
                                self._pad[column + row * 8].scale_color = DRUMCOLORS[column < 4]
                                self._pad[column + row * 8].display_press = True
                                self._pad[column + row * 8].press_flash(0, True)
                                self._pad[column + row * 8]._descriptor = str(NOTENAMES[self._pad[column + row * 8]._msg_identifier])
                                self._pad_CC[column + row * 8].set_identifier((DRUMNOTES[column + row * 8] + self._offsets[cur_chan]['drumoffset'] * 4) % 127)
                                self._offset_component._shifted_value = 3
                            else:
                                note_pos = column + abs(3 - row) * vertoffset
                                note = offset + SCALES[scale][note_pos % scale_len] + 12 * int(note_pos / scale_len)
                                self._pad[column + row * 8].set_identifier(note % 127)
                                self._pad[column + row * 8].scale_color = KEYCOLORS[(note % 12 in WHITEKEYS) + (note_pos % scale_len == 0) * 2]
                                self._pad[column + row * 8].display_press = True
                                self._pad[column + row * 8].press_flash(0, True)
                                self._pad[column + row * 8]._descriptor = str(NOTENAMES[self._pad[column + row * 8]._msg_identifier])
                                self._pad_CC[column + row * 8].set_identifier(note % 127)
                                self._offset_component._shifted_value = 11
                            self._pad[column + row * 8].set_enabled(False)
                            self._pad[column + row * 8].set_channel(cur_chan)
                            self._pad_CC[column + row * 8].set_enabled(False)
                            self._pad_CC[column + row * 8].set_channel(cur_chan)

                if self.pad_held():
                    for index in range(len(self._last_pad_stream)):
                        self._stream_pads[index].press_flash(self._last_pad_stream[index])

            else:
                is_midi = False
        if OSC_TRANSMIT:
            self.oscServer.sendOSC(self._prefix + '/glob/scale/', str(self.generate_strip_string(scale)))
            self.oscServer.sendOSC(self._prefix + '/glob/offset/', str(self.generate_strip_string(offset)))
            self.oscServer.sendOSC(self._prefix + '/glob/vertoffset/', str(self.generate_strip_string(vertoffset)))
        return is_midi

    def _assign_midi_shift_layer(self):
        cur_track = self._mixer._selected_strip._track
        is_midi = False
        scale, offset, vertoffset = (' ', ' ', ' ')
        if cur_track.has_midi_input:
            self._send_midi(LIVEBUTTONMODE)
            if AUTO_ARM_SELECTED:
                if not cur_track.arm:
                    self.schedule_message(1, self._arm_current_track, cur_track)
            is_midi = True
            cur_chan = cur_track.current_input_sub_routing
            if len(cur_chan) == 0:
                cur_chan = 'All Channels'
            if cur_chan in CHANNELS:
                cur_chan = CHANNELS.index(cur_chan) % 15 + 1
                offset, vertoffset, scale, split, sequencer = (self._offsets[cur_chan]['offset'],
                 self._offsets[cur_chan]['vertoffset'],
                 self._offsets[cur_chan]['scale'],
                 self._offsets[cur_chan]['split'],
                 self._offsets[cur_chan]['sequencer'])
                if scale == 'Auto':
                    scale = self._detect_instrument_type(cur_track)
                if scale == 'Session':
                    is_midi = False
                elif scale == 'Mod':
                    is_midi = 'Mod'
                else:
                    for button in self._touchpad[0:1]:
                        button.set_on_off_values(SPLITMODE, 0)
                        button._descriptor = 'Split'

                    for button in self._touchpad[1:2]:
                        button.set_on_off_values(SEQUENCERMODE, 0)
                        button._descriptor = 'Seq'

                    self._sequencer_mode_selector._mode_index = int(self._offsets[cur_chan]['sequencer'])
                    self._sequencer_mode_selector.set_enabled(True)
                    self._split_mode_selector._mode_index = int(self._offsets[cur_chan]['split'])
                    self._split_mode_selector.set_enabled(True)
                    for button in self._touchpad[4:6]:
                        button.set_on_off_values(SCALEOFFSET, 0)

                    self._touchpad[4]._descriptor = '< Scale'
                    self._touchpad[5]._descriptor = 'Scale >'
                    self._scale_offset_component._offset = SCALENAMES.index(self._offsets[cur_chan]['scale'])
                    self._scale_offset_component.set_offset_change_buttons(self._touchpad[5], self._touchpad[4])
                    if scale is not 'DrumPad':
                        for button in self._touchpad[2:4]:
                            button.set_on_off_values(VERTOFFSET, 0)

                        self._touchpad[2]._descriptor = '< Vertical'
                        self._touchpad[3]._descriptor = 'Vertical >'
                        self._vertical_offset_component._offset = self._offsets[cur_chan]['vertoffset']
                        self._vertical_offset_component.set_offset_change_buttons(self._touchpad[3], self._touchpad[2])
                    if not sequencer or not split:
                        for button in self._touchpad[6:8]:
                            button.set_on_off_values(OFFSET, 0)

                        self._touchpad[6]._descriptor = '< Offset'
                        self._touchpad[7]._descriptor = 'Offset >'
                        if scale is 'Auto':
                            scale = self._detect_instrument_type(cur_track)
                        if scale is 'DrumPad':
                            if not sequencer:
                                self._offset_component._offset = self._offsets[cur_chan]['drumoffset']
                        else:
                            self._offset_component._offset = self._offsets[cur_chan]['offset']
                        self._offset_component.set_offset_change_buttons(self._touchpad[7], self._touchpad[6])
                    elif scale is 'DrumPad':
                        is_midi = 'DrumSequencer'
                        self._step_sequencer.set_drum_bank_up_button(self._touchpad[7])
                        self._touchpad[7]._descriptor = 'Bank Up'
                        self._step_sequencer.set_drum_bank_down_button(self._touchpad[6])
                        self._touchpad[6]._descriptor = 'Bank Down'
                        for pad in self._touchpad[6:8]:
                            pad.set_on_off_values(DRUMBANK, 0)

                        self._step_sequencer.set_mute_button(self._touchpad[2])
                        self._touchpad[2]._descriptor = 'Pad Mute'
                        self._touchpad[2].set_on_off_values(MUTE + 7, MUTE)
                        self._touchpad[2].turn_off()
                        self._step_sequencer.set_solo_button(self._touchpad[3])
                        self._touchpad[3]._descriptor = 'Pad Solo'
                        self._touchpad[3].set_on_off_values(SOLO + 7, SOLO)
                        self._touchpad[3].turn_off()
                        self.set_pad_translations(make_pad_translations(cur_chan))
                        self.set_feedback_channels(range(cur_chan, cur_chan + 1))
                        vals = [-1,
                         -1,
                         -1,
                         -1,
                         0,
                         1,
                         2,
                         3,
                         -1,
                         -1,
                         -1,
                         -1,
                         4,
                         5,
                         6,
                         7,
                         -1,
                         -1,
                         -1,
                         -1,
                         8,
                         9,
                         10,
                         11,
                         -1,
                         -1,
                         -1,
                         -1,
                         12,
                         13,
                         14,
                         15]
                        for x, pad in enumerate(self._pad):
                            pad.display_press = False
                            if vals[x] == -1:
                                pad.set_identifier(vals[x + 4] + 16)
                                pad.set_channel(cur_chan)

                        self._step_sequencer.set_drum_matrix(self._base_grid.submatrix[:4, :4])
                        self._step_sequencer.set_loop_selector_matrix(self._base_grid.submatrix[4:8, :2])
                        for button in self._base_grid.submatrix[4:8, :2]:
                            button._descriptor = '- L -'

                        quant_buttons = self._pad[20:24] + self._pad[28:31]
                        self._step_sequencer.set_quantization_buttons(quant_buttons)
                        for button in quant_buttons:
                            button._descriptor = ['1/32',
                             '1/32t',
                             '1/16',
                             '1/16t',
                             '1/8',
                             '1/8t',
                             '1/4',
                             '1/4t'][quant_buttons.index(button)]

                        self._step_sequencer.set_follow_button(self._pad[31])
                        self._pad[31]._descriptor = 'Follow'
                        self.reset_controlled_track()
                        self.schedule_message(2, self._step_sequencer._drum_group._update_drum_pad_leds)
                    else:
                        is_midi = 'NoteSequencer'
                        for button in self._touchpad[6:8]:
                            button.set_on_off_values(OFFSET, 0)

                        self._touchpad[6]._descriptor = '< Offset'
                        self._touchpad[7]._descriptor = 'Offset >'
                        self._offset_component._offset = self._offsets[cur_chan]['offset']
                        self._offset_component.set_offset_change_buttons(self._touchpad[7], self._touchpad[6])
                        scale_len = len(SCALES[scale])
                        current_note = self._note_sequencer._note_editor.editing_note
                        for row in range(2, 4):
                            for column in range(8):
                                note_pos = column + abs(3 - row) * int(vertoffset)
                                note = offset + SCALES[scale][note_pos % scale_len] + 12 * int(note_pos / scale_len)
                                self._pad[column + row * 8]._stored_note = note
                                if current_note is note:
                                    self._pad[column + row * 8].scale_color = SELECTED_NOTE
                                else:
                                    self._pad[column + row * 8].scale_color = KEYCOLORS[(note % 12 in WHITEKEYS) + (note_pos % scale_len == 0) * 2]

                        for pad in self._pad[16:32]:
                            pad.send_value(pad.scale_color)

                        self._on_note_matrix_pressed.subject = self._base_grid
                        self._note_sequencer.set_loop_selector_matrix(self._base_grid.submatrix[:8, :1])
                        for button in self._base_grid.submatrix[:8, :1]:
                            button._descriptor = '- L -'

                        self._note_sequencer.set_quantization_buttons(self._pad[8:15])
                        for button in self._pad[8:15]:
                            button._descriptor = ['1/32',
                             '1/32t',
                             '1/16',
                             '1/16t',
                             '1/8',
                             '1/8t',
                             '1/4',
                             '1/4t'][self._pad[8:15].index(button)]

                        self._note_sequencer.set_follow_button(self._pad[15])
                        self._pad[15]._descriptor = 'Follow'
        if OSC_TRANSMIT:
            self.oscServer.sendOSC(self._prefix + '/glob/scale/', str(self.generate_strip_string(scale)))
            self.oscServer.sendOSC(self._prefix + '/glob/offset/', str(self.generate_strip_string(offset)))
            self.oscServer.sendOSC(self._prefix + '/glob/vertoffset/', str(self.generate_strip_string(vertoffset)))
        return is_midi

    def _notify_descriptors(self):
        if OSC_TRANSMIT:
            for pad in self._pad:
                self.oscServer.sendOSC(self._prefix + '/' + pad.name + '/lcd_name/', str(self.generate_strip_string(pad._descriptor)))

            for touchpad in self._touchpad:
                self.oscServer.sendOSC(self._prefix + '/' + touchpad.name + '/lcd_name/', str(self.generate_strip_string(touchpad._descriptor)))

            for button in self._button:
                self.oscServer.sendOSC(self._prefix + '/' + button.name + '/lcd_name/', str(self.generate_strip_string(button._descriptor)))

    def _current_device_offsets(self, dict_entry):
        selected_device = self._top_device()
        if selected_device is not None and hasattr(selected_device, 'name'):
            name = selected_device.name
            self.log_message('device name: ' + str(name.split(' ')))
            for item in name.split(' '):
                if len(str(item)) and str(item)[0] == '@':
                    vals = item[1:].split(':')
                    if len(vals) < 2:
                        def_assignments = {'scale': 'Auto',
                         'sequencer': False,
                         'split': False,
                         'offset': 36,
                         'vertoffset': 4,
                         'drumoffset': 0}
                        if vals[0] in def_assignments:
                            vals.append([vals[0]])
                    if vals[0] in dict_entry.keys():
                        if vals[0] == 'scale' and vals[1] in SCALES.keys():
                            dict_entry[vals[0]] = str(vals[1])
                        elif vals[0] in ('sequencer', 'split'):
                            if vals[1] in ('False', 'True'):
                                dict_entry[vals[0]] = bool(['False', 'True'].index(vals[1]))
                        elif vals[0] in ('offset', 'vertoffset', 'drumoffset'):
                            dict_entry[vals[0]] = int(vals[1])

        return dict_entry

    def _set_device_attribute(self, device, attribute, value, force = False):
        if device is not None and hasattr(device, 'name'):
            name = device.name.split(' ')
            for index in range(len(name)):
                if len(str(name[index])) and str(name[index][0]) == '@':
                    vals = name[index][1:].split(':')
                    if vals[0] == attribute:
                        name[index] = str('@' + str(attribute) + ':' + str(value))
                        device.name = ' '.join(name)

    def _top_device(self):
        selected_device = self._device._device
        if selected_device is not None and hasattr(selected_device, 'canonical_parent'):
            while not isinstance(selected_device.canonical_parent, Live.Track.Track):
                selected_device = selected_device.canonical_parent

        return selected_device

    def _arm_current_track(self, track):
        track.arm = 1

    def _disarm_track(self, track):
        track.arm = 0

    def _assign_alternate_mappings(self, chan = 0):
        self._send_midi(MIDIBUTTONMODE)
        for pad in self._touchpad:
            pad.use_default_message()
            pad.set_channel(chan)
            pad.set_enabled(False)
            pad.reset()

        for pad in self._pad:
            pad.use_default_message()
            pad.set_channel(chan)
            pad.set_enabled(False)

        for pad in self._pad_CC:
            pad.release_parameter()
            pad.set_channel(chan)
            pad.set_enabled(False)

        for pad in self._touchpad:
            pad.use_default_message()
            pad.set_channel(chan)
            pad.set_enabled(chan is 0)

        for fader in self._fader[0:8]:
            fader.use_default_message()
            fader.set_channel(chan)
            fader.set_enabled(False)

        self.request_rebuild_midi_map()

    def _detect_instrument_type(self, track):
        scale = DEFAULT_AUTO_SCALE
        if self._assign_mod():
            scale = 'Mod'
        else:
            for device in track.devices:
                if isinstance(device, Live.Device.Device):
                    if device.class_name == 'DrumGroupDevice':
                        scale = 'DrumPad'
                        self._step_sequencer.set_drum_group_device(device)
                        break

        return scale

    def _get_devices(self, track):

        def dig(container_device):
            contained_devices = []
            if container_device.can_have_chains:
                for chain in container_device.chains:
                    for chain_device in chain.devices:
                        for item in dig(chain_device):
                            contained_devices.append(item)

            else:
                contained_devices.append(container_device)
            return contained_devices

        devices = []
        for device in track.devices:
            for item in dig(device):
                devices.append(item)

        return devices

    def _is_mod(self, device):
        mod_device = None
        if is_device(device):
            if device.can_have_chains:
                if not device.can_have_drum_pads:
                    if len(device.view.selected_chain.devices) > 0:
                        device = device.view.selected_chain.devices[0]
            if self.monomodular and self.monomodular._mods:
                for mod in self.monomodular._mods:
                    if mod.device == device:
                        mod_device = mod
                        break

        return mod_device

    def _assign_mod(self):
        mod = self._is_mod(self._device._device)
        if mod is not None:
            self._send_midi(MIDIBUTTONMODE)
            self.modhandler._assign_base_grid(self._base_grid)
            self.modhandler._assign_base_grid_CC(self._base_grid_CC)
            self.modhandler.set_shift_button(self._button[self._layer])
            self.modhandler.set_device_component(self._device)
            if self.shift_pressed():
                self.modhandler._assign_keys(self._keys)
            else:
                self.modhandler._assign_keys(self._keys_display)
                if self._layer == 2:
                    self.modhandler._fader_color_override = True
        self.modhandler.select_mod(mod)
        return mod is not None

    def _assign_notes_per_scale(self, cur_chan):
        offset, vertoffset, scale, split = (self._offsets[cur_chan]['offset'],
         self._offsets[cur_chan]['vertoffset'],
         self._offsets[cur_chan]['scale'],
         self._offsets[cur_chan]['split'])
        if scale is 'Auto':
            scale = self._detect_instrument_type(cur_chan)
        if scale is 'Drumpad':
            for index in range(16):
                self._pad[index].set_enabled(False)
                self._pad[index].set_identifier((DRUMNOTES[index] + self._offsets[cur_chan]['drumoffset'] * 4) % 127)
                self._pad[index].set_channel(cur_chan)
                self._pad[index].send_value(DRUMCOLORS[index % 8 < 4], True)
                self._scene[int(index / 4)].clip_slot(index % 4).set_launch_button(self._pad[(index + 4) % 8])

        elif scale in SPLIT_SCALES or split:
            scale_len = len(SCALES[scale])
            for row in range(4):
                for column in range(4):
                    note_pos = column + abs(3 - row) * int(vertoffset / 2)
                    note = offset + SCALES[scale][note_pos % scale_len] + 12 * int(note_pos / scale_len)
                    self._pad[column + row * 8].set_enabled(False)
                    self._pad[column + row * 8].set_identifier(note)
                    self._pad[column + row * 8].set_channel(cur_chan)
                    self._pad[column + row * 8].send_value(KEYCOLORS[note % 12 in WHITEKEYS] + int(note % 12 == 0), True)
                    self._scene[row].clip_slot(column + 4).set_launch_button(self._pad[column + 4 + row * 8])

        else:
            scale_len = len(SCALES[scale])
            for row in range(4):
                for column in range(8):
                    note_pos = column + abs(3 - row) * vertoffset
                    note = offset + SCALES[scale][note_pos % scale_len] + 12 * int(note_pos / scale_len)
                    self._pad[column + row * 8].set_enabled(False)
                    self._pad[column + row * 8].set_identifier(note)
                    self._pad[column + row * 8].set_channel(cur_chan)
                    self._pad[column + row * 8].send_value(KEYCOLORS[note % 12 in WHITEKEYS] + int(note % 12 == 0), True)

    def _display_chars(self, char1 = None, char2 = None):
        if char1 in _base_translations:
            self._send_midi((176, 34, _base_translations[char1]))
        if char2 in _base_translations:
            self._send_midi((176, 35, _base_translations[char2]))

    def _display_mode(self):
        char1 = ['L',
         'S',
         'D',
         'U'][self._layer]
        char2 = '-'
        if self.shift_pressed():
            char2 = str(self._layer + 1)
        elif self.select_pressed():
            char2 = 'S'
        elif self._layer is 3:
            char2 = str(self._user_mode_selector._mode_index + 1)
        self._display_chars(char1, char2)
        if OSC_TRANSMIT:
            self.oscServer.sendOSC(self._prefix + '/glob/mode/', str(self.generate_strip_string(['Launch',
             'Sends',
             'Device',
             'User'][self._layer])))

    def _register_pad_pressed(self, bytes):
        raise len(bytes) is 8 or AssertionError
        decoded = []
        for i in range(0, 8):
            bin = bytes[i]
            for index in range(0, 4):
                decoded.append(bin & 1)
                bin = bin >> 1

        self._last_pad_stream = decoded
        for index in range(len(decoded)):
            self._stream_pads[index].press_flash(decoded[index])

    @subject_slot('value')
    def _on_duplicate_button_value(self, value):
        track = self._mixer.selected_strip()._track
        if value is not 0 and track is not None:
            try:
                track.duplicate_clip_slot([ s for s in self.song().scenes ].index(self.song().view.selected_scene))
            except:
                self.log_message('couldnt duplicate')
                self.log_message('because: ' + str([ s for s in self.song().scenes ].index(self.song().view.selected_scene)))

    @subject_slot('value')
    def _on_new_button_value(self, value):
        song = self.song()
        view = song.view
        try:
            selected_track = view.selected_track
            selected_scene_index = list(song.scenes).index(view.selected_scene)
            selected_track.stop_all_clips(False)
            self._jump_to_next_slot(selected_track, selected_scene_index)
        except:
            self.log_message('couldnt create new')

    def _jump_to_next_slot(self, track, start_index):
        song = self.song()
        new_scene_index = self._next_empty_slot(track, start_index)
        song.view.selected_scene = song.scenes[new_scene_index]

    def _next_empty_slot(self, track, scene_index):
        song = self.song()
        scene_count = len(song.scenes)
        while track.clip_slots[scene_index].has_clip:
            scene_index += 1
            if scene_index == scene_count:
                song.create_scene(scene_count)

        return scene_index

    @subject_slot('value')
    def _on_nav_button_value(self, value, x, y, is_momentary):
        button = self._nav_buttons.get_button(x, y)
        if button in self._current_nav_buttons:
            if value > 0:
                self._send_midi((176, 35, DIRS[self._current_nav_buttons.index(button)]))
            else:
                self._display_mode()

    @subject_slot('value')
    def _on_duplicate_clip_value(self, value, x, y, is_momentary):
        pass

    @subject_slot('value')
    def _on_clip_fired(self, *a, **k):
        pass

    def update_display(self):
        super(Base, self).update_display()
        self._timer = (self._timer + 1) % 256
        self.flash()

    def flash(self):
        if self.flash_status > 0:
            for control in self.controls:
                if isinstance(control, MonoButtonElement):
                    control.flash(self._timer)

    def _on_device_name_changed(self):
        name = self._device.device_name_data_source().display_string()
        self._monobridge._send('Device_Name', 'lcd_name', str(self.generate_strip_string('Device')))
        self._monobridge._send('Device_Name', 'lcd_value', str(self.generate_strip_string(name)))
        self.touched()
        if OSC_TRANSMIT:
            self.oscServer.sendOSC(self._prefix + '/glob/device/', str(self.generate_strip_string(name)))

    def _on_device_bank_changed(self):
        name = 'No Bank'
        if is_device(self._device._device):
            name, _ = self._device._current_bank_details()
        self._monobridge._send('Device_Bank', 'lcd_name', str(self.generate_strip_string('Bank')))
        self._monobridge._send('Device_Bank', 'lcd_value', str(self.generate_strip_string(name)))
        self.touched()

    def _on_device_chain_changed(self):
        name = ' '
        if is_device(self._device._device) and self._device._device.canonical_parent and isinstance(self._device._device.canonical_parent, Live.Chain.Chain):
            name = self._device._device.canonical_parent.name
        self._monobridge._send('Device_Chain', 'lcd_name', str(self.generate_strip_string('Chain')))
        self._monobridge._send('Device_Chain', 'lcd_value', str(self.generate_strip_string(name)))
        self.touched()

    def generate_strip_string(self, display_string):
        NUM_CHARS_PER_DISPLAY_STRIP = 12
        if not display_string:
            return ' ' * NUM_CHARS_PER_DISPLAY_STRIP
        else:
            display_string = str(display_string)
        if len(display_string.strip()) > NUM_CHARS_PER_DISPLAY_STRIP - 1 and display_string.endswith('dB') and display_string.find('.') != -1:
            display_string = display_string[:-2]
        if len(display_string) > NUM_CHARS_PER_DISPLAY_STRIP - 1:
            for um in [' ',
             'i',
             'o',
             'u',
             'e',
             'a']:
                while len(display_string) > NUM_CHARS_PER_DISPLAY_STRIP - 1 and display_string.rfind(um, 1) != -1:
                    um_pos = display_string.rfind(um, 1)
                    display_string = display_string[:um_pos] + display_string[um_pos + 1:]

        else:
            display_string = display_string.center(NUM_CHARS_PER_DISPLAY_STRIP - 1)
        ret = u''
        for i in range(NUM_CHARS_PER_DISPLAY_STRIP - 1):
            if ord(display_string[i]) > 127 or ord(display_string[i]) < 0:
                ret += ' '
            else:
                ret += display_string[i]

        ret += ' '
        ret = ret.replace(' ', '_')
        raise len(ret) == NUM_CHARS_PER_DISPLAY_STRIP or AssertionError
        return ret

    def notification_to_bridge(self, name, value, sender):
        if isinstance(sender, MonoEncoderElement):
            if OSC_TRANSMIT:
                self.oscServer.sendOSC(self._prefix + '/' + sender.name + '/lcd_name/', str(self.generate_strip_string(name)))
                self.oscServer.sendOSC(self._prefix + '/' + sender.name + '/lcd_value/', str(self.generate_strip_string(value)))
            self._monobridge._send(sender.name, 'lcd_name', str(self.generate_strip_string(name)))
            self._monobridge._send(sender.name, 'lcd_value', str(self.generate_strip_string(value)))
        else:
            self._monobridge._send(name, 'lcd_name', str(self.generate_strip_string(name)))
            self._monobridge._send(name, 'lcd_value', str(self.generate_strip_string(value)))
            if OSC_TRANSMIT:
                self.oscServer.sendOSC(self._prefix + '/' + name + '/lcd_name/', str(self.generate_strip_string(name)))
                self.oscServer.sendOSC(self._prefix + '/' + name + '/lcd_value/', str(self.generate_strip_string(value)))

    def touched(self):
        if self._touched is 0:
            self._monobridge._send('touch', 'on')
            self.schedule_message(2, self.check_touch)
        self._touched += 1

    def check_touch(self):
        if self._touched > 5:
            self._touched = 5
        elif self._touched > 0:
            self._touched -= 1
        if self._touched is 0:
            self._monobridge._send('touch', 'off')
        else:
            self.schedule_message(2, self.check_touch)

    def disconnect(self):
        self._deassign_all()
        self._send_midi(STREAMINGOFF)
        if self._last_selected_track is not None:
            if self._last_selected_track.current_input_sub_routing_has_listener(self._on_selected_track_midi_subrouting_changed):
                self._last_selected_track.remove_current_input_sub_routing_listener(self._on_selected_track_midi_subrouting_changed)
        if self.oscServer is not None:
            self.oscServer.shutdown()
        self.oscServer = None
        self.log_message('--------------= Base log closed =--------------')
        super(Base, self).disconnect()

    def _on_new_device_set(self):
        if self._layer in (1, 2):
            self._shift_update(self._layer, self.shift_pressed())
        self._on_device_bank_changed()
        self._on_device_chain_changed()
        if self._device._device is not None and self._device._device.can_have_drum_pads:
            self._step_sequencer.set_drum_group_device(self._device._device)

    def _on_selected_track_changed(self):
        super(Base, self)._on_selected_track_changed()
        track = self._mixer.selected_strip()._track
        track_list = []
        for t in self._mixer.tracks_to_use():
            track_list.append(t)

        if track in track_list:
            self._selected_session._track_offset = track_list.index(track)
        self._selected_session._reassign_tracks()
        self._selected_session._reassign_scenes()
        if self._last_selected_track and self._last_selected_track.can_be_armed and not self._last_selected_track_arm:
            self.schedule_message(1, self._disarm_track, self._last_selected_track)
        if track.can_be_armed:
            self._last_selected_track_arm = track.arm
        if self._last_selected_track is not None and isinstance(self._last_selected_track, Live.Track.Track) and self._last_selected_track in track_list:
            if self._last_selected_track.current_input_sub_routing_has_listener(self._on_selected_track_midi_subrouting_changed):
                self._last_selected_track.remove_current_input_sub_routing_listener(self._on_selected_track_midi_subrouting_changed)
        self._last_selected_track = track
        if track is not None:
            track.add_current_input_sub_routing_listener(self._on_selected_track_midi_subrouting_changed)
        if not self.pad_held():
            if self._layer in (1, 2):
                self._deassign_all()
                self._layers[self._layer]()
        else:
            self.schedule_message(2, self._on_selected_track_changed)
        self.reset_controlled_track()

    def reset_controlled_track(self, mode = None):
        self.set_controlled_track(self.song().view.selected_track)

    def _on_track_list_changed(self):
        super(Base, self)._on_track_list_changed()

    def _on_selected_track_midi_subrouting_changed(self):
        if self._layer in (1, 2):
            self._deassign_all()
            self._layers[self._layer]()

    def connect_script_instances(self, instanciated_scripts):
        with self.component_guard():
            self._setup_mod()

    def set_highlighting_session_component(self, session_component):
        self._highlighting_session_component = session_component
        self._highlighting_session_component.set_highlighting_callback(self._set_session_highlight)

    def handle_sysex(self, midi_bytes):
        if len(midi_bytes) > 14:
            if midi_bytes[:6] == tuple([240,
             0,
             1,
             97,
             12,
             64]):
                self._register_pad_pressed(midi_bytes[6:14])
            elif midi_bytes[3:10] == tuple([6,
             2,
             0,
             1,
             97,
             1,
             0]):
                if not self._connected:
                    self._connected = True
                    self._initialize_hardware()

    def _device_update(self, device):

        def _update():
            BaseDeviceComponent.update(device)
            self.request_rebuild_midi_map()

        return _update

    def set_pad_translations(self, pad_translations):
        if not pad_translations == self._pad_translations:
            self._pad_translations = None
            super(Base, self).set_pad_translations(pad_translations)