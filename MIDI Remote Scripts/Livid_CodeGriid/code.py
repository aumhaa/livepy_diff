#Embedded file name: /Applications/Ableton Live 9.05 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Livid_CodeGriid/code.py
from __future__ import with_statement
import Live
import time
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.DeviceComponent import DeviceComponent
from ShiftModeComponent import ShiftModeComponent
STANDALONE = False
COLS = 8
ROWS = 4
CH = 0
DIALCOUNT = 32
session = None
mixer = None
factoryreset = (240, 0, 1, 97, 4, 6, 247)
btn_channels = (240,
 0,
 1,
 97,
 4,
 19,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 0,
 247)
enc_channels = (240,
 0,
 1,
 97,
 4,
 20,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 CH,
 247)
track_select_notes = [38,
 39,
 40,
 41,
 42,
 43,
 44,
 45]
mode_select_notes = [33,
 34,
 35,
 36,
 37]
matrix_nums = [1,
 5,
 9,
 13,
 17,
 21,
 25,
 29,
 2,
 6,
 10,
 14,
 18,
 22,
 26,
 30,
 3,
 7,
 11,
 15,
 19,
 23,
 27,
 31,
 4,
 8,
 12,
 16,
 20,
 24,
 28,
 32]
device_encoders = [0,
 8,
 16,
 24,
 1,
 9,
 17,
 25,
 2,
 10,
 18,
 26,
 3,
 11,
 19,
 27,
 4,
 12,
 20,
 28,
 5,
 13,
 21,
 29,
 6,
 14,
 22,
 30,
 7,
 15,
 23,
 31]

class code(ControlSurface):
    __module__ = __name__
    __doc__ = ' Code controller script '

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self.log_message(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()) + '--------------= Code opened =--------------')
            self._send_midi(factoryreset)
            self._send_midi(btn_channels)
            self._send_midi(enc_channels)
            self._setup_controls()
            self._setup_device_controls()
            self._setup_mixer_control()
            self._setup_transport_control()
            self._setup_session_control()
            self._setup_modes()

    def handle_sysex(self, midi_bytes):
        self._send_midi(tuple([240,
         0,
         1,
         97,
         4,
         15,
         1,
         247]))

    def _setup_controls(self):
        is_momentary = True
        self._dial = [ None for index in range(DIALCOUNT) ]
        self._trackbtns = [ None for index in range(8) ]
        self._modebtns = [ None for index in range(5) ]
        for index in range(DIALCOUNT):
            self._dial[index] = EncoderElement(MIDI_CC_TYPE, CH, matrix_nums[index], Live.MidiMap.MapMode.absolute)
            self._dial[index].name = 'Dial_' + str(index)
            self._dial[index].set_feedback_delay(-1)

        for index in range(8):
            self._trackbtns[index] = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CH, track_select_notes[index])
            self._trackbtns[index].name = 'Button_' + str(index)

        for index in range(5):
            self._modebtns[index] = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CH, mode_select_notes[index])
            self._modebtns[index].name = 'ModeButton_' + str(index)

        self._matrix = ButtonMatrixElement()
        self._matrix.name = 'Matrix'
        self._grid = [ None for index in range(COLS) ]
        for column in range(COLS):
            self._grid[column] = [ None for index in range(COLS) ]
            for row in range(ROWS):
                nn = 1 + column * ROWS + row
                self._grid[column][row] = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CH, nn)
                self._grid[column][row].name = 'Grid_' + str(column) + '_' + str(row)

        for row in range(ROWS):
            button_row = []
            for column in range(COLS):
                button_row.append(self._grid[column][row])

            self._matrix.add_row(tuple(button_row))

    def _setup_modes(self):
        self._shift_mode = ShiftModeComponent(self, tuple((button for button in self._modebtns)))
        self._shift_mode.name = 'Mix_Mode'

    def _setup_transport_control(self):
        self._transport = TransportComponent()
        self._transport.name = 'Transport'

    def _setup_mixer_control(self):
        global mixer
        is_momentary = True
        self._num_tracks = COLS
        mixer = MixerComponent(COLS, 0, True, True)
        mixer.name = 'Mixer'
        self._mixer = mixer
        mixer.set_track_offset(0)
        for index in range(COLS):
            mixer.channel_strip(index).set_volume_control(self._dial[index + 24])

        for index in range(COLS):
            mixer.channel_strip(index).name = 'Mixer_ChannelStrip_' + str(index)
            mixer.track_eq(index).name = 'Mixer_EQ_' + str(index)
            mixer.track_filter(index).name = 'Mixer_Filter_' + str(index)
            mixer.channel_strip(index)._invert_mute_feedback = True

        self.song().view.selected_track = mixer.channel_strip(0)._track

    def _setup_session_control(self):
        global session
        is_momentary = True
        num_tracks = COLS
        num_scenes = ROWS
        session = SessionComponent(num_tracks, num_scenes)
        session.name = 'Session'
        session.set_offsets(0, 0)
        self._session = session
        self._session.set_stop_track_clip_value(0)
        self._scene = [ None for index in range(ROWS) ]
        for row in range(num_scenes):
            self._scene[row] = session.scene(row)
            self._scene[row].name = 'Scene_' + str(row)
            for column in range(num_tracks):
                clip_slot = self._scene[row].clip_slot(column)
                clip_slot.name = str(column) + '_Clip_Slot_' + str(row)
                clip_slot.set_triggered_to_play_value(64)
                clip_slot.set_triggered_to_record_value(64)
                clip_slot.set_stopped_value(0)
                clip_slot.set_started_value(64)
                clip_slot.set_recording_value(64)

        session.set_mixer(mixer)
        self._session_zoom = SessionZoomingComponent(session)
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_stopped_value(0)
        self._session_zoom.set_playing_value(64)
        self._session_zoom.set_selected_value(64)
        if STANDALONE is True:
            self.set_highlighting_session_component(self._session)
            self._session.set_track_bank_buttons(self._grid[5][3], self._grid[4][3])
            self._session.set_scene_bank_buttons(self._grid[7][3], self._grid[6][3])

    def _setup_device_controls(self):
        self._device = [ None for index in range(4) ]
        for index in range(ROWS):
            self._device[index] = DeviceComponent()
            self._device[index].name = 'Device_Component_' + str(index)
            device_param_controls = []
            for control in range(COLS):
                dial_index = device_encoders[control + index * COLS]
                device_param_controls.append(self._dial[dial_index])

            self._device[index].set_parameter_controls(tuple(device_param_controls))

    def deassign_matrix(self):
        for index in range(DIALCOUNT):
            self._dial[index].send_value(0, True)

        for index in range(COLS):
            self._mixer.track_eq(index).set_enabled(False)
            self._mixer.channel_strip(index).set_volume_control(None)
            self._mixer.track_filter(index).set_enabled(False)
            self._mixer.channel_strip(index).set_pan_control(None)
            self._mixer.channel_strip(index).set_select_button(None)
            self._mixer.channel_strip(index).set_send_controls(tuple([ None for index in range(4) ]))

        for device in range(4):
            self._device[device].set_bank_nav_buttons(None, None)
            self._device[device].set_enabled(False)

        for track in range(8):
            self._mixer.channel_strip(track).set_select_button(None)
            for scene in range(4):
                self._scene[scene].clip_slot(track).set_launch_button(None)

    def assign_page_0(self):
        """for each column"""
        is_momentary = True
        for index in range(COLS):
            self._mixer.track_eq(index).set_gain_controls((self._dial[index + 16], self._dial[index + 8], self._dial[index]))
            self._mixer.track_eq(index).set_enabled(True)
            self._mixer.channel_strip(index).set_volume_control(self._dial[index + 24])
            self._mixer.channel_strip(index).set_select_button(self._trackbtns[index])
            self.assign_cliplaunch()
            self._mixer.update()

    def assign_page_1(self):
        is_momentary = True
        for index in range(COLS):
            send_controllers = [self._dial[index],
             self._dial[index + 8],
             self._dial[index + 16],
             self._dial[index + 24]]
            self._mixer.channel_strip(index).set_send_controls(tuple(send_controllers))
            self._mixer.channel_strip(index).set_select_button(self._trackbtns[index])
            self._mixer.update()

    def assign_pages_2_3(self):
        for index in range(4):
            self._device[index].set_enabled(True)

        self._reassign_devices(self._shift_mode._mode_index)

    def assign_page_4(self):
        is_momentary = True
        for index in range(COLS):
            self._mixer.track_filter(index).set_filter_controls(self._dial[index], self._dial[index + 8])
            self._mixer.track_filter(index).set_enabled(True)
            self._mixer.channel_strip(index).set_pan_control(self._dial[index + 16])
            self._mixer.channel_strip(index).set_volume_control(self._dial[index + 24])
            self._mixer.channel_strip(index).set_select_button(self._trackbtns[index])
            self._mixer.update()

    def assign_cliplaunch(self):
        if STANDALONE is True:
            for column in range(COLS):
                for row in range(ROWS - 1):
                    self._scene[row].clip_slot(column).set_launch_button(self._grid[column][row])

    def _reassign_devices(self, mode_index):
        if self._shift_mode._mode_index in range(2, 4):
            offset = (mode_index - 2) * 4
            track = self.song().view.selected_track
            for index in range(4):
                if index + offset < len(track.devices):
                    self._device[index].set_device(track.devices[index + offset])
                else:
                    self._device[index].set_device(None)
                self._device[index].set_bank_nav_buttons(self._trackbtns[index * 2], self._trackbtns[index * 2 + 1])
                self._device[index].update()

    def disconnect(self):
        """clean things up on disconnect"""
        self.log_message(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()) + '--------------= Code log closed =--------------')
        ControlSurface.disconnect(self)