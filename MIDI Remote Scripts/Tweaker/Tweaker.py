
from __future__ import with_statement
import Live
import time
import math
import sys
from itertools import chain
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.DisplayDataSource import DisplayDataSource
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
from MonoButtonElement import MonoButtonElement
from DetailViewControllerComponent import DetailViewControllerComponent
import LiveUtils
from _Generic.Devices import *
from Tweaker_Map import *
CHANNEL = 0
session = None
mixer = None
NUM_TRACKS = 7
NUM_SCENES = 3
EQ3_BANK1 = ('GainHi',
 'GainMid',
 'GainLo',
 '',
 'FreqHi',
 'FreqLo',
 'Slope',
 '')
EQ3_BANK2 = ('FreqHi',
 'FreqLo',
 'Slope',
 '',
 'GainHi',
 'GainMid',
 'GainLo',
 '')
EQ3_BANKS = (EQ3_BANK1, EQ3_BANK2)
EQ3_BOBS = (EQ3_BANK1, EQ3_BANK2)
DEVICE_DICT = {'AudioEffectGroupDevice': RCK_BANKS,
 'MidiEffectGroupDevice': RCK_BANKS,
 'InstrumentGroupDevice': RCK_BANKS,
 'DrumGroupDevice': RCK_BANKS,
 'InstrumentImpulse': IMP_BANKS,
 'Operator': OPR_BANKS,
 'UltraAnalog': ALG_BANKS,
 'OriginalSimpler': SIM_BANKS,
 'MultiSampler': SAM_BANKS,
 'MidiArpeggiator': ARP_BANKS,
 'LoungeLizard': ELC_BANKS,
 'StringStudio': TNS_BANKS,
 'MidiChord': CRD_BANKS,
 'MidiNoteLength': NTL_BANKS,
 'MidiPitcher': PIT_BANKS,
 'MidiRandom': RND_BANKS,
 'MidiScale': SCL_BANKS,
 'MidiVelocity': VEL_BANKS,
 'AutoFilter': AFL_BANKS,
 'AutoPan': APN_BANKS,
 'BeatRepeat': BRP_BANKS,
 'Chorus': CHR_BANKS,
 'Compressor2': CP3_BANKS,
 'Tube': DTB_BANKS,
 'Eq8': EQ8_BANKS,
 'FilterEQ3': EQ3_BANKS,
 'Erosion': ERO_BANKS,
 'FilterDelay': FLD_BANKS,
 'Flanger': FLG_BANKS,
 'GrainDelay': GRD_BANKS,
 'Phaser': PHS_BANKS,
 'Redux': RDX_BANKS,
 'Saturator': SAT_BANKS,
 'Resonator': RSN_BANKS,
 'CrossDelay': SMD_BANKS,
 'StereoGain': UTL_BANKS,
 'Tube': DTB_BANKS,
 'Reverb': RVB_BANKS,
 'Vinyl': VDS_BANKS,
 'Gate': GTE_BANKS,
 'PingPongDelay': PPG_BANKS}
DEVICE_BOB_DICT = {'AudioEffectGroupDevice': RCK_BOBS,
 'MidiEffectGroupDevice': RCK_BOBS,
 'InstrumentGroupDevice': RCK_BOBS,
 'DrumGroupDevice': RCK_BOBS,
 'InstrumentImpulse': IMP_BOBS,
 'Operator': OPR_BOBS,
 'UltraAnalog': ALG_BOBS,
 'OriginalSimpler': SIM_BOBS,
 'MultiSampler': SAM_BOBS,
 'MidiArpeggiator': ARP_BOBS,
 'LoungeLizard': ELC_BOBS,
 'StringStudio': TNS_BOBS,
 'MidiChord': CRD_BOBS,
 'MidiNoteLength': NTL_BOBS,
 'MidiPitcher': PIT_BOBS,
 'MidiRandom': RND_BOBS,
 'MidiScale': SCL_BOBS,
 'MidiVelocity': VEL_BOBS,
 'AutoFilter': AFL_BOBS,
 'AutoPan': APN_BOBS,
 'BeatRepeat': BRP_BOBS,
 'Chorus': CHR_BOBS,
 'Compressor2': CP3_BOBS,
 'Tube': DTB_BOBS,
 'Eq8': EQ8_BOBS,
 'FilterEQ3': EQ3_BOBS,
 'Erosion': ERO_BOBS,
 'FilterDelay': FLD_BOBS,
 'Flanger': FLG_BOBS,
 'GrainDelay': GRD_BOBS,
 'Phaser': PHS_BOBS,
 'Redux': RDX_BOBS,
 'Saturator': SAT_BOBS,
 'Resonator': RSN_BOBS,
 'CrossDelay': SMD_BOBS,
 'StereoGain': UTL_BOBS,
 'Tube': DTB_BOBS,
 'Reverb': RVB_BOBS,
 'Vinyl': VDS_BOBS,
 'Gate': GTE_BOBS,
 'PingPongDelay': PPG_BOBS}

class DeviceComponent(ControlSurfaceComponent):
    """ Class representing a device in Live """

    def __init__(self):
        super(DeviceComponent, self).__init__()
        self._device_banks = DEVICE_DICT
        self._device_best_banks = DEVICE_BOB_DICT
        self._device_bank_names = BANK_NAME_DICT
        self._device = None
        self._parameter_controls = None
        self._bank_up_button = None
        self._bank_down_button = None
        self._bank_buttons = None
        self._on_off_button = None
        self._lock_button = None
        self._lock_callback = None
        self._device_name_data_source = None
        self._device_bank_registry = {}
        self._bank_index = 0
        self._bank_name = '<No Bank>'
        self._locked_to_device = False

    def disconnect(self):
        self._lock_callback = None
        self._device_bank_registry = None
        if self._parameter_controls != None:
            for control in self._parameter_controls:
                control.release_parameter()

            self._parameter_controls = None
        if self._bank_up_button != None:
            self._bank_up_button.remove_value_listener(self._bank_up_value)
            self._bank_up_button = None
        if self._bank_down_button != None:
            self._bank_down_button.remove_value_listener(self._bank_down_value)
            self._bank_down_button = None
        if self._bank_buttons != None:
            for button in self._bank_buttons:
                button.remove_value_listener(self._bank_value)

        self._bank_buttons = None
        if self._on_off_button != None:
            self._on_off_button.remove_value_listener(self._on_off_value)
            self._on_off_button = None
        if self._lock_button != None:
            self._lock_button.remove_value_listener(self._lock_value)
            self._lock_button = None
        if self._device != None:
            parameter = self._on_off_parameter()
            if parameter != None:
                parameter.remove_value_listener(self._on_on_off_changed)
            self._device.remove_name_listener(self._on_device_name_changed)
            self._device.remove_parameters_listener(self._on_parameters_changed)
            self._device = None

    def on_enabled_changed(self):
        self.update()

    def set_device(self, device):
        if not (device == None or isinstance(device, Live.Device.Device)):
            raise AssertionError
            if not self._locked_to_device and device != self._device:
                if self._device != None:
                    self._device.remove_name_listener(self._on_device_name_changed)
                    self._device.remove_parameters_listener(self._on_parameters_changed)
                    parameter = self._on_off_parameter()
                    if parameter != None:
                        parameter.remove_value_listener(self._on_on_off_changed)
                    if self._parameter_controls != None:
                        for control in self._parameter_controls:
                            control.release_parameter()

                self._device = device
                if self._device != None:
                    self._bank_index = 0
                    self._device.add_name_listener(self._on_device_name_changed)
                    self._device.add_parameters_listener(self._on_parameters_changed)
                    parameter = self._on_off_parameter()
                    parameter != None and parameter.add_value_listener(self._on_on_off_changed)
            for key in self._device_bank_registry.keys():
                if key == self._device:
                    self._bank_index = self._device_bank_registry.get(key, 0)
                    del self._device_bank_registry[key]
                    break

            self._bank_name = '<No Bank>'
            self._on_device_name_changed()
            self.update()

    def set_bank_nav_buttons(self, down_button, up_button):
        if not (down_button != None or up_button == None):
            raise AssertionError
            if not (up_button == None or isinstance(up_button, ButtonElement)):
                raise AssertionError
                if not (down_button == None or isinstance(down_button, ButtonElement)):
                    raise AssertionError
                    do_update = False
                    if up_button != self._bank_up_button:
                        do_update = True
                        if self._bank_up_button != None:
                            self._bank_up_button.remove_value_listener(self._bank_up_value)
                        self._bank_up_button = up_button
                        if self._bank_up_button != None:
                            self._bank_up_button.add_value_listener(self._bank_up_value)
                    if down_button != self._bank_down_button:
                        do_update = True
                        self._bank_down_button != None and self._bank_down_button.remove_value_listener(self._bank_down_value)
                    self._bank_down_button = down_button
                    self._bank_down_button != None and self._bank_down_button.add_value_listener(self._bank_down_value)
            do_update and self.update()

    def set_bank_buttons(self, buttons):
        if not (buttons == None or isinstance(buttons, tuple)):
            raise AssertionError
            if self._bank_buttons != None:
                for button in self._bank_buttons:
                    button.remove_value_listener(self._bank_value)

            self._bank_buttons = buttons
            identify_sender = self._bank_buttons != None and True
            for button in self._bank_buttons:
                button.add_value_listener(self._bank_value, identify_sender)

        self.update()

    def set_parameter_controls(self, controls):
        raise controls != None or AssertionError
        raise isinstance(controls, tuple) or AssertionError
        if self._device != None and self._parameter_controls != None:
            for control in self._parameter_controls:
                control.release_parameter()

        for control in controls:
            raise control != None or AssertionError
            raise isinstance(control, EncoderElement) or AssertionError

        self._parameter_controls = controls
        self.update()

    def set_lock_to_device(self, lock, device):
        if not isinstance(lock, type(False)):
            raise AssertionError
            if not lock is not self._locked_to_device:
                raise AssertionError
                if lock:
                    self.set_device(device)
                else:
                    raise device == self._device or AssertionError
                self._locked_to_device = lock
                if self.is_enabled():
                    self._lock_button != None and self._locked_to_device and self._lock_button.turn_on()
                else:
                    self._lock_button.turn_off()

    def set_lock_button(self, button):
        if not (button == None or isinstance(button, ButtonElement)):
            raise AssertionError
            if self._lock_button != None:
                self._lock_button.remove_value_listener(self._lock_value)
                self._lock_button = None
            self._lock_button = button
            self._lock_button != None and self._lock_button.add_value_listener(self._lock_value)
        self.update()

    def set_on_off_button(self, button):
        if not (button == None or isinstance(button, ButtonElement)):
            raise AssertionError
            if self._on_off_button != None:
                self._on_off_button.remove_value_listener(self._on_off_value)
                self._on_off_button = None
            self._on_off_button = button
            self._on_off_button != None and self._on_off_button.add_value_listener(self._on_off_value)
        self.update()

    def set_lock_callback(self, callback):
        raise self._lock_callback == None or AssertionError
        raise callback != None or AssertionError
        raise dir(callback).count('im_func') is 1 or AssertionError
        self._lock_callback = callback

    def restore_bank(self, bank_index):
        if self._device != None and self._is_banking_enabled() and self._locked_to_device and self._number_of_parameter_banks() > bank_index and self._bank_index != bank_index:
            self._bank_index = bank_index
            self.update()

    def device_name_data_source(self):
        if self._device_name_data_source == None:
            self._device_name_data_source = DisplayDataSource()
            self._on_device_name_changed()
        return self._device_name_data_source

    def update(self):
        if self.is_enabled() and self._device != None:
            self._device_bank_registry[self._device] = self._bank_index
            if self._parameter_controls != None:
                old_bank_name = self._bank_name
                self._assign_parameters()
                if self._bank_name != old_bank_name:
                    self._show_msg_callback(self._device.name + ' Bank: ' + self._bank_name)
            if self._bank_up_button != None and self._bank_down_button != None:
                if self.number_of_parameter_banks() > self._bank_index + 1:
                    self._bank_up_button.turn_on()
                else:
                    self._bank_up_button.turn_off()
                if self._bank_index > 0:
                    self._bank_down_button.turn_on()
                else:
                    self._bank_down_button.turn_off()
            if self._bank_buttons != None:
                for index in range(len(self._bank_buttons)):
                    if index == self._bank_index:
                        self._bank_buttons[index].turn_on()
                    else:
                        self._bank_buttons[index].turn_off()

        else:
            if self._lock_button != None:
                self._lock_button.turn_off()
            if self._bank_up_button != None:
                self._bank_up_button.turn_off()
            if self._bank_down_button != None:
                self._bank_down_button.turn_off()
            if self._bank_buttons != None:
                for button in self._bank_buttons:
                    button.turn_off()

            if self._parameter_controls != None:
                for control in self._parameter_controls:
                    control.release_parameter()

    def _bank_up_value(self, value):
        raise self._bank_up_button != None or AssertionError
        raise value != None or AssertionError
        raise isinstance(value, int) or AssertionError
        if self.is_enabled():
            if not self._bank_up_button.is_momentary() or value is not 0:
                if self._device != None:
                    num_banks = self._number_of_parameter_banks()
                    if self._bank_down_button == None:
                        self._bank_name = ''
                        self._bank_index = (self._bank_index + 1) % num_banks
                        self.update()
                    elif num_banks > self._bank_index + 1:
                        self._bank_name = ''
                        self._bank_index += 1
                        self.update()

    def _bank_down_value(self, value):
        if not self._bank_down_button != None:
            raise AssertionError
            raise value != None or AssertionError
            if not isinstance(value, int):
                raise AssertionError
                if self.is_enabled():
                    self._bank_name = (not self._bank_down_button.is_momentary() or value is not 0) and self._device != None and self._bank_index > 0 and ''
                    self._bank_index -= 1
                    self.update()

    def _lock_value(self, value):
        if not self._lock_button != None:
            raise AssertionError
            raise self._lock_callback != None or AssertionError
            raise value != None or AssertionError
            raise isinstance(value, int) or AssertionError
            (not self._lock_button.is_momentary() or value is not 0) and self._lock_callback()

    def _on_off_value(self, value):
        if not self._on_off_button != None:
            raise AssertionError
            if not value in range(128):
                raise AssertionError
                parameter = (not self._on_off_button.is_momentary() or value is not 0) and self._on_off_parameter()
                parameter.value = parameter != None and parameter.is_enabled and float(int(parameter.value == 0.0))

    def _bank_value(self, value, button):
        if not self._bank_buttons != None:
            raise AssertionError
            raise value != None or AssertionError
            raise button != None or AssertionError
            raise isinstance(value, int) or AssertionError
            raise isinstance(button, ButtonElement) or AssertionError
            if not list(self._bank_buttons).count(button) == 1:
                raise AssertionError
                if self.is_enabled() and self._device != None:
                    if not button.is_momentary() or value is not 0:
                        bank = list(self._bank_buttons).index(button)
                        self._bank_name = bank != self._bank_index and self._number_of_parameter_banks() > bank and ''
                        self._bank_index = bank
                        self.update()
                else:
                    self._show_msg_callback(self._device.name + ' Bank: ' + self._bank_name)

    def _is_banking_enabled(self):
        direct_banking = self._bank_buttons != None
        roundtrip_banking = self._bank_up_button != None
        increment_banking = self._bank_up_button != None and self._bank_down_button != None
        return direct_banking or roundtrip_banking or increment_banking

    def _assign_parameters(self):
        if not self.is_enabled():
            raise AssertionError
            raise self._device != None or AssertionError
            if not self._parameter_controls != None:
                raise AssertionError
                self._bank_name = 'Bank ' + str(self._bank_index + 1)
                if not (self._device.class_name in self._device_banks.keys() and self._device.class_name in self._device_best_banks.keys()):
                    raise AssertionError
                    banks = self._device_banks[self._device.class_name]
                    bank = None
                    if len(banks) > self._bank_index:
                        bank = banks[self._bank_index]
                        self._bank_name[self._bank_index] = self._is_banking_enabled() and self._device.class_name in self._device_bank_names.keys() and self._device_bank_names[self._device.class_name]
            raise bank == None or len(bank) >= len(self._parameter_controls) or AssertionError
            for index in range(len(self._parameter_controls)):
                parameter = None
                if bank != None:
                    parameter = get_parameter_by_name(self._device, bank[index])
                if parameter != None:
                    self._parameter_controls[index].connect_to(parameter)
                else:
                    self._parameter_controls[index].release_parameter()

        else:
            parameters = self._device_parameters_to_map()
            num_controls = len(self._parameter_controls)
            index = self._bank_index * num_controls
            for control in self._parameter_controls:
                if index < len(parameters):
                    control.connect_to(parameters[index])
                else:
                    control.release_parameter()
                index += 1

    def _on_device_name_changed(self):
        if self._device_name_data_source != None:
            if self.is_enabled() and self._device != None:
                self._device_name_data_source.set_display_string(self._device.name)
            else:
                self._device_name_data_source.set_display_string('No Device')

    def _on_parameters_changed(self):
        self.update()

    def _on_off_parameter(self):
        result = None
        if self._device != None:
            for parameter in self._device.parameters:
                if str(parameter.name).startswith('Device On'):
                    result = parameter
                    break

        return result

    def _on_on_off_changed(self):
        if self.is_enabled() and self._on_off_button != None:
            turn_on = False
            if self._device != None:
                parameter = self._on_off_parameter()
                if parameter != None:
                    turn_on = parameter.value > 0.0
                turn_on and self._on_off_button.turn_on()
            else:
                self._on_off_button.turn_off()

    def _device_parameters_to_map(self):
        raise self.is_enabled() or AssertionError
        raise self._device != None or AssertionError
        raise self._parameter_controls != None or AssertionError
        return self._device.parameters[1:]

    def _number_of_parameter_banks(self):
        return number_of_parameter_banks(self._device)


class PadOffsetComponent(ModeSelectorComponent):
    __module__ = __name__

    def __init__(self, script, *a, **k):
        super(PadOffsetComponent, self).__init__(*a, **k)
        self._script = script
        self._set_protected_mode_index(0)

    def set_mode_buttons(self, buttons):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                raise isinstance(button, ButtonElement) or AssertionError
                identify_sender = True
                button.add_value_listener(self._mode_value, identify_sender)
                self._modes_buttons.append(button)

            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._script.log_message('turn on ' + str(index))
                    self._modes_buttons[index].turn_on(True)
                else:
                    self._modes_buttons[index].turn_off(True)

    def number_of_modes(self):
        return 8

    def update(self):
        if self.is_enabled() is True:
            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._modes_buttons[index].send_value(127, True)
                else:
                    self._modes_buttons[index].send_value(0, True)

        else:
            for button in self._modes_buttons:
                button.send_value(0, True)


class TweakerMonoButtonElement(MonoButtonElement):

    def __init__(self, *a, **k):
        super(TweakerMonoButtonElement, self).__init__(*a, **k)
        self._color_map = COLOR_MAP


class Tweaker(ControlSurface):
    __module__ = __name__
    __doc__ = ' Tweaker control surface script '

    def __init__(self, c_instance, *a, **k):
        super(Tweaker, self).__init__(c_instance, *a, **k)
        with self.component_guard():
            self._update_linked_device_selection = None
            self._tweaker_version_check = '0.3'
            self.log_message('--------------= Tweaker Session ' + str(self._tweaker_version_check) + ' log opened =--------------')
            self._timer = 0
            self.flash_status = 1
            self._last_selected_strip_number = 0
            self._device_selection_follows_track_selection = False
            self._linked_session = None
            self._mixer_offset = 0
            self._nav_lock = True
            self._setup_controls()
            self._setup_transport_control()
            self._setup_device_control()
            self._setup_mixer_control()
            self._setup_session_control()
            self._setup_crossfader()
            self._setup_modes()
            self._setup_pads()
            self._setup_navigation_lock()
            self._setup_arrange_session_toggle()
            self.show_message('Tweaker Control Surface Loaded')
        self.show_message('Tweaker Control Surface Loaded')
        self.assign_main_configuration()
        self.schedule_message(3, self._mixer._reassign_tracks)

    def _setup_controls(self):
        is_momentary = True
        self._grid = [ None for index in range(8) ]
        for column in range(8):
            self._grid[column] = [ TweakerMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, column + row * 8 + 1, 'Grid_' + str(column) + '_' + str(row), self) for row in range(4) ]

        self._button = [ TweakerMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, TWEAKER_BUTTONS[index], 'Button_' + str(index), self) for index in range(len(TWEAKER_BUTTONS)) ]
        self._nav = [ TweakerMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, TWEAKER_NAVS[index], 'Nav_' + str(index), self) for index in range(len(TWEAKER_NAVS)) ]
        self._encoder_button = [ TweakerMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, TWEAKER_ENCODER_BUTTONS[index], 'Encoder_Button_' + str(index), self) for index in range(len(TWEAKER_ENCODER_BUTTONS)) ]
        self._dial = [ EncoderElement(MIDI_CC_TYPE, CHANNEL, TWEAKER_DIALS[index], Live.MidiMap.MapMode.absolute) for index in range(len(TWEAKER_DIALS)) ]
        self._fader = [ EncoderElement(MIDI_CC_TYPE, CHANNEL, TWEAKER_FADERS[index], Live.MidiMap.MapMode.absolute) for index in range(len(TWEAKER_FADERS)) ]
        self._crossfader = EncoderElement(MIDI_CC_TYPE, CHANNEL, CROSSFADER, Live.MidiMap.MapMode.absolute)
        self._encoder = [ EncoderElement(MIDI_CC_TYPE, CHANNEL, TWEAKER_ENCODERS[index], Live.MidiMap.MapMode.absolute) for index in range(len(TWEAKER_ENCODERS)) ]
        self._pad = [ TweakerMonoButtonElement(False, MIDI_NOTE_TYPE, CHANNEL, TWEAKER_PADS[index], 'Pad_' + str(index), self) for index in range(len(TWEAKER_PADS)) ]
        for index in range(4):
            self._pad[index].set_enabled(False)
            self._pad[index].set_channel(PAD_CHANNEL)
            self._pad[index].set_identifier(index + 4)
            self._pad[index + 4].set_enabled(False)
            self._pad[index + 4].set_channel(PAD_CHANNEL)
            self._pad[index + 4].set_identifier(index)

        self._pad_pressure = [ EncoderElement(MIDI_CC_TYPE, CHANNEL, TWEAKER_PAD_PRESSURES[index], Live.MidiMap.MapMode.absolute) for index in range(len(TWEAKER_PADS)) ]
        for index in range(8):
            self._pad_pressure[index]._last_sent = 0

        self._matrix = ButtonMatrixElement()
        self._matrix.name = 'Matrix'
        for row in range(4):
            button_row = []
            for column in range(7):
                button_row.append(self._grid[column][row])

            self._matrix.add_row(tuple(button_row))

        self._send_midi(tuple([240,
         0,
         1,
         106,
         1,
         7,
         21,
         21,
         247]))
        self._send_midi(tuple([240,
         0,
         1,
         106,
         1,
         6,
         127,
         127,
         25,
         0,
         15,
         0,
         9,
         PAD_SENSITIVITY,
         247]))

    def _setup_transport_control(self):
        self._transport = TransportComponent()
        self._transport.name = 'Transport'

    def _setup_mixer_control(self):
        is_momentary = True
        self._num_tracks = 2
        self._mixer = MixerComponent(2, 0, False, False)
        self._mixer.name = 'Mixer'
        self._mixer.tracks_to_use = self._mixer_tracks_to_use(self._mixer)
        self._device_navigator = [ None for index in range(2) ]
        self._mixer.set_track_offset(0)
        for index in range(2):
            self._mixer.channel_strip(index).set_volume_control(self._fader[index])
            self._mixer.channel_strip(index)._on_cf_assign_changed = self._channelstrip_on_cf_assign_changed(self._mixer.channel_strip(index))
            self._mixer.channel_strip(index).name = 'Mixer_ChannelStrip_' + str(index)
            self._mixer.channel_strip(index)._invert_mute_feedback = True
            self._mixer.channel_strip(index)._device_component = self._device[index]
            self._mixer.channel_strip(index).update = self._channelstrip_update(self._mixer.channel_strip(index))
            self._mixer.channel_strip(index)._select_value = self._channelstrip_select_value(self._mixer.channel_strip(index), index)
            self._device_navigator[index] = DetailViewControllerComponent(self, self._mixer.channel_strip(index))
            self._device_navigator[index].name = 'Device_Navigator_' + str(index)

        self._mixer.channel_strip(0).set_track = self._channelstrip_set_track(self._mixer.channel_strip(0), self._channelstrip1_cb)
        self._mixer.channel_strip(1).set_track = self._channelstrip_set_track(self._mixer.channel_strip(1), self._channelstrip2_cb)
        self.song().view.selected_track = self._mixer.channel_strip(0)._track

    def _setup_session_control(self):
        is_momentary = True
        num_tracks = NUM_TRACKS
        num_scenes = NUM_SCENES
        self._session = SessionComponent(num_tracks, num_scenes)
        self._session.name = 'Session'
        self._session.set_offsets(0, 0)
        self._session.set_stop_track_clip_value(STOP_CLIP)
        self._scene = [ None for index in range(3) ]
        for row in range(num_scenes):
            self._scene[row] = self._session.scene(row)
            self._scene[row].name = 'Scene_' + str(row)
            for column in range(num_tracks):
                clip_slot = self._scene[row].clip_slot(column)
                clip_slot.name = str(column) + '_Clip_Slot_' + str(row)
                clip_slot.set_triggered_to_play_value(CLIP_TRG_PLAY)
                clip_slot.set_triggered_to_record_value(CLIP_TRG_REC)
                clip_slot.set_stopped_value(CLIP_STOP)
                clip_slot.set_started_value(CLIP_STARTED)
                clip_slot.set_recording_value(CLIP_RECORDING)

        self._session._stop_track_value = self._session_stop_track_value(self._session)
        self._session._on_fired_slot_index_changed = self._session_on_fired_slot_index_changed(self._session)
        self._session._change_offsets = self._session_change_offsets(self._session)
        self._session.update = self._session_update(self._session)
        self._session.set_mixer(self._mixer)
        self.set_highlighting_session_component(self._session)
        self._session_zoom = SessionZoomingComponent(self._session)
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_stopped_value(ZOOM_STOPPED)
        self._session_zoom.set_playing_value(ZOOM_PLAYING)
        self._session_zoom.set_selected_value(ZOOM_SELECTED)

    def _setup_device_control(self):
        self._device = [ None for index in range(2) ]
        for index in range(2):
            self._device[index] = DeviceComponent()
            self._device[index].name = 'Device_Component_' + str(index)
            self._device[index].set_enabled(True)
            self._device[index]._number_of_parameter_banks = self._device_number_of_parameter_banks(self._device[index])
            self._device[index]._assign_parameters = self._device_assign_parameters(self._device[index])
            self._device[index]._device_banks = DEVICE_DICT
            self._device[index]._device_best_banks = DEVICE_BOB_DICT
            self._device[index]._device_bank_names = BANK_NAME_DICT

    def _setup_crossfader(self):
        self._mixer.set_crossfader_control(self._crossfader)

    def _setup_modes(self):
        self._pad_offset = PadOffsetComponent(self)
        self._pad_offset._set_protected_mode_index(0)
        self._pad_offset.set_enabled(False)

    def _setup_pads(self):
        for pad in self._pad_pressure:
            pad.add_value_listener(self._light_pad, True)

    def _setup_navigation_lock(self):
        if self._encoder_button[0].value_has_listener(self._nav_lock_value):
            self._encoder_button[0].remove_value_listener(self._nav_lock_value)
        self._encoder_button[0].add_value_listener(self._nav_lock_value)

    def _setup_arrange_session_toggle(self):
        if self._nav[1].value_has_listener(self._arrange_session_value):
            self._nav[1].remove_value_listener(self._arrange_session_value)
        self._nav[1].add_value_listener(self._arrange_session_value)

    def assign_main_configuration(self):
        for column in range(7):
            for row in range(3):
                self._scene[row].clip_slot(column).set_launch_button(self._grid[column][row])

        self._session.set_stop_track_clip_buttons(tuple([ self._grid[index][3] for index in range(7) ]))
        for row in range(3):
            self._scene[row].set_launch_button(self._grid[7][row])

        self._device[0].set_parameter_controls(tuple([ self._encoder[index + 1] for index in range(3) ]))
        self._device[0].set_enabled(True)
        self._device[1].set_parameter_controls(tuple([ self._encoder[index + 4] for index in range(3) ]))
        self._device[1].set_enabled(True)
        for track in range(2):
            self._mixer.channel_strip(track).set_volume_control(self._fader[track])
            self._mixer.channel_strip(track).set_solo_button(self._button[track * 3])
            self._button[track * 3].set_on_off_values(SOLO, 0)
            self._mixer.channel_strip(track).set_arm_button(self._button[1 + track * 3])
            self._button[1 + track * 3].set_on_off_values(ARM, 0)
            self._mixer.channel_strip(track).set_crossfade_toggle(self._button[2 + track * 3])

        self._mixer.master_strip().set_volume_control(self._dial[1])
        self._mixer.set_prehear_volume_control(self._dial[0])
        self._session.set_track_bank_buttons(self._nav[4], self._nav[3])
        self._session.set_scene_bank_buttons(self._nav[2], self._nav[0])
        self._session_zoom.set_zoom_button(self._grid[7][3])
        self._session_zoom.set_nav_buttons(self._nav[0], self._nav[2], self._nav[3], self._nav[4])
        self._session_zoom.set_button_matrix(self._matrix)
        self._device[0].set_on_off_button(self._encoder_button[1])
        self._device_navigator[0].set_device_nav_buttons(self._encoder_button[2], self._encoder_button[3])
        self._device[1].set_on_off_button(self._encoder_button[4])
        self._device_navigator[1].set_device_nav_buttons(self._encoder_button[5], self._encoder_button[6])
        for track in range(2):
            self._update_device(self._mixer.channel_strip(track))

        self.assign_track_selector(self._encoder[0])
        if not self._grid[7][3].value_has_listener(self._shift_value):
            self._grid[7][3].add_value_listener(self._shift_value)
        self._grid[7][3].send_value(127, True)
        self.request_rebuild_midi_map()

    def _shift_value(self, value):
        self._pad_offset.set_enabled(value > 0)
        if value > 0:
            self._update_navigation_view()
            for pad in self._pad:
                pad.use_default_message()
                pad.set_enabled(True)

            self._pad_offset.set_mode_buttons(tuple(self._pad))
            self.schedule_message(1, self._pad_offset.update)
            if self._session.is_enabled():
                self._update_navigation_view()
            self._grid[7][3].send_value(SHIFT_ON)
            for track in range(2):
                self._mixer.channel_strip(track).set_crossfade_toggle(None)
                self._mixer.channel_strip(track).set_select_button(self._button[2 + track * 3])

        else:
            self._pad_offset.set_mode_buttons(None)
            for index in range(4):
                self._pad[index].set_enabled(False)
                self._pad[index].set_channel(PAD_CHANNEL)
                self._pad[index].set_identifier(index + 4 + self._pad_offset._mode_index * 8)
                self._pad[index + 4].set_enabled(False)
                self._pad[index + 4].set_channel(PAD_CHANNEL)
                self._pad[index + 4].set_identifier(index + self._pad_offset._mode_index * 8)

            self._grid[7][3].send_value(SHIFT_OFF)
            for track in range(2):
                self._mixer.channel_strip(track).set_select_button(None)
                self._mixer.channel_strip(track).set_crossfade_toggle(self._button[2 + track * 3])

    def assign_track_selector(self, encoder):
        if not isinstance(encoder, EncoderElement):
            raise AssertionError
            encoder.value_has_listener(self._track_selector_value) or encoder.add_value_listener(self._track_selector_value)

    def deassign_track_selector(self, encoder):
        if encoder.value_has_listener(self._track_selector_value):
            encoder.remove_value_listener(self._track_selector_value)

    def _nav_lock_value(self, value):
        if value > 0:
            if self._nav_lock:
                self._mixer_offset = self._mixer_offset + self._session._track_offset
                self._mixer.set_track_offset(self._mixer_offset)
            else:
                if self._mixer_offset in range(self._session._track_offset, self._session._track_offset + 5):
                    self._mixer_offset = self._mixer_offset - self._session._track_offset
                elif self._mixer_offset < self._session._track_offset:
                    self._mixer_offset = 0
                else:
                    self._mixer_offset = min(self._session._track_offset + 5, len(self._session.tracks_to_use()) - 2)
                self._mixer.set_track_offset(self._session._track_offset + self._mixer_offset)
            self._nav_lock = not self._nav_lock
            self._session.update()

    def _arrange_session_value(self, value):
        if value > 0:
            if self.application().view.is_view_visible('Arranger'):
                self.application().view.show_view('Session')
            else:
                self.application().view.show_view('Arranger')

    def _track_selector_value(self, value):
        if value is 1:
            if self._nav_lock:
                self._mixer_offset = min(self._mixer_offset + 1, min(NUM_TRACKS - 2, len(self._session.tracks_to_use()) - self._session._track_offset - 2))
            else:
                self._mixer_offset = min(self._mixer_offset + 1, len(self._session.tracks_to_use()) - 2)
        elif value is 127:
            self._mixer_offset = max(self._mixer_offset - 1, 0)
        if self._nav_lock:
            self._mixer.set_track_offset(self._session._track_offset + self._mixer_offset)
        else:
            self._mixer.set_track_offset(self._mixer_offset)
        self._session.update()
        if self._mixer.channel_strip(self._last_selected_strip_number)._track != None:
            self.song().view.selected_track = self._mixer.channel_strip(self._last_selected_strip_number)._track
        if self._linked_session != None:
            if self._linked_session._is_linked():
                self._linked_session._unlink()
            self._linked_session.set_offsets(self._mixer._track_offset, self._linked_session._scene_offset)
            self._linked_session._link()

    def _update_navigation_view(self):
        dif = self._mixer._track_offset - self._session._track_offset
        for index in range(7):
            if index + self._session._track_offset in range(0, len(self.song().visible_tracks)):
                self._grid[index][3].send_value(NAV_COLORS[int(index in range(dif, dif + 2))], True)
            elif index + self._session._track_offset in range(len(self.song().visible_tracks), len(self._session.tracks_to_use())):
                self._grid[index][3].send_value(RETURN_NAV_COLORS[int(index in range(dif, dif + 2))], True)
            else:
                self._grid[index][3].send_value(0, True)

        self._send_midi(tuple([240,
         0,
         1,
         106,
         1,
         7,
         21,
         21,
         247]))

    def _update_device(self, channelstrip):
        for control in channelstrip._device_component._parameter_controls:
            control.send_value(0, True)

        if channelstrip._device_component._on_off_button != None:
            channelstrip._device_component._on_off_button.turn_off()
        if channelstrip._track is not None:
            if channelstrip._device_component._device not in channelstrip._track.devices:
                track = channelstrip._track
                device_to_select = track.view.selected_device
                if device_to_select == None and len(track.devices) > 0:
                    device_to_select = track.devices[0]
                elif channelstrip._device_component and type(channelstrip._device_component) is not type(None):
                    channelstrip._device_component.set_device(device_to_select)
                else:
                    channelstrip._device_component.set_device(None)
        else:
            channelstrip._device_component.set_device(None)
        channelstrip._device_component._on_on_off_changed()

    def _light_pad(self, value, sender):
        if not self._pad_offset.is_enabled():
            if value > sender._last_sent:
                if self._pad[self._pad_pressure.index(sender)]._last_sent_value < 1:
                    self._pad[self._pad_pressure.index(sender)].send_value(127, True)
            else:
                self._pad[self._pad_pressure.index(sender)].send_value(0, True)
        sender._last_sent = value

    def update_display(self):
        super(Tweaker, self).update_display()
        self._timer = (self._timer + 1) % 256
        self.flash()

    def flash(self):
        if self.flash_status > 0:
            for control in self.controls:
                if isinstance(control, TweakerMonoButtonElement):
                    control.flash(self._timer)

    def generate_strip_string(self, display_string):
        NUM_CHARS_PER_DISPLAY_STRIP = 12
        if not display_string:
            return ' ' * NUM_CHARS_PER_DISPLAY_STRIP
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
        return ret

    def notification_to_bridge(self, name, value, sender):
        if isinstance(sender, MonoEncoderElement2):
            self._monobridge._send(sender.name, 'lcd_name', str(self.generate_strip_string(name)))
            self._monobridge._send(sender.name, 'lcd_value', str(self.generate_strip_string(value)))

    def touched(self):
        if self._shift_mode._mode_index < 2:
            if self._touched is 0:
                self._monobridge._send('touch', 'on')
                self.schedule_message(2, self.check_touch)
            self._touched += 1

    def check_touch(self):
        if self._shift_mode._mode_index < 2:
            if self._touched > 5:
                self._touched = 5
            elif self._touched > 0:
                self._touched -= 1
            if self._touched is 0:
                self._monobridge._send('touch', 'off')
            else:
                self.schedule_message(2, self.check_touch)

    def handle_sysex(self, midi_bytes):
        pass

    def disconnect(self):
        """clean things up on disconnect"""
        if self._session.offset_has_listener(self._update_navigation_view):
            self._session.remove_offset_listener(self._update_navigation_view)
        if self._nav[1].value_has_listener(self._arrange_session_value):
            self._nav[1].remove_value_listener(self._arrange_session_value)
        if self._encoder_button[0].value_has_listener(self._nav_lock_value):
            self._encoder_button[0].remove_value_listener(self._nav_lock_value)
        for pad in self._pad_pressure:
            if pad.value_has_listener(self._light_pad):
                pad.remove_value_listener(self._light_pad)

        if self._grid[7][3].value_has_listener(self._shift_value):
            self._grid[7][3].remove_value_listener(self._shift_value)
        if self._session._is_linked():
            self._session._unlink()
        self.deassign_track_selector(self._encoder[0])
        self.log_message('--------------= Tweaker Session ' + str(self._tweaker_version_check) + ' log closed =--------------')
        super(Tweaker, self).disconnect()

    def _get_num_tracks(self):
        return self.num_tracks

    def _on_selected_track_changed(self):
        super(Tweaker, self)._on_selected_track_changed()
        if self._session.is_enabled():
            self._session.update()
        for index in range(2):
            self._update_device(self._mixer.channel_strip(index))
            self._mixer.on_selected_track_changed()

    def connect_script_instances(self, instanciated_scripts):
        link = False
        for s in instanciated_scripts:
            if '_tweaker_version' in dir(s):
                if s._tweaker_version == self._tweaker_version_check:
                    link = True
                    break

        if link == True:
            if not self._session._is_linked():
                self._session._link()

    def _session_update(self, session):

        def _update():
            SessionComponent.update(session)
            if session.is_enabled():
                self._update_navigation_view()

        return _update

    def _session_change_offsets(self, session):

        def _change_offsets(track_increment, scene_increment):
            if not track_increment != 0:
                offsets_changed = scene_increment != 0
                offsets_changed and session._track_offset += track_increment
                session._scene_offset += scene_increment
                if not session._track_offset >= 0:
                    raise AssertionError
                    if not session._scene_offset >= 0:
                        raise AssertionError
                        if session._mixer != None:
                            if self._nav_lock:
                                if session.track_offset() + self._mixer_offset > len(session.tracks_to_use()) - 2:
                                    self._mixer_offset = max(len(session.tracks_to_use()) - session._track_offset - 2, 0)
                                session._mixer.set_track_offset(max(0, session.track_offset() + self._mixer_offset))
                    session._reassign_tracks()
                    if offsets_changed:
                        session._reassign_scenes()
                        session.notify_offset()
                        self._update_navigation_view()
                        self.song().view.selected_track = self._mixer.channel_strip(self._last_selected_strip_number)._track != None and self._mixer.channel_strip(self._last_selected_strip_number)._track
                    session.width() > 0 and session.height() > 0 and session._do_show_highlight()

        return _change_offsets

    def _session_on_fired_slot_index_changed(self, session):

        def _on_fired_slot_index_changed(index):
            tracks_to_use = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)
            track_index = index + session.track_offset()
            if session.is_enabled() and session._stop_track_clip_buttons != None:
                if index < len(session._stop_track_clip_buttons):
                    button = session._stop_track_clip_buttons[index]
                    if button != None:
                        if track_index < len(tracks_to_use) and tracks_to_use[track_index].clip_slots and tracks_to_use[track_index].fired_slot_index == -2:
                            button.send_value(session._stop_track_clip_value)
                        else:
                            self._update_navigation_view()

        return _on_fired_slot_index_changed

    def _session_stop_track_value(self, session):

        def _stop_track_value(value, sender):
            if not session._stop_track_clip_buttons != None:
                raise AssertionError
                raise list(session._stop_track_clip_buttons).count(sender) == 1 or AssertionError
                if not value in range(128):
                    raise AssertionError
                    if session.is_enabled():
                        tracks = (value is not 0 or not sender.is_momentary()) and session.tracks_to_use()
                        track_index = list(session._stop_track_clip_buttons).index(sender) + session.track_offset()
                        track_index in range(len(tracks)) and tracks[track_index] in session.song().tracks and tracks[track_index].stop_all_clips()
                    sender.send_value(3, True)
                    self.schedule_message(10, self._update_navigation_view)

        return _stop_track_value

    def _channelstrip_update(self, channelstrip):

        def _update():
            ChannelStripComponent.update(channelstrip)
            self._update_device(channelstrip)

        return _update

    def _channelstrip_set_track(self, channelstrip, cb):

        def _set_track(track):
            if not (track == None or isinstance(track, Live.Track.Track)):
                raise AssertionError
                if channelstrip._track != None and isinstance(channelstrip._track, Live.Track.Track):
                    if channelstrip._track.devices_has_listener(cb):
                        channelstrip._track.remove_devices_listener(cb)
                track != None and track.add_devices_listener(cb)
            ChannelStripComponent.set_track(channelstrip, track)

        return _set_track

    def _channelstrip_select_value(self, channelstrip, index):

        def _select_value(value):
            ChannelStripComponent._select_value(channelstrip, value)
            self._last_selected_strip_number = index

        return _select_value

    def _channelstrip_on_cf_assign_changed(self, channel_strip):

        def _on_cf_assign_changed():
            if channel_strip.is_enabled() and channel_strip._crossfade_toggle != None:
                if channel_strip._track != None and channel_strip._track in chain(self.song().tracks, self.song().return_tracks):
                    if channel_strip._track.mixer_device.crossfade_assign == 1:
                        channel_strip._crossfade_toggle.turn_off()
                    elif channel_strip._track.mixer_device.crossfade_assign == 0:
                        channel_strip._crossfade_toggle.send_value(CROSSFADE_A)
                    else:
                        channel_strip._crossfade_toggle.send_value(CROSSFADE_B)

        return _on_cf_assign_changed

    def _channelstrip1_cb(self):
        self._on_selected_track_changed()

    def _channelstrip2_cb(self):
        self._on_selected_track_changed()

    def _mixer_tracks_to_use(self, mixer):

        def tracks_to_use():
            return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

        return tracks_to_use

    def _device_number_of_parameter_banks(self, device):

        def _number_of_parameter_banks():
            return number_of_parameter_banks(device._device)

        return _number_of_parameter_banks

    def _device_assign_parameters(self, device):

        def _assign_parameters():
            if not device.is_enabled():
                raise AssertionError
                raise device._device != None or AssertionError
                if not device._parameter_controls != None:
                    raise AssertionError
                    device._bank_name = 'Bank ' + str(device._bank_index + 1)
                    if not (device._device.class_name in device._device_banks.keys() and device._device.class_name in device._device_best_banks.keys()):
                        raise AssertionError
                        banks = device._device_banks[device._device.class_name]
                        bank = None
                        if not device._is_banking_enabled():
                            banks = device._device_best_banks[device._device.class_name]
                            device._bank_name = 'Best of Parameters'
                        if len(banks) > device._bank_index:
                            bank = banks[device._bank_index]
                            device._bank_name[device._bank_index] = device._is_banking_enabled() and device._device.class_name in device._device_bank_names.keys() and device._device_bank_names[device._device.class_name]
                raise bank == None or len(bank) >= len(device._parameter_controls) or AssertionError
                for index in range(len(device._parameter_controls)):
                    parameter = None
                    if bank != None:
                        parameter = get_parameter_by_name(device._device, bank[index])
                    if parameter != None:
                        device._parameter_controls[index].connect_to(parameter)
                    else:
                        device._parameter_controls[index].release_parameter()

            else:
                parameters = device._device_parameters_to_map()
                num_controls = len(device._parameter_controls)
                index = device._bank_index * num_controls
                for control in device._parameter_controls:
                    if index < len(parameters):
                        control.connect_to(parameters[index])
                    else:
                        control.release_parameter()
                    index += 1

        return _assign_parameters