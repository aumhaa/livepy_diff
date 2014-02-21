#Embedded file name: /Applications/Ableton Live 9 Beta.app/Contents/App-Resources/MIDI Remote Scripts/Livid_Block/Block.py
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
CHANNEL = 0
session = None
mixer = None
switchxfader = (240, 0, 1, 97, 2, 15, 1, 247)

class Block(ControlSurface):
    __module__ = __name__
    __doc__ = ' Ohm64 controller script '

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self.log_message(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()) + '--------------= Block opened =--------------')
            self._send_midi(switchxfader)
            self._setup_transport_control()
            self._setup_mixer_control()
            self._setup_session_control()

    def handle_sysex(self, midi_bytes):
        self._send_midi(240, 0, 1, 97, 2, 15, 1, 247)
        response = [long(0), long(0)]
        self.log_message(response)

    def _setup_transport_control(self):
        is_momentary = True
        transport = TransportComponent()
        transport.set_play_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 69))
        transport.set_stop_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 70))
        device_param_controls = []
        effects_knob_cc = [17,
         16,
         9,
         8,
         19,
         18,
         11,
         10]
        device = DeviceComponent()
        for index in range(8):
            device_param_controls.append(EncoderElement(MIDI_CC_TYPE, 0, effects_knob_cc[index], Live.MidiMap.MapMode.absolute))

        device.set_parameter_controls(tuple(device_param_controls))
        self.set_device_component(device)

    def _setup_mixer_control(self):
        global mixer
        is_momentary = True
        num_tracks = 7
        mixer = MixerComponent(num_tracks, 0, with_eqs=False, with_filters=False)
        mixer.set_track_offset(0)
        self.song().view.selected_track = mixer.channel_strip(0)._track
        mixer.selected_strip().set_mute_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 64))
        mixer.selected_strip().set_arm_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, 72))
        track_select_notes = [65,
         73,
         66,
         74,
         67,
         75,
         68,
         76]
        slider_select_notes = [3,
         2,
         1,
         0,
         5,
         4,
         6,
         7]
        master_volume_control = SliderElement(MIDI_CC_TYPE, 0, 7)
        for index in range(num_tracks):
            mixer.channel_strip(index).set_volume_control(SliderElement(MIDI_CC_TYPE, CHANNEL, slider_select_notes[index]))

        master_volume_control.name = 'Master_Volume_Control'
        mixer.master_strip().set_volume_control(master_volume_control)

    def _setup_session_control(self):
        global session
        is_momentary = True
        self._shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 87)
        right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 67)
        left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 66)
        up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 71)
        down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 68)
        right_button.name = 'Bank_Select_Right_Button'
        left_button.name = 'Bank_Select_Left_Button'
        up_button.name = 'Bank_Select_Up_Button'
        down_button.name = 'Bank_Select_Down_Button'
        session = SessionComponent(7, 8)
        session.name = 'Session_Control'
        session.set_track_bank_buttons(right_button, left_button)
        session.set_scene_bank_buttons(down_button, up_button)
        matrix = ButtonMatrixElement()
        matrix.name = 'Button_Matrix'
        scene_launch_notes = [56,
         57,
         58,
         59,
         60,
         61,
         62,
         63]
        scene_launch_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, scene_launch_notes[index]) for index in range(8) ]
        for index in range(len(scene_launch_buttons)):
            scene_launch_buttons[index].name = 'Scene_' + str(index) + '_Launch_Button'

        for scene_index in range(8):
            scene = session.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            button_row = []
            scene.set_launch_button(scene_launch_buttons[scene_index])
            for track_index in range(7):
                button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, track_index * 8 + scene_index)
                button.name = str(track_index) + '_Clip_' + str(scene_index) + '_Button'
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index)
                clip_slot.set_stopped_value(0)
                clip_slot.set_started_value(64)
                clip_slot.set_launch_button(button)

            matrix.add_row(tuple(button_row))

        session.selected_scene().name = 'Selected_Scene'
        session.set_mixer(mixer)
        self.set_highlighting_session_component(session)

    def disconnect(self):
        """clean things up on disconnect"""
        self.log_message(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()) + '--------------= Block log closed =--------------')
        ControlSurface.disconnect(self)