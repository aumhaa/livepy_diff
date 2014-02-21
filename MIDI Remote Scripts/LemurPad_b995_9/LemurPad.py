#Embedded file name: /Applications/Ableton Live 9 Beta.app/Contents/App-Resources/MIDI Remote Scripts/LemurPad_b995_9/LemurPad.py
from __future__ import with_statement
import Live
import time
import math
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.NotifyingControlElement import NotifyingControlElement
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.SliderElement import SliderElement
from _Framework.TrackEQComponent import TrackEQComponent
from _Framework.TrackFilterComponent import TrackFilterComponent
from _Framework.TransportComponent import TransportComponent
from _Generic.Devices import *
from _Mono_Framework.MonoBridgeElement import MonoBridgeElement
from _Mono_Framework.MonoButtonElement import MonoButtonElement
from _Mono_Framework.MonoEncoderElement import MonoEncoderElement
from _Mono_Framework.DeviceSelectorComponent import DeviceSelectorComponent
from _Mono_Framework.ResetSendsComponent import ResetSendsComponent
from _Mono_Framework.DetailViewControllerComponent import DetailViewControllerComponent
from _Mono_Framework.MonomodComponent import MonomodComponent
from _Mono_Framework.LiveUtils import *
from SpecialMonomodComponent import SpecialMonomodComponent
from MonOhm_b995_9.MonOhm import MonOhm
from MonOhm_b995_9.Map import *
from Map import *

class OSCMonoButtonElement(MonoButtonElement):

    def __init__(self, is_momentary, msg_type, channel, identifier, name, osc, osc_alt, osc_name, cs, *a, **k):
        super(OSCMonoButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, name, cs, *a, **k)
        self.osc = osc
        self.osc_alt = osc_alt
        self.osc_name = osc_name
        self._value = 0
        self._last_sent = -1
        self._color_map = [7,
         1,
         3,
         2,
         6,
         5,
         4]
        self._script._monobridge._send_osc(self.osc, 0, True)

    def send_midi(self, message):
        if not message != None:
            raise AssertionError
            if not isinstance(message, tuple):
                raise AssertionError
                color = message[2] != self._last_sent and message[2] == 127 and 7
            else:
                color = int(message[2])
            self._script._monobridge._send_osc(str(self.osc_alt), color)
        self._last_sent = message[2]

    def set_value(self, value):
        if self._parameter_to_map_to != None:
            newval = float(value * (self._parameter_to_map_to.max - self._parameter_to_map_to.min)) + self._parameter_to_map_to.min
            self._parameter_to_map_to.value = newval
            return [value, str(self.mapped_parameter())]
        self.receive_value(int(value != 0))


class OSCMonoEncoderElement(MonoEncoderElement):

    def __init__(self, msg_type, channel, identifier, map_mode, name, num, osc, osc_parameter, osc_name, script, *a, **k):
        super(OSCMonoEncoderElement, self).__init__(msg_type, channel, identifier, map_mode, name, num, script, *a, **k)
        self.osc = osc
        self.osc_parameter = osc_parameter
        self.osc_name = osc_name
        self._mapping_feedback_delay = 0
        self._timer = 0
        self._threshold = 0
        self._script._monobridge._send_osc(self.osc, 0, True)

    def set_value(self, value):
        MonoEncoderElement.set_value(self, value)
        self._timer = self._script._timer

    def forward_parameter_value(self):
        if type(self._parameter) is not type(None):
            try:
                parameter = str(self.mapped_parameter())
            except:
                parameter = ' '

            if parameter != self._parameter_last_value:
                try:
                    self._parameter_last_value = str(self.mapped_parameter())
                except:
                    self._parameter_last_value = ' '

                self._script._monobridge._send_osc(self.osc_parameter, self._script.generate_strip_string(self._parameter_last_value), True, True)
                if self._timer + self._threshold < self._script._timer:
                    new_value = float((self._parameter.value - self._parameter.min) / (self._parameter.max - self._parameter.min))
                    self._script._monobridge._send_osc(self.osc, new_value)
                    self._script.log_message(str(self._timer) + ' ' + str(self._script._timer) + ' ' + str(new_value))

    def forward_parameter_name(self):
        if type(self._parameter) is not type(None):
            parameter = self._parameter
            if parameter:
                if isinstance(parameter, Live.DeviceParameter.DeviceParameter):
                    if str(parameter.original_name) == 'Track Volume' or self._mapped_to_midi_velocity is True:
                        self._parameter_lcd_name = str(parameter.canonical_parent.canonical_parent.name)
                    elif str(parameter.original_name) == 'Track Panning':
                        self._parameter_lcd_name = 'Pan'
                    else:
                        self._parameter_lcd_name = str(parameter.name)
                self._script._monobridge._send_osc(self.osc_name, self._script.generate_strip_string(self._parameter_lcd_name), False, True)

    def add_parameter_listener(self, parameter):
        self._parameter = parameter
        if parameter:
            if isinstance(parameter, Live.DeviceParameter.DeviceParameter):
                if str(parameter.original_name) == 'Track Volume' or self._mapped_to_midi_velocity is True:
                    self._parameter_lcd_name = str(parameter.canonical_parent.canonical_parent.name)
                    cbb = lambda : self.forward_parameter_name()
                    parameter.canonical_parent.canonical_parent.add_name_listener(cbb)
                elif str(parameter.original_name) == 'Track Panning':
                    self._parameter_lcd_name = 'Pan'
                else:
                    self._parameter_lcd_name = str(parameter.name)
            try:
                self._parameter_last_value = str(self.mapped_parameter())
            except:
                self._parameter_last_value = ' '

            self._script._monobridge._send_osc(self.osc_name, self._script.generate_strip_string(self._parameter_lcd_name), False, True)
            self._script._monobridge._send_osc(self.osc_parameter, self._script.generate_strip_string(self._parameter_last_value), False, True)
            new_value = float((self._parameter.value - self._parameter.min) / (self._parameter.max - self._parameter.min))
            self._script._monobridge._send_osc(self.osc, new_value)
            cb = lambda : self.forward_parameter_value()
            parameter.add_value_listener(cb)

    def remove_parameter_listener(self, parameter):
        self._parameter = None
        if parameter:
            cb = lambda : self.forward_parameter_value()
            cbb = lambda : self.forward_parameter_name()
            if parameter.value_has_listener is True:
                parameter.remove_value_listener(cb)
            if isinstance(parameter, Live.DeviceParameter.DeviceParameter):
                if str(parameter.original_name) == 'Track Volume' or self._mapped_to_midi_velocity is True:
                    if parameter.canonical_parent.canonical_parent.name_has_listener is True:
                        parameter.canonical_parent.canonical_parent.remove_name_listener(cbb)
            self._parameter_lcd_name = ' '
            self._parameter_last_value = ' '
            self._script._monobridge._send_osc(self.osc, 0)
            self._script._monobridge._send_osc(self.osc_name, '`_', False, True)
            self._script._monobridge._send_osc(self.osc_parameter, '`_', False, True)


class NameServerClipSlotComponent(ClipSlotComponent):

    def __init__(self, script, *a, **k):
        self._script = script
        super(NameServerClipSlotComponent, self).__init__(*a, **k)
        self._on_name_changed_slot = self.register_slot(None, self._name_listener, 'name')

    def set_clip_slot(self, clip_slot):
        if not (clip_slot == None or isinstance(clip_slot, Live.ClipSlot.ClipSlot)):
            raise AssertionError
            clip = clip_slot != None and clip_slot.clip
        else:
            clip = None
        self._on_name_changed_slot.subject = clip
        super(NameServerClipSlotComponent, self).set_clip_slot(clip_slot)

    def _name_listener(self):
        self._script.log_message('_name_listener')
        self.update()

    def update(self):
        super(NameServerClipSlotComponent, self).update()
        new_name = ' '
        if self._allow_updates:
            if self.is_enabled() and not self._launch_button_value_slot.subject == None:
                if self._clip_slot != None:
                    if self.has_clip():
                        new_name = self._clip_slot.clip.name
                self._script.clip_name(self._launch_button_value_slot.subject, new_name)


class NameServerSceneComponent(SceneComponent):
    """         Override for SceneComponent that provides Clip NameServer support """

    def __init__(self, script, num_slots, tracks_to_use_callback, *a, **k):
        self._script = script
        super(NameServerSceneComponent, self).__init__(num_slots, tracks_to_use_callback, *a, **k)

    def _create_clip_slot(self):
        return NameServerClipSlotComponent(self._script)


class NameServerSessionComponent(SessionComponent):
    """ Override for SessionComponent that provides Clip NameServer support """

    def __init__(self, num_tracks, num_scenes, script, *a, **k):
        self._script = script
        super(NameServerSessionComponent, self).__init__(num_tracks, num_scenes, *a, **k)

    def _create_scene(self):
        return NameServerSceneComponent(self._script, num_slots=self._num_tracks, tracks_to_use_callback=self.tracks_to_use)


class OSCMonoBridgeElement(MonoBridgeElement):

    def __init__(self, *a, **k):
        super(OSCMonoBridgeElement, self).__init__(*a, **k)
        self.bridge = 'None'
        self._page_str = '/2'
        self._elapsed_events = 0
        self._threshold = 50
        self._buffer = []
        self._device = None
        self._device_parent = None
        self._connected = False
        self._script._register_timer_callback(self._send_buffer)

    def _is_connected(self):
        return self._connected

    def connect_to(self, device):
        self._connected = True
        self._script.connected = 1
        self.device = device
        if self._device_parent != None:
            if self._device_parent.devices_has_listener(self._device_listener):
                self._device_parent.remove_devices_listener(self._device_listener)
        self._device_parent = device.canonical_parent
        if not self._device_parent.devices_has_listener(self._device_listener):
            self._device_parent.add_devices_listener(self._device_listener)

    def _disconnect_client(self):
        if self._device_parent != None:
            if self._device_parent.devices_has_listener(self._device_listener):
                self._device_parent.remove_devices_listener(self._device_listener)
        self._connected = False
        self._script.connected = 0

    def _device_listener(self):
        if self.device == None:
            self._disconnect_client()

    def reset(self):
        pass

    def osc_in(self, messagename, arguments = None):
        if self._script._osc_registry.has_key(messagename):
            self._script._osc_registry[messagename](arguments)
        else:
            self._script.log_message(str(messagename) + ' : ' + str(arguments))

    def osc_extra(self, messagename):
        pass

    def _send_osc(self, osc, value, force = False, name = False):
        if osc != None:
            self._elapsed_events += 1
            if self._elapsed_events < self._threshold:
                if name == True:
                    self._send('name', osc, value)
                else:
                    self._send('osc', osc, value)
            else:
                self._buffer.append([osc, value, name])

    def _send_buffer(self):
        for index in range(min(len(self._buffer), self._threshold)):
            if self._buffer[0][2] == True:
                self._send('name', self._buffer[0][0], self._buffer[0][1])
            else:
                self._send('osc', self._buffer[0][0], self._buffer[0][1])
            self._buffer.pop(0)

        self._elapsed_events = 0

    def ping(self, message):
        if self._connected is False:
            self._send('page', self._page_str)
            self._connected = True
            self._script.refresh_state()

    def page1(self, message):
        self._page_str = '/1'

    def page2(self, message):
        self._page_str = '/2'

    def reset_grid(self):
        self._script._key_buttons.reset()
        self._script._bank_buttons.reset()

    def set_brightness(self, value):
        self._script._set_brightness(value)

    def set_threshold(self, value):
        self._threshold = int(value)


class LemurPad(MonOhm):
    __module__ = __name__
    __doc__ = ' Lemur version of the MonOhm companion controller script '

    def __init__(self, *a, **k):
        self._timer_callbacks = []
        self._osc_registry = {}
        self._display_button_names = DISPLAY_BUTTON_NAMES
        super(LemurPad, self).__init__(*a, **k)
        self._host_name = 'LemurPad'
        self._color_type = 'AumPad'
        self.connected = 0
        with self.component_guard():
            self._setup_touchosc()
            self._assign_host2()
            self._assign_session_colors()

    def query_ohm(self):
        pass

    def _setup_monobridge(self):
        self._monobridge = OSCMonoBridgeElement(self)
        self._monobridge.name = 'MonoBridge'

    def _setup_controls(self):
        is_momentary = True
        self._fader = [ None for index in range(8) ]
        self._dial = [ None for index in range(16) ]
        self._button = [ None for index in range(8) ]
        self._menu = [ None for index in range(6) ]
        for index in range(8):
            self._fader[index] = OSCMonoEncoderElement(MIDI_CC_TYPE, CHANNEL, OHM_FADERS[index], Live.MidiMap.MapMode.absolute, 'Fader_' + str(index), index, '/Fader_' + str(index) + '/x', '/Strip' + str(index + 8) + '/set', '/Strip' + str(index) + '/set', self)

        for index in range(8):
            self._button[index] = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, OHM_BUTTONS[index], 'Button_' + str(index), '/Select_' + str(index) + '/value', '/Select/set ' + str(index), '/Select/text ' + str(index), self)

        for index in range(16):
            self._dial[index] = OSCMonoEncoderElement(MIDI_CC_TYPE, CHANNEL, OHM_DIALS[index], Live.MidiMap.MapMode.absolute, 'Dial_' + str(index), index + 8, '/Dial_' + str(index) + '/x', '/Dial' + str(index) + 'val/set', '/Dial' + str(index) + 'name/set', self)

        for index in range(6):
            self._menu[index] = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, OHM_MENU[index], 'Menu_' + str(index), '/Function_' + str(index) + '/value', '/Function/set ' + str(index), '/Function/text ' + str(index), self)

        self._crossfader = OSCMonoEncoderElement(MIDI_CC_TYPE, CHANNEL, CROSSFADER, Live.MidiMap.MapMode.absolute, 'Crossfader', 24, '/XFader/x', '/XFader/none', None, self)
        self._livid = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, LIVID, 'Livid_Button', '/Livid/x', '/Livid/x', None, self)
        self._shift_l = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, SHIFT_L, 'Shift_Button_Left', '/ShiftL/x', '/ShiftL/x', None, self)
        self._shift_r = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, SHIFT_R, 'Shift_Button_Right', '/ShiftR/x', '/ShiftR/x', None, self)
        self._matrix = ButtonMatrixElement()
        self._matrix.name = 'Matrix'
        self._monomod = ButtonMatrixElement()
        self._monomod.name = 'Monomod'
        self._grid = [ None for index in range(8) ]
        for column in range(8):
            self._grid[column] = [ None for index in range(8) ]
            for row in range(8):
                self._grid[column][row] = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, column * 8 + row, 'Grid_' + str(column) + '_' + str(row), '/ClipGrid_' + str(column) + '_' + str(row) + '/value', '/ClipGrid/set ' + str(column) + ' ' + str(row), '/ClipGrid/text ' + str(column) + ' ' + str(row), self)

        for row in range(5):
            button_row = []
            for column in range(7):
                button_row.append(self._grid[column][row])

            self._matrix.add_row(tuple(button_row))

        for row in range(8):
            button_row = []
            for column in range(8):
                button_row.append(self._grid[column][row])

            self._monomod.add_row(tuple(button_row))

        self._dummy_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 125)
        self._dummy_button.name = 'Dummy1'
        self._dummy_button2 = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 126)
        self._dummy_button2.name = 'Dummy2'
        self._dummy_button3 = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, 127)
        self._dummy_button2.name = 'Dummy3'
        self._monomod256 = ButtonMatrixElement()
        self._monomod256.name = 'Monomod256'
        self._square = [ None for index in range(16) ]
        for column in range(16):
            self._square[column] = [ None for index in range(16) ]
            for row in range(16):
                self._square[column][row] = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, int(column / 8) + 1, row + column % 8 * 16, '256Grid_' + str(column) + '_' + str(row), '/Grid_' + str(column) + '_' + str(row) + '/value', '/Grid/set ' + str(column) + ' ' + str(row), None, self)

        for row in range(16):
            button_row = []
            for column in range(16):
                button_row.append(self._square[column][row])

            self._monomod256.add_row(tuple(button_row))

        self._bank_buttons = ButtonMatrixElement()
        self._key_buttons = ButtonMatrixElement()
        self._bank_button = [ None for index in range(2) ]
        for index in range(2):
            self._bank_button[index] = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, index, '256Grid_Bank_' + str(index), '/Shift_' + str(index) + '/value', '/Shift/set ' + str(index), None, self)

        button_row = []
        for index in range(2):
            button_row.append(self._bank_button[index])

        self._bank_buttons.add_row(tuple(button_row))
        button_row = []
        self._key_button = [ None for index in range(8) ]
        for index in range(8):
            self._key_button[index] = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, index + 8, '256Grid_Key_' + str(index), '/Keys_' + str(index) + '/value', '/Keys/set ' + str(index), None, self)

        for index in range(8):
            button_row.append(self._key_button[index])

        self._key_buttons.add_row(tuple(button_row))
        self._pedal = [ None for index in range(8) ]
        if self._use_pedal is True:
            for index in range(8):
                self._pedal[index] = EncoderElement(MIDI_CC_TYPE, 0, 25 + index, Live.MidiMap.MapMode.absolute)
                self._pedal[index].name = 'Pedal_' + str(index)
                self._pedal[index]._report = False

    def _setup_session_control(self):
        is_momentary = True
        num_tracks = 4
        num_scenes = 5
        self._session = NameServerSessionComponent(num_tracks, num_scenes, self)
        self._session.name = 'Left_Session'
        self._session.set_offsets(0, 0)
        self._session.set_stop_track_clip_value(self._color_defs['STOP_CLIP'])
        self._scene = [ None for index in range(5) ]
        for row in range(num_scenes):
            self._scene[row] = self._session.scene(row)
            self._scene[row].name = 'L_Scene_' + str(row)
            for column in range(num_tracks):
                clip_slot = self._scene[row].clip_slot(column)
                clip_slot.name = str(column) + '_Clip_Slot_L_' + str(row)
                clip_slot.set_triggered_to_play_value(self._color_defs['CLIP_TRG_PLAY'])
                clip_slot.set_triggered_to_record_value(self._color_defs['CLIP_TRG_REC'])
                clip_slot.set_stopped_value(self._color_defs['CLIP_STOP'])
                clip_slot.set_started_value(self._color_defs['CLIP_STARTED'])
                clip_slot.set_recording_value(self._color_defs['CLIP_RECORDING'])

        self._session.set_mixer(self._mixer)
        self._session_zoom = SessionZoomingComponent(self._session)
        self._session_zoom.name = 'L_Session_Overview'
        self._session_zoom.set_stopped_value(self._color_defs['ZOOM_STOPPED'])
        self._session_zoom.set_playing_value(self._color_defs['ZOOM_PLAYING'])
        self._session_zoom.set_selected_value(self._color_defs['ZOOM_SELECTED'])
        self._session_zoom._zoom_button = self._dummy_button
        self._session_zoom.set_enabled(True)
        self._session2 = SessionComponent(num_tracks, num_scenes)
        self._session2.name = 'Right_Session'
        self._session2.set_offsets(4, 0)
        self._session2.set_stop_track_clip_value(self._color_defs['STOP_CLIP'])
        self._scene2 = [ None for index in range(5) ]
        for row in range(num_scenes):
            self._scene2[row] = self._session2.scene(row)
            self._scene2[row].name = 'R_Scene_' + str(row)
            for column in range(num_tracks):
                clip_slot = self._scene2[row].clip_slot(column)
                clip_slot.name = str(column) + '_Clip_Slot_R_' + str(row)
                clip_slot.set_triggered_to_play_value(self._color_defs['CLIP_TRG_PLAY'])
                clip_slot.set_triggered_to_record_value(self._color_defs['CLIP_TRG_REC'])
                clip_slot.set_stopped_value(self._color_defs['CLIP_STOP'])
                clip_slot.set_started_value(self._color_defs['CLIP_STARTED'])
                clip_slot.set_recording_value(self._color_defs['CLIP_RECORDING'])

        self._session2.set_mixer(self._mixer2)
        self._session2.add_offset_listener(self._on_session_offset_changes)
        self._session_zoom2 = SessionZoomingComponent(self._session2)
        self._session_zoom2.name = 'R_Session_Overview'
        self._session_zoom2.set_stopped_value(self._color_defs['ZOOM_STOPPED'])
        self._session_zoom2.set_playing_value(self._color_defs['ZOOM_PLAYING'])
        self._session_zoom2.set_selected_value(self._color_defs['ZOOM_SELECTED'])
        self._session_zoom.set_enabled(True)
        self._session_zoom2._zoom_button = self._dummy_button2
        self._session_main = SessionComponent(8, num_scenes)
        self._session_main.name = 'Main_Session'
        self._session_main.set_stop_track_clip_value(self._color_defs['STOP_CLIP'])
        self._scene_main = [ None for index in range(5) ]
        for row in range(num_scenes):
            self._scene_main[row] = self._session_main.scene(row)
            self._scene_main[row].name = 'M_Scene_' + str(row)
            for column in range(8):
                clip_slot = self._scene_main[row].clip_slot(column)
                clip_slot.name = str(column) + '_Clip_Slot_M_' + str(row)
                clip_slot.set_triggered_to_play_value(self._color_defs['CLIP_TRG_PLAY'])
                clip_slot.set_triggered_to_record_value(self._color_defs['CLIP_TRG_REC'])
                clip_slot.set_stopped_value(self._color_defs['CLIP_STOP'])
                clip_slot.set_started_value(self._color_defs['CLIP_STARTED'])
                clip_slot.set_recording_value(self._color_defs['CLIP_RECORDING'])

        self._session_main.set_mixer(self._mixer)
        self._session_zoom_main = SessionZoomingComponent(self._session_main)
        self._session_zoom_main.name = 'M_Session_Overview'
        self._session_zoom_main.set_stopped_value(self._color_defs['ZOOM_STOPPED'])
        self._session_zoom_main.set_playing_value(self._color_defs['ZOOM_PLAYING'])
        self._session_zoom_main.set_selected_value(self._color_defs['ZOOM_SELECTED'])
        self._session_zoom_main.set_enabled(True)
        self._session_zoom_main._zoom_button = self._dummy_button3
        self._sessions = [self._session, self._session2, self._session_main]
        self._zooms = [self._session_zoom, self._session_zoom2, self._session_zoom_main]

    def _setup_monomod(self):
        self._host = MonomodComponent(self)
        self._host.name = 'Monomod_Host'
        self._host2 = SpecialMonomodComponent(self)
        self._host2.name = '256_Monomod_Host'
        self.hosts = [self._host, self._host2]

    def _assign_host2(self):
        self._host2._set_shift_button(self._bank_button[0])
        self._host2._set_alt_button(self._bank_button[1])
        self._host2._set_button_matrix(self._monomod256)
        self._host2._set_key_buttons(self._key_button)
        self._host2.set_enabled(True)

    def _setup_touchosc(self):
        self._osc_registry = {}
        for control in self.controls:
            if hasattr(control, 'osc'):
                self._osc_registry[control.osc] = control.set_value

    def deassign_matrix(self):
        super(LemurPad, self).deassign_matrix()
        self.clear_grid_names()

    def deassign_menu(self):
        super(LemurPad, self).deassign_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(' '))

    def assign_device_nav_to_menu(self):
        super(LemurPad, self).assign_device_nav_to_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(str(DEVICE_NAV_NAMES[index])))

    def assign_transport_to_menu(self):
        super(LemurPad, self).assign_transport_to_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(str(TRANSPORT_NAMES[index])))

    def assign_session_nav_to_menu(self):
        super(LemurPad, self).assign_session_nav_to_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(str(SESSION_NAV_NAMES[index])))

    def assign_session_main_nav_to_menu(self):
        super(LemurPad, self).assign_session_main_nav_to_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(str(SESSION_NAV_NAMES[index])))

    def assign_monomod_shift_to_menu(self):
        super(LemurPad, self).assign_monomod_shift_to_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(str(MONOMOD_SHIFT_NAMES[index])))

    def assign_monomod_to_menu(self):
        super(LemurPad, self).assign_monomod_shift_to_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(str(MONOMOD_NAMES[index])))

    def assign_session_bank_to_menu(self):
        super(LemurPad, self).assign_session_bank_to_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(str(SESSION_BANK_NAMES[index])))

    def assign_session2_bank_to_menu(self):
        super(LemurPad, self).assign_session2_bank_to_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(str(SESSION_BANK2_NAMES[index])))

    def assign_session_main_nav_to_menu(self):
        super(LemurPad, self).assign_session_main_nav_to_menu()
        for index in range(6):
            self._monobridge._send_osc(self._menu[index].osc_name, self.generate_strip_string(str(SESSION_MAIN_BANK_NAMES[index])))

    def generate_strip_string(self, display_string):
        NUM_CHARS_PER_DISPLAY_STRIP = 9
        if not display_string:
            return '`_'
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
        raise len(ret) == NUM_CHARS_PER_DISPLAY_STRIP or AssertionError
        return '`' + ret.replace(' ', '_')

    def notification_to_bridge(self, name, value, sender):
        if isinstance(sender, MonoEncoderElement2):
            self._monobridge._send('lcd_name', sender.name, self.generate_strip_string(str(name)))
            self._monobridge._send('lcd_value', sender.name, self.generate_strip_string(str(value)))

    def clip_name(self, sender, name):
        self._monobridge._send_osc(sender.osc_name, self.generate_strip_string(str(name)))

    def update_display(self):
        super(LemurPad, self).update_display()
        for callback in self._timer_callbacks:
            callback()

    def flash(self):
        if self.flash_status > 0:
            for control in self.controls:
                if isinstance(control, MonoButtonElement):
                    control.flash(self._timer)

    def strobe(self):
        pass

    def disconnect(self):
        super(MonOhm, self).disconnect()

    def clear_grid_names(self):
        for column in range(8):
            for row in range(8):
                self._monobridge._send_osc(self._grid[column][row].osc_name, '`_')

    def _register_timer_callback(self, callback):
        """ Registers a callback that is triggerd on every call of update_display """
        raise callback != None or AssertionError
        raise dir(callback).count('im_func') is 1 or AssertionError
        raise self._timer_callbacks.count(callback) == 0 or AssertionError
        self._timer_callbacks.append(callback)

    def _unregister_timer_callback(self, callback):
        """ Unregisters a timer callback """
        raise callback != None or AssertionError
        raise dir(callback).count('im_func') is 1 or AssertionError
        raise self._timer_callbacks.count(callback) == 1 or AssertionError
        self._timer_callbacks.remove(callback)

    def _set_brightness(self, value):
        pass

    def reset(self):
        for control in self.controls:
            control.reset()

    def assign_lower_grid_names(self, mode):
        if self._display_button_names is True:
            for column in range(8):
                for row in range(3):
                    self._monobridge._send_osc(self._grid[column][row + 5].osc_name, self.generate_strip_string(str(GRID_NAMES[mode][row][column])))

    def reset_and_refresh_state(self, *a, **k):
        self.schedule_message(1, self.reset)
        self.schedule_message(2, self.refresh_state)