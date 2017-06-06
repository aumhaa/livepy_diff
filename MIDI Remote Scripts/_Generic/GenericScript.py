
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from .SpecialMixerComponent import SpecialMixerComponent

class GenericScript(ControlSurface):
    u""" A generic script class with predefined behaviour.
        It can be customised to use/not use certain controls on instantiation.
    """

    def __init__(self, c_instance, macro_map_mode, volume_map_mode, device_controls, transport_controls, volume_controls, trackarm_controls, bank_controls, descriptions = None, mixer_options = None):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            global_channel = 0
            if descriptions:
                if list(descriptions.keys()).count(u'INPUTPORT') > 0:
                    self._suggested_input_port = descriptions[u'INPUTPORT']
                if list(descriptions.keys()).count(u'OUTPUTPORT') > 0:
                    self._suggested_output_port = descriptions[u'OUTPUTPORT']
                if list(descriptions.keys()).count(u'CHANNEL') > 0:
                    global_channel = descriptions[u'CHANNEL']
                    if global_channel not in range(16):
                        global_channel = 0
                if list(descriptions.keys()).count(u'PAD_TRANSLATION') > 0:
                    self.set_pad_translations(descriptions[u'PAD_TRANSLATION'])
            self._init_mixer_component(volume_controls, trackarm_controls, mixer_options, global_channel, volume_map_mode)
            self._init_device_component(device_controls, bank_controls, global_channel, macro_map_mode)
            self._init_transport_component(transport_controls, global_channel)

    def handle_sysex(self, midi_bytes):
        pass

    def _init_mixer_component(self, volume_controls, trackarm_controls, mixer_options, global_channel, volume_map_mode):
        if volume_controls != None and trackarm_controls != None:
            num_strips = max(len(volume_controls), len(trackarm_controls))
            send_info = []
            momentary_buttons = False
            mixer = SpecialMixerComponent(num_strips)
            mixer.name = u'Mixer'
            mixer.master_strip().name = u'Master_Channel_Strip'
            mixer.selected_strip().name = u'Selected_Channel_Strip'
            if mixer_options != None:
                if u'MASTERVOLUME' in mixer_options.keys() and mixer_options[u'MASTERVOLUME'] in range(128):
                    encoder = EncoderElement(MIDI_CC_TYPE, global_channel, mixer_options[u'MASTERVOLUME'], volume_map_mode)
                    encoder.name = u'Master_Volume_Control'
                    mixer.master_strip().set_volume_control(encoder)
                if u'NUMSENDS' in mixer_options.keys() and mixer_options[u'NUMSENDS'] > 0:
                    for send in range(mixer_options[u'NUMSENDS']):
                        key = u'SEND' + str(send + 1)
                        raise key in mixer_options.keys() or AssertionError
                        send_info.append(mixer_options[key])

                momentary_buttons = u'NOTOGGLE' in mixer_options.keys()
                next_bank_button = None
                prev_bank_button = None
                if u'NEXTBANK' in mixer_options.keys() and mixer_options[u'NEXTBANK'] in range(128):
                    next_bank_button = ButtonElement(momentary_buttons, MIDI_CC_TYPE, global_channel, mixer_options[u'NEXTBANK'])
                    next_bank_button.name = u'Mixer_Next_Bank_Button'
                if u'PREVBANK' in mixer_options.keys() and mixer_options[u'PREVBANK'] in range(128):
                    prev_bank_button = ButtonElement(momentary_buttons, MIDI_CC_TYPE, global_channel, mixer_options[u'PREVBANK'])
                    prev_bank_button.name = u'Mixer_Previous_Bank_Button'
                mixer.set_bank_buttons(next_bank_button, prev_bank_button)
            for track in range(num_strips):
                strip = mixer.channel_strip(track)
                strip.name = u'Channel_Strip_' + str(track)
                if track in range(len(volume_controls)):
                    channel = global_channel
                    cc = volume_controls[track]
                    if isinstance(volume_controls[track], (tuple, list)):
                        cc = volume_controls[track][0]
                        if volume_controls[track][1] in range(16):
                            channel = volume_controls[track][1]
                    if cc in range(128) and channel in range(16):
                        encoder = EncoderElement(MIDI_CC_TYPE, channel, cc, volume_map_mode)
                        encoder.name = str(track) + u'_Volume_Control'
                        strip.set_volume_control(encoder)
                if track in range(len(trackarm_controls)) and trackarm_controls[track] in range(128):
                    button = ButtonElement(momentary_buttons, MIDI_CC_TYPE, global_channel, trackarm_controls[track])
                    button.name = str(track) + u'_Arm_Button'
                    strip.set_arm_button(button)
                send_controls = []
                for send in send_info:
                    encoder = None
                    if track in range(len(send)):
                        channel = global_channel
                        cc = send[track]
                        if isinstance(send[track], (tuple, list)):
                            cc = send[track][0]
                            if send[track][1] in range(16):
                                channel = send[track][1]
                        if cc in range(128) and channel in range(16):
                            encoder = EncoderElement(MIDI_CC_TYPE, channel, cc, volume_map_mode)
                            encoder.name = str(track) + u'_Send_' + str(list(send_info).index(send)) + u'_Control'
                    send_controls.append(encoder)

                strip.set_send_controls(tuple(send_controls))

    def _init_device_component(self, device_controls, bank_controls, global_channel, macro_map_mode):
        is_momentary = True
        if device_controls:
            device = DeviceComponent(device_selection_follows_track_selection=True)
            device.name = u'Device_Component'
            if bank_controls:
                next_button = None
                prev_button = None
                if u'NEXTBANK' in bank_controls.keys() and bank_controls[u'NEXTBANK'] in range(128):
                    next_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, bank_controls[u'NEXTBANK'])
                    next_button.name = u'Device_Next_Bank_Button'
                if u'PREVBANK' in bank_controls.keys() and bank_controls[u'PREVBANK'] in range(128):
                    prev_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, bank_controls[u'PREVBANK'])
                    prev_button.name = u'Device_Previous_Bank_Button'
                device.set_bank_nav_buttons(prev_button, next_button)
                if u'TOGGLELOCK' in bank_controls.keys() and bank_controls[u'TOGGLELOCK'] in range(128):
                    lock_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, bank_controls[u'TOGGLELOCK'])
                    lock_button.name = u'Device_Lock_Button'
                    device.set_lock_button(lock_button)
                bank_buttons = []
                for index in range(8):
                    key = u'BANK' + str(index + 1)
                    if key in bank_controls.keys():
                        control_info = bank_controls[key]
                        channel = global_channel
                        cc = -1
                        if isinstance(control_info, (tuple, list)):
                            cc = control_info[0]
                            if control_info[1] in range(16):
                                channel = control_info[1]
                        else:
                            cc = control_info
                        if cc in range(128) and channel in range(16):
                            button = ButtonElement(is_momentary, MIDI_CC_TYPE, channel, cc)
                            button.name = u'Device_Bank_' + str(index) + u'_Button'
                            bank_buttons.append(button)

                if len(bank_buttons) > 0:
                    device.set_bank_buttons(tuple(bank_buttons))
            parameter_encoders = []
            for control_info in device_controls:
                channel = global_channel
                cc = -1
                if isinstance(control_info, (tuple, list)):
                    cc = control_info[0]
                    if control_info[1] in range(16):
                        channel = control_info[1]
                else:
                    cc = control_info
                if cc in range(128) and channel in range(16):
                    encoder = EncoderElement(MIDI_CC_TYPE, channel, cc, macro_map_mode)
                    encoder.name = u'Device_Parameter_' + str(list(device_controls).index(control_info)) + u'_Control'
                    parameter_encoders.append(encoder)

            if len(parameter_encoders) > 0:
                device.set_parameter_controls(tuple(parameter_encoders))
            self.set_device_component(device)

    def _init_transport_component(self, transport_controls, global_channel):
        is_momentary = True
        if transport_controls:
            transport = TransportComponent()
            transport.name = u'Transport'
            if u'STOP' in transport_controls.keys() and transport_controls[u'STOP'] in range(128):
                stop_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, transport_controls[u'STOP'])
                stop_button.name = u'Stop_Button'
                transport.set_stop_button(stop_button)
            if u'PLAY' in transport_controls.keys() and transport_controls[u'PLAY'] in range(128):
                play_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, transport_controls[u'PLAY'])
                play_button.name = u'Play_Button'
                transport.set_play_button(play_button)
            if u'REC' in transport_controls.keys() and transport_controls[u'REC'] in range(128):
                rec_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, transport_controls[u'REC'])
                rec_button.name = u'Record_Button'
                transport.set_record_button(rec_button)
            if u'LOOP' in transport_controls.keys() and transport_controls[u'LOOP'] in range(128):
                loop_button = ButtonElement(is_momentary, MIDI_CC_TYPE, global_channel, transport_controls[u'LOOP'])
                loop_button.name = u'Loop_Button'
                transport.set_loop_button(loop_button)
            ffwd_button = None
            rwd_button = None
            momentary_seek = u'NORELEASE' not in transport_controls.keys()
            if u'FFWD' in transport_controls.keys() and transport_controls[u'FFWD'] in range(128):
                ffwd_button = ButtonElement(momentary_seek, MIDI_CC_TYPE, global_channel, transport_controls[u'FFWD'])
                ffwd_button.name = u'FFwd_Button'
            if u'RWD' in transport_controls.keys() and transport_controls[u'RWD'] in range(128):
                rwd_button = ButtonElement(momentary_seek, MIDI_CC_TYPE, global_channel, transport_controls[u'RWD'])
                rwd_button.name = u'Rwd_Button'
            transport.set_seek_buttons(ffwd_button, rwd_button)