#Embedded file name: /Applications/Ableton Live 9 Standard.app/Contents/App-Resources/MIDI Remote Scripts/Lemur256_b995_9/Lemur256.py
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


class Lemur256(ControlSurface):
    __module__ = __name__
    __doc__ = ' Lemur Monomodular 256cell controller script '

    def __init__(self, *a, **k):
        self._timer_callbacks = []
        super(Lemur256, self).__init__(*a, **k)
        self._host_name = 'Lemur256'
        self._color_type = 'AumPad'
        self.connected = 0
        self._suggested_input_port = 'None'
        self._suggested_output_port = 'None'
        self._monomod_version = 'b995'
        self.hosts = []
        self._bright = True
        self._rgb = 0
        self._timer = 0
        self.flash_status = 1
        self._osc_registry = {}
        with self.component_guard():
            self._setup_monobridge()
            self._setup_controls()
            self._setup_monomod()
            self._setup_touchosc()
            self._assign_host2()
        self.reset()
        self.refresh_state()
        self.show_message(str(self._host_name) + ' Control Surface Loaded')
        self.log_message('<<<<<<<<<<<<<<<<<<<<  ' + str(self._host_name) + ' ' + str(self._monomod_version) + ' log opened   >>>>>>>>>>>>>>>>>>>>')

    def _setup_controls(self):
        is_momentary = True
        self._monomod256 = ButtonMatrixElement()
        self._monomod256.name = 'Monomod256'
        self._square = [ None for index in range(16) ]
        for column in range(16):
            self._square[column] = [ None for index in range(16) ]
            for row in range(16):
                self._square[column][row] = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, int(column / 8) + 1, row + column % 8 * 16, '256Grid_' + str(column) + '_' + str(row), '/Grid_' + str(column) + '_' + str(row), '/Grid/set ' + str(column) + ' ' + str(row), None, self)

        for row in range(16):
            button_row = []
            for column in range(16):
                button_row.append(self._square[column][row])

            self._monomod256.add_row(tuple(button_row))

        self._key_buttons = ButtonMatrixElement()
        self._bank_button = [ None for index in range(2) ]
        for index in range(2):
            self._bank_button[index] = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, index, '256Grid_Bank_' + str(index), '/Shift_' + str(index), '/Shift/set ' + str(index), None, self)

        button_row = []
        self._key_button = [ None for index in range(8) ]
        for index in range(8):
            self._key_button[index] = OSCMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, 15, index + 8, '256Grid_Key_' + str(index), '/Keys_' + str(index), '/Keys/set ' + str(index), None, self)

        for index in range(8):
            button_row.append(self._key_button[index])

        self._key_buttons.add_row(tuple(button_row))

    def _setup_monomod(self):
        self._host2 = SpecialMonomodComponent(self)
        self._host2.name = '256_Monomod_Host'
        self.hosts = [self._host2]

    def _setup_monobridge(self):
        self._monobridge = OSCMonoBridgeElement(self)
        self._monobridge.name = 'MonoBridge'

    def _assign_host2(self):
        self._host2._set_shift_button(self._bank_button[0])
        self._host2._set_alt_button(self._bank_button[1])
        self._host2._set_button_matrix(self._monomod256)
        self._host2._set_key_buttons(self._key_button)
        self._host2.set_enabled(True)

    def _setup_touchosc(self):
        self._osc_registry = {}
        self._osc_registry['/ping'] = self._monobridge.ping
        self._osc_registry['/1'] = self._monobridge.page1
        for control in self.controls:
            if hasattr(control, 'osc'):
                self._osc_registry[control.osc] = control.set_value

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
        super(Lemur256, self).update_display()
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
        self.log_message('<<<<<<<<<<<<<<<<<<<<  ' + str(self._host_name) + ' log closed   >>>>>>>>>>>>>>>>>>>>')
        super(ControlSurface, self).disconnect()

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