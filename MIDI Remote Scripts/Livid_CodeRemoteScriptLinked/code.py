#Embedded file name: /Applications/Ableton Live 9 Beta.app/Contents/App-Resources/MIDI Remote Scripts/Livid_CodeRemoteScriptLinked/code.py
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
from _Framework.EncoderElement import EncoderElement
from _Framework.DeviceComponent import DeviceComponent
from TransportComponent import TransportComponent
from DetailViewCntrlComponent import DetailViewCntrlComponent
from AddlTransportComponent import AddlTransportComponent
from ShiftableTransportComponent import ShiftableTransportComponent
from ShiftableTranslatorComponent import ShiftableTranslatorComponent
CHAN = 0
session = None
mixer = None
factoryreset = (240, 0, 1, 97, 4, 6, 247)
btn_channels = (240,
 0,
 1,
 97,
 4,
 19,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 0,
 247)
enc_channels = (240,
 0,
 1,
 97,
 4,
 20,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 CHAN,
 247)

class code(ControlSurface):
    __module__ = __name__
    __doc__ = ' Code controller script '

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self.log_message(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()) + '--------------= Code opened =--------------')
            self._link_offset = [False, True]
            self._send_midi(factoryreset)
            self._send_midi(btn_channels)
            self._send_midi(enc_channels)
            self._setup_mixer_control()
            self._setup_transport_control()
            self._setup_session_control()
            for control in self.controls:
                if isinstance(control, EncoderElement):
                    control.set_feedback_delay(-1)

            for component in self.components:
                component.set_enabled(True)

    def handle_sysex(self, midi_bytes):
        self._send_midi(tuple([240,
         0,
         1,
         97,
         4,
         15,
         1,
         247]))

    def _setup_transport_control(self):
        is_momentary = True
        transport = ShiftableTransportComponent()
        device_param_controls = []
        effects_knob_cc = [17,
         21,
         25,
         29,
         18,
         22,
         26,
         30]
        device = DeviceComponent()
        for index in range(8):
            device_param_controls.append(EncoderElement(MIDI_CC_TYPE, CHAN, effects_knob_cc[index], Live.MidiMap.MapMode.absolute))

        device.set_parameter_controls(tuple(device_param_controls))
        device_bank_buttons = []
        device_buttons = [17,
         21,
         25,
         29,
         18,
         22,
         26,
         30]
        bank_button_labels = ('Clip_Track_Button', 'Device_On_Off_Button', 'Previous_Device_Button', 'Next_Device_Button', 'Detail_View_Button', 'Rec_Quantization_Button', 'Midi_Overdub_Button', 'Device_Lock_Button')
        for index in range(8):
            device_bank_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, device_buttons[index]))
            device_bank_buttons[-1].name = bank_button_labels[index]

        device.name = 'Device_Component'
        device.set_bank_buttons(tuple(device_bank_buttons))
        detail_view_toggler = DetailViewCntrlComponent()
        detail_view_toggler.name = 'Detail_View_Control'
        detail_view_toggler.set_device_clip_toggle_button(device_bank_buttons[0])
        device.set_on_off_button(device_bank_buttons[1])
        detail_view_toggler.set_device_nav_buttons(device_bank_buttons[2], device_bank_buttons[3])
        detail_view_toggler.set_detail_toggle_button(device_bank_buttons[4])
        device.set_lock_button(device_bank_buttons[7])
        self.set_device_component(device)
        self._shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 37)
        play_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 24)
        stop_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 28)
        record_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 32)
        nudge_up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 27)
        nudge_down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 23)
        redo_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 19)
        undo_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 20)
        play_button.name = 'Play_Button'
        stop_button.name = 'Stop_Button'
        record_button.name = 'Record_Button'
        nudge_up_button.name = 'Nudge_Up_Button'
        nudge_down_button.name = 'Nudge_Down_Button'
        redo_button.name = 'Redo_Button'
        undo_button.name = 'Undo_Button'
        transport.set_shift_button(self._shift_button)
        transport.set_play_button(play_button)
        transport.set_stop_button(stop_button)
        transport.set_record_button(record_button)
        transport.set_nudge_buttons(nudge_up_button, nudge_down_button)
        transport.set_tap_tempo_button(nudge_up_button)
        transport.set_quant_toggle_button(device_bank_buttons[5])
        transport.set_overdub_button(device_bank_buttons[6])
        bank_button_translator = ShiftableTranslatorComponent()
        bank_button_translator.set_controls_to_translate(tuple(device_bank_buttons))
        bank_button_translator.set_shift_button(self._shift_button)

    def _setup_mixer_control(self):
        global mixer
        is_momentary = True
        num_tracks = 4
        mixer = MixerComponent(num_tracks, 2, with_eqs=True, with_filters=False)
        mixer.set_track_offset(0)
        self.song().view.selected_track = mixer.channel_strip(0)._track
        track_select_notes = [38,
         39,
         40,
         41]
        send_ccs = [2,
         6,
         10,
         14,
         1,
         5,
         9,
         13]
        pan_ccs = [3,
         7,
         11,
         15]
        slider_ccs = [4,
         8,
         12,
         16]
        for index in range(num_tracks):
            mixer.channel_strip(index).set_select_button(ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, track_select_notes[index]))
            mixer.channel_strip(index).set_volume_control(SliderElement(MIDI_CC_TYPE, CHAN, slider_ccs[index]))
            mixer.channel_strip(index).set_pan_control(EncoderElement(MIDI_CC_TYPE, CHAN, pan_ccs[index], Live.MidiMap.MapMode.absolute))
            send_controlers = [EncoderElement(MIDI_CC_TYPE, CHAN, send_ccs[index], Live.MidiMap.MapMode.absolute), EncoderElement(MIDI_CC_TYPE, CHAN, send_ccs[index + num_tracks], Live.MidiMap.MapMode.absolute)]
            mixer.channel_strip(index).set_send_controls(tuple(send_controlers))

        crossfader = SliderElement(MIDI_CC_TYPE, CHAN, 28)
        master_volume_control = SliderElement(MIDI_CC_TYPE, CHAN, 32)
        returna_pan_control = SliderElement(MIDI_CC_TYPE, CHAN, 19)
        returna_volume_control = SliderElement(MIDI_CC_TYPE, CHAN, 20)
        returnb_pan_control = SliderElement(MIDI_CC_TYPE, CHAN, 23)
        returnb_volume_control = SliderElement(MIDI_CC_TYPE, CHAN, 24)
        master_select_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 31)
        prehear_control = EncoderElement(MIDI_CC_TYPE, CHAN, 30, Live.MidiMap.MapMode.absolute)
        crossfader.name = 'Crossfader'
        master_volume_control.name = 'Master_Volume_Control'
        returna_pan_control.name = 'ReturnA_Pan_Control'
        returna_volume_control.name = 'ReturnA_Volume_Control'
        returnb_pan_control.name = 'ReturnB_Pan_Control'
        returnb_volume_control.name = 'ReturnB_Volume_Control'
        master_select_button.name = 'Master_Select_Button'
        prehear_control.name = 'Prehear_Volume_Control'
        mixer.set_crossfader_control(crossfader)
        mixer.master_strip().set_volume_control(master_volume_control)
        mixer.master_strip().set_select_button(master_select_button)
        mixer.set_prehear_volume_control(prehear_control)
        mixer.return_strip(0).set_pan_control(returna_pan_control)
        mixer.return_strip(0).set_volume_control(returna_volume_control)
        mixer.return_strip(1).set_pan_control(returnb_pan_control)
        mixer.return_strip(1).set_volume_control(returnb_volume_control)

    def _setup_session_control(self):
        global session
        is_momentary = True
        right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 43)
        left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 42)
        up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 44)
        down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, 45)
        right_button.name = 'Bank_Select_Right_Button'
        left_button.name = 'Bank_Select_Left_Button'
        up_button.name = 'Bank_Select_Up_Button'
        down_button.name = 'Bank_Select_Down_Button'
        session = SessionComponent(4, 4)
        session.name = 'Session_Control'
        session.set_track_bank_buttons(right_button, left_button)
        session.set_scene_bank_buttons(down_button, up_button)
        self._session = session
        matrix = ButtonMatrixElement()
        matrix.name = 'Button_Matrix'
        scene_launch_notes = [33,
         34,
         35,
         36]
        scene_launch_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, scene_launch_notes[index]) for index in range(4) ]
        for index in range(len(scene_launch_buttons)):
            scene_launch_buttons[index].name = 'Scene_' + str(index) + '_Launch_Button'

        button_notes = [1,
         2,
         3,
         4,
         5,
         6,
         7,
         8,
         9,
         10,
         11,
         12,
         13,
         14,
         15,
         16,
         17,
         18,
         19,
         20,
         21,
         22,
         23,
         24,
         25,
         26,
         27,
         28,
         29,
         30,
         31,
         32]
        for scene_index in range(4):
            scene = session.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            button_row = []
            scene.set_launch_button(scene_launch_buttons[scene_index])
            for track_index in range(4):
                button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, CHAN, track_index * 4 + scene_index + 1)
                button.name = str(track_index) + '_Clip_' + str(scene_index) + '_Button'
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index)
                clip_slot.set_stopped_value(0)
                clip_slot.set_started_value(64)
                clip_slot.set_launch_button(button)

            matrix.add_row(tuple(button_row))

        session.selected_scene().name = 'Selected_Scene'
        self.set_highlighting_session_component(session)
        session.set_mixer(mixer)

    def disconnect(self):
        """clean things up on disconnect"""
        if self._session._is_linked():
            self._session._unlink()
        self.log_message(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()) + '--------------= Code log closed =--------------')
        ControlSurface.disconnect(self)

    def connect_script_instances(self, instanciated_scripts):
        link = False
        offsets = [0, 0]
        new_channel = CHAN
        for s in instanciated_scripts:
            if isinstance(s, code) and s is not self:
                link = True
                if s._session._is_linked():
                    self.log_message('found other linked instance')
                    offsets[0] += int(self._link_offset[0]) * 8
                    offsets[1] += int(self._link_offset[1]) * 4
                    new_channel += 1

        if link and not self._session._is_linked():
            self._session.set_offsets(offsets[0], offsets[1])
            self._session._link()
        self._set_code_channels(new_channel)

    def _set_code_channels(self, channel):
        for control in self.controls:
            if isinstance(control, InputControlElement):
                control.set_channel(channel)
                control._original_channel = channel

        self.request_rebuild_midi_map()
        self._send_midi(tuple([240,
         0,
         1,
         97,
         4,
         6,
         247]))
        self._send_midi(tuple([240,
         0,
         1,
         97,
         4,
         19,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         247]))
        self._send_midi(tuple([240,
         0,
         1,
         97,
         4,
         20,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         channel,
         247]))
        for index in range(128):
            self._send_midi(tuple([240,
             0,
             1,
             97,
             4,
             21,
             index,
             0,
             channel,
             247]))