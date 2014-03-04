
from __future__ import with_statement
import Live
import time
import math
import sys
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
from _Mono_Framework.CodecEncoderElement import CodecEncoderElement
from _Mono_Framework.EncoderMatrixElement import EncoderMatrixElement
from _Mono_Framework.MonoChopperComponent import MonoChopperComponent
from _Mono_Framework.MonoBridgeElement import MonoBridgeElement
from _Mono_Framework.MonoButtonElement import MonoButtonElement
from _Mono_Framework.MonoEncoderElement import MonoEncoderElement
from _Mono_Framework.ResetSendsComponent import ResetSendsComponent
from _Mono_Framework.DetailViewControllerComponent import DetailViewControllerComponent
from _Mono_Framework.DeviceSelectorComponent import DeviceSelectorComponent
from _Mono_Framework.MonomodComponent import MonomodComponent
from _Mono_Framework.MonoDeviceComponent import MonoDeviceComponent
from _Mono_Framework.SwitchboardElement import SwitchboardElement
from _Mono_Framework.MonoClient import MonoClient
from _Mono_Framework.LiveUtils import *
from _Generic.Devices import *
from ModDevices import *
from Map import *
switchxfader = (240, 0, 1, 97, 2, 15, 1, 247)
switchxfaderrgb = (240, 0, 1, 97, 7, 15, 1, 247)
assigncolors = (240, 0, 1, 97, 7, 34, 0, 7, 3, 6, 5, 1, 2, 4, 247)
assign_default_colors = (240, 0, 1, 97, 7, 34, 0, 7, 6, 5, 1, 4, 3, 2, 247)
check_model = (240, 126, 127, 6, 1, 247)
factoryreset = (240, 0, 1, 97, 8, 6, 247)
btn_channels = (240,
 0,
 1,
 97,
 8,
 19,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 0,
 247)
enc_channels = (240,
 0,
 1,
 97,
 8,
 20,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 CHANNEL,
 247)
SLOWENCODER = (240, 0, 1, 97, 8, 30, 69, 0, 247)
NORMALENCODER = (240, 0, 1, 97, 8, 30, 0, 0, 247)
FASTENCODER = (240, 0, 1, 97, 8, 30, 4, 0, 247)

class ShiftModeComponent(ModeSelectorComponent):

    def __init__(self, script, callback, *a, **k):
        super(ShiftModeComponent, self).__init__(*a, **k)
        self._script = script
        self.update = callback
        self._modes_buttons = []
        self._last_mode = 0
        self._set_protected_mode_index(0)

    def set_mode_buttons(self, buttons):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                raise isinstance(button, ButtonElement or FlashingButtonElement) or AssertionError
                identify_sender = True
                button.add_value_listener(self._mode_value, identify_sender)
                self._modes_buttons.append(button)

    def number_of_modes(self):
        return 5

    def set_mode(self, mode):
        if not isinstance(mode, int):
            raise AssertionError
            mode += 1
            raise mode in range(self.number_of_modes()) or AssertionError
            self._mode_index = self._mode_index != mode and mode
            self.update()
        elif self._mode_index != 0:
            self._mode_index = 0
            self.update()

    def _mode_value(self, value, sender):
        if not len(self._modes_buttons) > 0:
            raise AssertionError
            raise isinstance(value, int) or AssertionError
            raise isinstance(sender, ButtonElement) or AssertionError
            raise self._modes_buttons.count(sender) == 1 or AssertionError
            (value is not 0 or not sender.is_momentary()) and self.set_mode(self._modes_buttons.index(sender))


class MonomodModeComponent(ModeSelectorComponent):
    __module__ = __name__
    __doc__ = ' Class for switching between modes, handle several functions with few controls '

    def __init__(self, script, *a, **k):
        super(MonomodModeComponent, self).__init__(*a, **k)
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
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()

    def set_mode_toggle(self, button):
        if not (button == None or isinstance(button, ButtonElement or FlashingButtonElement)):
            raise AssertionError
            if self._mode_toggle != None:
                self._mode_toggle.remove_value_listener(self._toggle_value)
            self._mode_toggle = button
            self._mode_toggle != None and self._mode_toggle.add_value_listener(self._toggle_value)

    def number_of_modes(self):
        return 2


class CntrlrDetailViewControllerComponent(DetailViewControllerComponent):

    def __init__(self, script, *a, **k):
        super(CntrlrDetailViewControllerComponent, self).__init__(*a, **k)
        self._script = script

    def _nav_value(self, value, sender):
        super(CntrlrDetailViewControllerComponent, self)._nav_value(value, sender)
        if self.is_enabled() and not self._shift_pressed:
            if not sender.is_momentary() or value != 0:
                modifier_pressed = True
                if not not self.application().view.is_view_visible('Detail'):
                    not self.application().view.is_view_visible('Detail/DeviceChain') or self._script._update_selected_device()


class CntrlrSwitchboardElement(SwitchboardElement):

    def __init__(self, *a, **k):
        super(CntrlrSwitchboardComponent, self).__init__(*a, **k)


class CntrlrMonoDevice(MonoDeviceComponent):

    def __init__(self, *a, **k):
        super(CntrlrMonoDevice, self).__init__(*a, **k)


class CntrlrMonoClient(MonoClient):

    def __init__(self, *a, **k):
        super(CntrlrMonoClient, self).__init__(*a, **k)
        self._raw = False

    def _banner(self):
        pass

    def disconnect_client(self, *a, **k):
        super(CntrlrMonoClient, self).disconnect_client(*a, **k)
        if not self._mod_dial == None:
            if self._mod_dial._parameter is self._mod_dial_parameter:
                self._mod_dial.release_parameter()

    def _send_c_key(self, index, value, *a, **k):
        self._send('key', index, value)
        if self._raw is True:
            control = self._host._host._keys[index]
            if control != None:
                self._send('raw', control._msg_type + control._original_channel, control._original_identifier, value)

    def _send_c_grid(self, column, row, value, *a, **k):
        self._send('grid', column, row, value)
        if self._raw is True:
            control = self._host._host._grid.get_button(column, row)
            if control != None:
                self._send('raw', control._msg_type + control._original_channel, control._original_identifier, value)

    def _send_c_dial(self, column, row, value, *a, **k):
        self._send('dial', column, row, value)
        if self._raw is True:
            control = self._host._host._dial_matrix.get_dial(column, row)
            if control != None:
                self._send('raw', control._msg_type + control._original_channel, control._original_identifier, value)

    def _send_c_dial_button(self, column, row, value, *a, **k):
        if row > 0:
            self._send('dial_button', column, row - 1, value)
            if self._raw is True:
                control = self._host._host._dial_button_matrix.get_button(column, row)
                if control != None:
                    self._send('raw', control._msg_type + control._original_channel, control._original_identifier, value)

    def _send_key(self, *a):
        pass

    def _send_grid(self, *a):
        pass

    def _send_dial(self, *a):
        pass

    def _send_dial_button(self, *a):
        pass

    def receive_key(self, *a, **k):
        super(CntrlrMonoClient, self).receive_c_key(*a, **k)

    def receive_grid(self, *a, **k):
        super(CntrlrMonoClient, self).receive_c_grid(*a, **k)

    def receive_grid_row(self, *a, **k):
        super(CntrlrMonoClient, self).receive_c_grid_row(*a, **k)

    def receive_grid_column(self, *a, **k):
        super(CntrlrMonoClient, self).receive_c_grid_column(*a, **k)

    def receive_grid_all(self, *a, **k):
        super(CntrlrMonoClient, self).receive_c_grid_all(*a, **k)

    def receive_mask_key(self, *a, **k):
        super(CntrlrMonoClient, self).receive_mask_c_key(*a, **k)

    def receive_mask_grid(self, *a, **k):
        super(CntrlrMonoClient, self).receive_mask_c_grid(*a, **k)

    def receive_mask_column(self, *a, **k):
        super(CntrlrMonoClient, self).receive_mask_c_column(*a, **k)

    def receive_mask_row(self, row, value):
        super(CntrlrMonoClient, self).receive_mask_c_row(*a, **k)

    def receive_mask_all(self, *a, **k):
        super(CntrlrMonoClient, self).receive_mask_c_all(*a, **k)

    def receive_wheel(self, *a, **k):
        super(CntrlrMonoClient, self).receive_c_wheel(*a, **k)

    def set_local_ring_control(self, *a, **k):
        super(CntrlrMonoClient, self).set_c_local_ring_control(*a, **k)

    def set_absolute_mode(self, *a, **k):
        super(CntrlrMonoClient, self).set_c_absolute_mode(*a, **k)

    def receive_mod_color(self, val):
        if val != 1:
            self._mod_color = val
            self._host.shift_update()

    def set_raw_enabled(self, value):
        self._raw = value > 0
        if self._raw is True:
            self._update_controls_dictionary()

    def receive_raw(self, Type, Identifier, value):
        if self._controls[Type]:
            if Identifier in self._controls[Type]:
                self._controls[Type][Identifier](value)

    def _update_controls_dictionary(self):
        if self._host._host != None:
            self._controls = [{}, {}]
            if self._control_defs['grid'] != None:
                for column in range(self._control_defs['grid'].width()):
                    for row in range(self._control_defs['grid'].height()):
                        button = self._control_defs['grid'].get_button(column, row)
                        if button != None:
                            self._controls[0][button._original_identifier] = self._make_grid_call(column, row)

            if self._control_defs['keys'] != None:
                for index in range(len(self._control_defs['keys'])):
                    key = self._control_defs['keys'][index]
                    if key != None:
                        self._controls[0][key._original_identifier] = self._make_key_call(index)

            if self._control_defs['dials'] != None:
                for index in range(12):
                    column = index % 4
                    row = int(index / 4)
                    dial = self._control_defs['dials'].get_dial(column, row)
                    if dial != None:
                        self._controls[1][dial._original_identifier] = self._make_dial_call(index)

            if self._control_defs['buttons'] != None:
                for index in range(8):
                    column = index % 4
                    row = int(index / 4) + 1
                    button = self._control_defs['buttons'].get_button(column, row)
                    if button != None:
                        self._controls[0][button._original_identifier] = self._make_dial_button_call(index + 4)

    def _make_grid_call(self, column, row):

        def recieve_grid(value):
            self.receive_c_grid(column, row, value)

        return recieve_grid

    def _make_key_call(self, number):

        def receive_key(value):
            self.receive_c_key(number, value)

        return receive_key

    def _make_dial_call(self, number):

        def receive_c_wheel(value):
            self.receive_wheel(number, 'value', value)

        return receive_wheel

    def _make_dial_button_call(self, number):

        def receive_c_wheel(value):
            self.receive_wheel(number, 'white', value)

        return receive_wheel


class CntrlrMonomodComponent(MonomodComponent):

    def __init__(self, *a, **k):
        super(CntrlrMonomodComponent, self).__init__(*a, **k)
        self._alt_device_banks = MOD_TYPES

    def _send_grid(self, *a):
        pass

    def _send_key(self, *a):
        pass

    def disconnect(self, *a, **k):
        self._release_mod_dials()
        super(CntrlrMonomodComponent, self).disconnect(*a, **k)

    def connect_to_clients(self, *a, **k):
        super(CntrlrMonomodComponent, self).connect_to_clients(*a, **k)
        for index in range(4):
            self._client[index]._mod_dial = self._script._encoder[index]

    def _select_client(self, *a, **k):
        super(CntrlrMonomodComponent, self)._select_client(*a, **k)
        self._script.set_local_ring_control(self._active_client._c_local_ring_control)
        self._script.set_absolute_mode(self._active_client._c_absolute_mode)
        self._active_client._device_component.update()

    def on_enabled_changed(self, *a, **k):
        super(CntrlrMonomodComponent, self).on_enabled_changed(*a, **k)
        if self._active_client != None:
            if self.is_enabled():
                self._active_client._device_component.update()
                self._script.set_absolute_mode(self._active_client._c_absolute_mode)
                self._script.set_local_ring_control(self._active_client._c_local_ring_control)
            else:
                for control in self._parameter_controls:
                    control.release_parameter()

                self._script.set_absolute_mode(1)
                self._script.set_local_ring_control(1)

    def _set_button_matrix(self, grid):
        if not isinstance(grid, (ButtonMatrixElement, type(None))):
            raise AssertionError
            if grid != self._grid:
                if self._grid != None:
                    self._grid.remove_value_listener(self._matrix_value)
                self._grid = grid
                self._grid != None and self._grid.add_value_listener(self._matrix_value)
            self.update()

    def _matrix_value(self, value, x, y, is_momentary):
        if not self._grid != None:
            raise AssertionError
            raise value in range(128) or AssertionError
            raise isinstance(is_momentary, type(False)) or AssertionError
            self.is_enabled() and self._active_client._send_c_grid(x + self._x, y + self._y, value)

    def _update_grid(self):
        if self.is_enabled() and self._grid != None:
            for column in range(4):
                for row in range(4):
                    self._send_c_grid(column, row, self._active_client._c_grid[column][row])

    def _alt_value(self, value):
        if self._shift_pressed == 0:
            self._alt_pressed = value != 0
            self._active_client._send('alt', int(self._alt_pressed))
            self.update()

    def _set_key_buttons(self, buttons):
        if not (buttons == None or isinstance(buttons, tuple)):
            raise AssertionError
            for key in self._keys:
                if key.value_has_listener(self._key_value):
                    key.remove_value_listener(self._key_value)

            self._keys = []
            raise buttons != None and (len(buttons) == 32 or AssertionError)
            for button in buttons:
                raise isinstance(button, MonoButtonElement) or AssertionError
                self._keys.append(button)
                button.add_value_listener(self._key_value, True)

    def _key_value(self, value, sender):
        if self.is_enabled():
            self._active_client._send_c_key(self._keys.index(sender), int(value != 0))

    def _update_keys(self):
        for index in range(32):
            self._send_c_key(index, self._active_client._c_key[index])

    def _set_knobs(self, knobs):
        if not (knobs == None or isinstance(knobs, tuple)):
            raise AssertionError
            for knob in self._knobs:
                if knob.has_value_listener(self._knob_value):
                    knob.remove_value_listener(self._knob_value)

            self._knobs = []
            raise knobs != None and (len(knobs) == 24 or AssertionError)
            for knob in knobs:
                raise isinstance(knob, EncoderElement) or AssertionError
                self._knobs.append(knob)
                knob.add_value_listener(self._knob_value, True)

    def _knob_value(self, value, sender):
        if self.is_enabled():
            self._active_client._send_c_knob(self._knobs.index(sender), value)

    def _dial_matrix_value(self, value, x, y):
        if self.is_enabled() and self._active_client != None:
            if self._script._absolute_mode == 0:
                value = RELATIVE[int(value == 1)]
            self._active_client._send_c_dial(x, y, value)

    def _dial_button_matrix_value(self, value, x, y, force):
        if self.is_enabled() and self._active_client != None:
            self._active_client._send_c_dial_button(x, y, value)

    def _reset_encoder(self, coord):
        self._dial_matrix.get_dial(coord[0], coord[1])._reset_to_center()

    def _send_c_grid(self, column, row, value):
        if self.is_enabled() and self._grid != None:
            if column in range(self._x, self._x + 4):
                if row in range(self._y, self._y + 4):
                    self._grid.get_button(column - self._x, row - self._y).send_value(int(self._colors[value]))

    def _send_c_key(self, index, value):
        if self.is_enabled():
            if self._keys != None and len(self._keys) > index:
                self._keys[index].send_value(int(self._colors[value]))

    def _send_c_wheel(self, column, row, wheel, parameter = None):
        if self.is_enabled() and wheel != None:
            if column < 4 and row < 3:
                dial = self._dial_matrix.get_dial(column, row)
                if parameter == 'value':
                    dial._ring_value = int(wheel['value'])
                dial._ring_mode = int(wheel['mode'])
                dial._ring_green = int(wheel['green'] != 0)
                dial._ring_log = int(wheel['log'])
                if parameter == 'custom':
                    dial._ring_custom = dial._calculate_custom(str(wheel['custom']))
            self._dial_button_matrix.send_value(column, row, wheel['white'])
            if self._script._absolute_mode > 0 and not self._active_client._device_component.is_enabled():
                dial.send_value(wheel['log'], True)

    def _update_c_wheel(self):
        if self._dial_button_matrix != None:
            for column in range(4):
                for row in range(3):
                    self._send_c_wheel(column, row, self._active_client._c_wheel[column][row])
                    if not self._active_client._device_component.is_enabled():
                        self._send_to_lcd(column, row, self._active_client._c_wheel[column][row])

    def _update_wheel(self):
        self._update_c_wheel()

    def set_c_local_ring_control(self, val = 1):
        self._c_local_ring_control = val != 0
        self._script.set_local_ring_control(self._c_local_ring_control)

    def set_c_absolute_mode(self, val = 1):
        self._c_absolute_mode = val != 0
        self._script.set_absolute_mode(self._c_absolute_mode)

    def _release_mod_dials(self):
        if self._client is not None:
            for index in range(4):
                if not self._client[index]._mod_dial == None:
                    self._client[index]._mod_dial.release_parameter()

    def _assign_mod_dials(self):
        if self._client is not None:
            for index in range(4):
                param = self._client[index]._mod_dial_parameter()
                if not self._client[index]._mod_dial == None:
                    if not param == None:
                        self._client[index]._mod_dial.connect_to(param)
                    else:
                        self._client[index]._mod_dial.release_parameter()

            self._script.request_rebuild_midi_map()

    def _display_mod_colors(self):
        if self._client is not None:
            for index in range(4):
                self._script._shift_mode._modes_buttons[index].send_value(self._client[index]._mod_color)

            if self._is_enabled:
                self._script._shift_mode._modes_buttons[self._client.index(self._active_client)].send_value(8)
        else:
            for index in range(4):
                self._script._shift_mode._modes_buttons[index].send_value(0)

    def _send_nav_box(self):
        pass


class Cntrlr(ControlSurface):
    __module__ = __name__
    __doc__ = ' Monomodular controller script for Livid CNTRLR '

    def __init__(self, *a, **k):
        super(Cntrlr, self).__init__(*a, **k)
        self._version_check = 'b994'
        self._host_name = 'Cntrlr'
        self._color_type = 'OhmRGB'
        self._hosts = []
        self.hosts = []
        self._client = [ None for index in range(4) ]
        self._active_client = None
        self._rgb = 0
        self._timer = 0
        self._touched = 0
        self._local_ring_control = True
        self.set_local_ring_control(1)
        self._absolute_mode = 1
        self.flash_status = 1
        self._leds_last = None
        self._device_selection_follows_track_selection = FOLLOW
        with self.component_guard():
            self._setup_monobridge()
            self._setup_controls()
            self._setup_transport_control()
            self._setup_mixer_control()
            self._setup_session_control()
            self._assign_session_colors()
            self._setup_device_control()
            self._setup_device_selector()
            self._setup_mod()
            self._setup_switchboard()
            self._setup_chopper()
            self._setup_modes()
        self.schedule_message(1, self._open_log)
        self.song().view.add_selected_track_listener(self._update_selected_device)

    def _open_log(self):
        self.log_message('<<<<<<<<<<<<<<<<<<<<= ' + str(self._host_name) + ' ' + str(self._version_check) + ' log opened =>>>>>>>>>>>>>>>>>>>')
        self.show_message(str(self._host_name) + ' Control Surface Loaded')

    def _setup_monobridge(self):
        self._monobridge = MonoBridgeElement(self)
        self._monobridge.name = 'MonoBridge'

    def _setup_controls(self):
        is_momentary = True
        self._fader = [ None for index in range(8) ]
        self._dial_left = [ None for index in range(12) ]
        self._dial_right = [ None for index in range(12) ]
        self._encoder = [ None for index in range(12) ]
        self._encoder_button = [ None for index in range(12) ]
        self._grid = [ None for index in range(16) ]
        self._button = [ None for index in range(32) ]
        for index in range(8):
            self._fader[index] = MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, CNTRLR_FADERS[index], Live.MidiMap.MapMode.absolute, 'Fader_' + str(index), index, self)

        self._knobs = []
        for index in range(12):
            self._dial_left[index] = MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, CNTRLR_KNOBS_LEFT[index], Live.MidiMap.MapMode.absolute, 'Dial_Left_' + str(index), CNTRLR_KNOBS_LEFT[index], self)
            self._knobs.append(self._dial_left[index])

        for index in range(12):
            self._dial_right[index] = MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, CNTRLR_KNOBS_RIGHT[index], Live.MidiMap.MapMode.absolute, 'Dial_Right_' + str(index), CNTRLR_KNOBS_RIGHT[index], self)
            self._knobs.append(self._dial_right[index])

        for index in range(12):
            self._encoder[index] = CodecEncoderElement(MIDI_CC_TYPE, CHANNEL, CNTRLR_DIALS[index], Live.MidiMap.MapMode.absolute, 'Encoder_' + str(index), CNTRLR_DIALS[index], self)

        for index in range(12):
            self._encoder_button[index] = MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, CNTRLR_DIAL_BUTTONS[index], 'Encoder_Button_' + str(index), self)

        for index in range(16):
            self._grid[index] = MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, CNTRLR_GRID[index], 'Grid' + str(index), self)

        for index in range(32):
            self._button[index] = MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, CNTRLR_BUTTONS[index], 'Button_' + str(index), self)

        self._matrix = ButtonMatrixElement()
        self._matrix.name = 'Matrix'
        self._dial_matrix = EncoderMatrixElement(self)
        self._dial_matrix.name = 'Dial_Matrix'
        self._dial_button_matrix = ButtonMatrixElement()
        self._dial_button_matrix.name = 'Dial_Button_Matrix'
        for row in range(4):
            button_row = []
            for column in range(4):
                button_row.append(self._grid[row * 4 + column])

            self._matrix.add_row(tuple(button_row))

        for row in range(3):
            dial_row = []
            for column in range(4):
                dial_row.append(self._encoder[row * 4 + column])

            self._dial_matrix.add_row(tuple(dial_row))

        for row in range(3):
            dial_button_row = []
            for column in range(4):
                dial_button_row.append(self._encoder_button[row * 4 + column])

            self._dial_button_matrix.add_row(tuple(dial_button_row))

        self._key_matrix = ButtonMatrixElement()
        button_row = []
        for column in range(16):
            button_row.append(self._button[16 + column])

        self._key_matrix.add_row(tuple(button_row))

    def _setup_transport_control(self):
        self._transport = TransportComponent()
        self._transport.name = 'Transport'

    def _setup_mixer_control(self):
        is_momentary = True
        self._num_tracks = 4
        self._mixer = MixerComponent(4, 2, True, False)
        self._mixer.name = 'Mixer'
        self._mixer.set_track_offset(0)
        for index in range(4):
            self._mixer.channel_strip(index).set_volume_control(self._fader[index])
            self._mixer.channel_strip(index).name = 'Mixer_ChannelStrip_' + str(index)
            self._mixer.track_eq(index).name = 'Mixer_EQ_' + str(index)
            self._mixer.channel_strip(index)._invert_mute_feedback = True

        self.song().view.selected_track = self._mixer.channel_strip(0)._track
        self._send_reset = ResetSendsComponent(self)
        self._send_reset.name = 'Sends_Reset'

    def _setup_session_control(self):
        is_momentary = True
        num_tracks = 4
        num_scenes = 4
        self._session = SessionComponent(num_tracks, num_scenes)
        self._session.name = 'Session'
        self._session.set_offsets(0, 0)
        self._session.set_stop_track_clip_value(STOP_CLIP[self._rgb])
        self._scene = [ None for index in range(4) ]
        for row in range(num_scenes):
            self._scene[row] = self._session.scene(row)
            self._scene[row].name = 'Scene_' + str(row)
            for column in range(num_tracks):
                clip_slot = self._scene[row].clip_slot(column)
                clip_slot.name = str(column) + '_Clip_Slot' + str(row)
                clip_slot.set_triggered_to_play_value(CLIP_TRG_PLAY[self._rgb])
                clip_slot.set_triggered_to_record_value(CLIP_TRG_REC[self._rgb])
                clip_slot.set_stopped_value(CLIP_STOP[self._rgb])
                clip_slot.set_started_value(CLIP_STARTED[self._rgb])
                clip_slot.set_recording_value(CLIP_RECORDING[self._rgb])

        self.set_highlighting_session_component(self._session)
        self._session.set_mixer(self._mixer)
        self._session_zoom = SessionZoomingComponent(self._session)
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_stopped_value(ZOOM_STOPPED[self._rgb])
        self._session_zoom.set_playing_value(ZOOM_PLAYING[self._rgb])
        self._session_zoom.set_selected_value(ZOOM_SELECTED[self._rgb])
        self._session_zoom.set_button_matrix(self._matrix)
        self._session_zoom.set_zoom_button(self._button[31])

    def _assign_session_colors(self):
        num_tracks = 4
        num_scenes = 4
        self._session.set_stop_track_clip_value(STOP_ALL[self._rgb])
        for row in range(num_scenes):
            for column in range(num_tracks):
                self._scene[row].clip_slot(column).set_triggered_to_play_value(CLIP_TRG_PLAY[self._rgb])
                self._scene[row].clip_slot(column).set_triggered_to_record_value(CLIP_TRG_REC[self._rgb])
                self._scene[row].clip_slot(column).set_stopped_value(CLIP_STOP[self._rgb])
                self._scene[row].clip_slot(column).set_started_value(CLIP_STARTED[self._rgb])
                self._scene[row].clip_slot(column).set_recording_value(CLIP_RECORDING[self._rgb])

        self._session_zoom.set_stopped_value(ZOOM_STOPPED[self._rgb])
        self._session_zoom.set_playing_value(ZOOM_PLAYING[self._rgb])
        self._session_zoom.set_selected_value(ZOOM_SELECTED[self._rgb])
        self.refresh_state()

    def _setup_device_control(self):
        self._device = DeviceComponent()
        self._device.name = 'Device_Component'
        self._device._is_banking_enabled = self.device_is_banking_enabled(self._device)
        self._device.update = self._device_update(self._device)
        self._device.set_parameter_controls(tuple([ self._encoder[index + 4] for index in range(8) ]))
        self.set_device_component(self._device)
        self._device_navigator = CntrlrDetailViewControllerComponent(self)
        self._device_navigator.name = 'Device_Navigator'
        self._device_selection_follows_track_selection = FOLLOW

    def _setup_device_selector(self):
        self._device_selector = DeviceSelectorComponent(self)
        self._device_selector.name = 'Device_Selector'

    def _setup_mod(self):
        self._host = CntrlrMonomodComponent(self)
        self._host.name = 'Cntrlr_Host'
        self.hosts = [self._host]
        self._hosts = [self._host]
        self._host._set_parameter_controls(self._encoder)
        for index in range(4):
            self._client[index] = CntrlrMonoClient(self, index)
            self._client[index].name = 'Client_' + str(index)
            self._client[index]._mod_dial = self._encoder[index]
            self._client[index]._device_component = MonoDeviceComponent(self._client[index], MOD_BANK_DICT, MOD_TYPES)
            self._client[index]._control_defs = {'dials': self._dial_matrix,
             'buttons': self._dial_button_matrix,
             'grid': self._matrix,
             'keys': self._button,
             'knobs': self._knobs}

        self._active_client = self._client[0]
        self._active_client._is_active = True
        self._host.connect_to_clients(self)

    def _setup_switchboard(self):
        self._switchboard = SwitchboardElement(self, self._client)
        self._switchboard.name = 'Switchboard'

    def _setup_chopper(self):
        self._chopper = MonoChopperComponent(self, self._mixer)
        self._chopper.name = 'Chopper'
        self._chopper._set_button_matrix(self._key_matrix)

    def _setup_modes(self):
        self._shift_mode = ShiftModeComponent(self, self.shift_update)
        self._shift_mode.name = 'Mod_Mode'
        self._shift_mode.set_mode_buttons([ self._encoder_button[index] for index in range(4) ])

    def deassign_live_controls(self):
        self._leds_last = None
        for index in range(4):
            self._mixer.channel_strip(index).set_volume_control(None)

        for index in range(2):
            self._mixer.return_strip(index).set_volume_control(None)

        self._mixer.master_strip().set_volume_control(None)
        self._mixer.set_prehear_volume_control(None)
        for index in range(4):
            self._mixer.channel_strip(index).set_solo_button(None)
            self._mixer.channel_strip(index).set_arm_button(None)
            self._mixer.channel_strip(index).set_mute_button(None)
            self._mixer.channel_strip(index).set_select_button(None)

        for column in range(4):
            for row in range(4):
                self._scene[row].clip_slot(column).set_launch_button(None)

        self._send_reset.set_buttons(tuple([ None for index in range(4) ]))
        self._session.set_stop_track_clip_buttons(None)
        self._transport.set_play_button(None)
        self._transport.set_record_button(None)
        self._transport.set_stop_button(None)
        for index in range(16):
            self._grid[index].set_on_off_values(127, 0)
            self._grid[index].reset()

        for index in range(32):
            self._button[index].set_on_off_values(127, 0)
            self._button[index].reset()
            self._button[index].release_parameter()

        for client in self._client:
            client._mod_dial == None or client._mod_dial.release_parameter()

        self._device_navigator.set_device_nav_buttons(None, None)
        self._device_navigator.set_enabled(False)
        self._device.set_on_off_button(None)
        self._device.set_lock_button(None)
        self._device.set_bank_nav_buttons(None, None)
        self._device.set_enabled(False)
        self._session.set_enabled(False)
        self._session_zoom.set_enabled(False)
        for index in range(16):
            self._grid[index].clear_send_cache()

        for index in range(32):
            self._button[index].clear_send_cache()

        for index in range(12):
            self._device._parameter_controls = None
            self._encoder[index].release_parameter()
            self._encoder[index].send_value(0, True)
            self._encoder[index].clear_send_cache()

        for index in range(8):
            self._encoder_button[index + 4].send_value(0, True)
            self._encoder_button[index + 4].clear_send_cache()

        self._session_zoom.set_zoom_button(None)
        self._host._release_mod_dials()
        self.request_rebuild_midi_map()

    def assign_live_controls(self):
        """the following lines update all of the controls' last_sent properties, so that they forward the next value they receive regardless of whether or not it is the same as the last it recieved"""
        for index in range(16):
            self._grid[index].clear_send_cache()

        for index in range(32):
            self._button[index].clear_send_cache()

        for index in range(8):
            self._encoder_button[index + 4].send_value(0, True)
            self._encoder_button[index + 4].clear_send_cache()

        for index in range(8):
            self._encoder[index + 4].send_value(0, True)

        for index in range(12):
            self._encoder[index].clear_send_cache()

        self.schedule_message(4, self._assign_mod_dials)
        for index in range(4):
            self._button[index].set_on_value(SOLO[self._rgb])
            self._mixer.channel_strip(index).set_solo_button(self._button[index])
            self._button[index + 4].set_on_value(ARM[self._rgb])
            self._mixer.channel_strip(index).set_arm_button(self._button[index + 4])
            self._button[index + 16].set_on_value(MUTE[self._rgb])
            self._mixer.channel_strip(index).set_mute_button(self._button[index + 16])
            self._button[index + 20].set_on_value(SELECT[self._rgb])
            self._mixer.channel_strip(index).set_select_button(self._button[index + 20])

        self._send_reset.set_buttons(tuple((self._button[index + 8] for index in range(4))))
        self._session.set_stop_track_clip_buttons(tuple((self._button[index + 24] for index in range(4))))
        for index in range(4):
            self._button[index + 8].send_value(SEND_RESET[self._rgb], True)
            self._button[index + 24].set_on_off_values(STOP_CLIP[self._rgb], STOP_CLIP[self._rgb])
            self._button[index + 24].send_value(STOP_CLIP[self._rgb], True)

        self._button[28].set_on_off_values(PLAY_ON[self._rgb], PLAY[self._rgb])
        self._transport.set_play_button(self._button[28])
        self._button[30].set_on_off_values(RECORD_ON[self._rgb], RECORD[self._rgb])
        self._transport.set_record_button(self._button[30])
        self._button[29].set_on_value(STOP[self._rgb])
        self._transport.set_stop_button(self._button[29])
        self._button[29].send_value(STOP_OFF[self._rgb], True)
        for index in range(4):
            self._button[index + 12].set_on_off_values(SESSION_NAV[self._rgb], SESSION_NAV_OFF[self._rgb])

        self._session.set_track_bank_buttons(self._button[15], self._button[14])
        self._session.set_scene_bank_buttons(self._button[13], self._button[12])
        for column in range(4):
            for row in range(4):
                self._scene[row].clip_slot(column).set_launch_button(self._grid[row * 4 + column])

        for index in range(4):
            self._mixer.channel_strip(index).set_volume_control(self._fader[index])

        for index in range(2):
            self._mixer.return_strip(index).set_volume_control(self._fader[index + 4])

        self._mixer.master_strip().set_volume_control(self._fader[7])
        self._mixer.set_prehear_volume_control(self._fader[6])
        for track in range(4):
            channel_strip_send_controls = []
            for control in range(2):
                channel_strip_send_controls.append(self._dial_left[track + control * 4])

            self._mixer.channel_strip(track).set_send_controls(tuple(channel_strip_send_controls))
            self._mixer.channel_strip(track).set_pan_control(self._dial_left[track + 8])
            self._mixer.track_eq(track).set_gain_controls(tuple([self._dial_right[track + 8], self._dial_right[track + 4], self._dial_right[track]]))
            self._mixer.track_eq(track).set_enabled(True)

        self._device.set_parameter_controls(tuple([ self._encoder[index + 4] for index in range(8) ]))
        self._encoder_button[7].set_on_value(DEVICE_LOCK[self._rgb])
        self._device.set_lock_button(self._encoder_button[7])
        self._encoder_button[4].set_on_value(DEVICE_ON[self._rgb])
        self._device.set_on_off_button(self._encoder_button[4])
        for index in range(2):
            self._encoder_button[index + 8].set_on_value(DEVICE_NAV[self._rgb])
            self._encoder_button[index + 10].set_on_value(DEVICE_BANK[self._rgb])

        self._device_navigator.set_device_nav_buttons(self._encoder_button[10], self._encoder_button[11])
        self._device.set_bank_nav_buttons(self._encoder_button[8], self._encoder_button[9])
        self._session_zoom.set_zoom_button(self._button[31])
        self._device.set_enabled(True)
        self._device_navigator.set_enabled(True)
        self._session.set_enabled(True)
        self._session_zoom.set_enabled(True)
        self._device.update()
        self._session.update()

    def assign_chopper_controls(self):
        """the following lines update all of the controls' last_sent properties, so that they forward the next value they receive regardless of whether or not it is the same as the last it recieved"""
        for index in range(16):
            self._grid[index].clear_send_cache()

        for index in range(32):
            self._button[index].clear_send_cache()

        for index in range(8):
            self._encoder_button[index + 4].send_value(0, True)
            self._encoder_button[index + 4].clear_send_cache()

        for index in range(12):
            self._encoder[index].send_value(0, True)
            self._encoder[index].clear_send_cache()

        self.schedule_message(4, self._assign_mod_dials)
        for index in range(4):
            self._button[index].set_on_value(MUTE[self._rgb])
            self._mixer.channel_strip(index).set_mute_button(self._button[index])
            self._button[index + 4].set_on_value(SELECT[self._rgb])
            self._mixer.channel_strip(index).set_select_button(self._button[index + 4])

        self._session.set_stop_track_clip_buttons(tuple((self._button[index + 8] for index in range(4))))
        for index in range(4):
            self._button[index + 8].set_on_off_values(STOP_CLIP[self._rgb], STOP_CLIP[self._rgb])
            self._button[index + 8].send_value(STOP_CLIP[self._rgb], True)

        for index in range(4):
            self._button[index + 12].set_on_off_values(SESSION_NAV[self._rgb], SESSION_NAV_OFF[self._rgb])

        self._session.set_scene_bank_buttons(self._button[13], self._button[12])
        self._session.set_track_bank_buttons(self._button[15], self._button[14])
        for index in range(2):
            self._mixer.return_strip(index).set_volume_control(self._fader[index + 4])

        self._mixer.master_strip().set_volume_control(self._fader[7])
        self._mixer.set_prehear_volume_control(self._fader[6])
        for track in range(4):
            channel_strip_send_controls = []
            for control in range(2):
                channel_strip_send_controls.append(self._dial_left[track + control * 4])

            self._mixer.channel_strip(track).set_send_controls(tuple(channel_strip_send_controls))
            self._mixer.channel_strip(track).set_pan_control(self._dial_left[track + 8])
            gain_controls = []
            self._mixer.track_eq(track).set_gain_controls(tuple([self._dial_right[track + 8], self._dial_right[track + 4], self._dial_right[track]]))
            self._mixer.track_eq(track).set_enabled(True)

        for column in range(4):
            for row in range(4):
                self._scene[row].clip_slot(column).set_launch_button(self._grid[row * 4 + column])

        self._encoder_button[7].set_on_value(DEVICE_LOCK[self._rgb])
        self._device.set_lock_button(self._encoder_button[7])
        self._encoder_button[4].set_on_value(DEVICE_ON[self._rgb])
        self._device.set_on_off_button(self._encoder_button[4])
        for index in range(2):
            self._encoder_button[index + 8].set_on_value(DEVICE_NAV[self._rgb])
            self._encoder_button[index + 10].set_on_value(DEVICE_BANK[self._rgb])

        self._device_navigator.set_device_nav_buttons(self._encoder_button[10], self._encoder_button[11])
        self._device.set_bank_nav_buttons(self._encoder_button[8], self._encoder_button[9])
        self._device.set_enabled(True)
        self._device_navigator.set_enabled(True)
        self._session.set_enabled(True)
        self._session_zoom.set_enabled(True)
        self._device.update()
        self._session.update()
        self.request_rebuild_midi_map()

    def display_mod_colors(self):
        for index in range(4):
            self._shift_mode._modes_buttons[index].send_value(self._client[index]._mod_color)

    def shift_update(self):
        self.assign_alternate_mappings(0)
        self._chopper.set_enabled(False)
        for index in range(4):
            self._shift_mode._modes_buttons[index].send_value(self._client[index]._mod_color)

        if self._shift_mode._mode_index is 0:
            self._host._set_dial_matrix(None, None)
            self._host._set_button_matrix(None)
            self._host._set_key_buttons(None)
            self._host.set_enabled(False)
            self.set_local_ring_control(1)
            self.assign_live_controls()
        elif CHOPPER_ENABLE and not self._host._client[3].is_connected() and self._shift_mode._mode_index == 4:
            self.deassign_live_controls()
            for index in range(4):
                if self._shift_mode._mode_index == index + 1:
                    self._shift_mode._modes_buttons[index].send_value(1)

            self.schedule_message(4, self._assign_mod_dials)
            self._host._set_dial_matrix(None, None)
            self._host._set_button_matrix(None)
            self._host._set_key_buttons(None)
            self._host.set_enabled(False)
            self.set_local_ring_control(1)
            self.assign_chopper_controls()
            self._chopper.set_enabled(True)
        else:
            self.deassign_live_controls()
            self.assign_mixer_controls()
            self._host.set_enabled(True)
            self._host._set_dial_matrix(self._dial_matrix, self._dial_button_matrix)
            self._host._set_button_matrix(self._matrix)
            self._host._set_key_buttons(tuple(self._button))
            self._host._select_client(self._shift_mode._mode_index - 1)
            self._host.display_active_client()
            for index in range(4):
                if self._shift_mode._mode_index == index + 1:
                    self._shift_mode._modes_buttons[index].send_value(1)

            if not self._host._active_client.is_connected():
                self.assign_alternate_mappings(self._shift_mode._mode_index)

    def assign_mixer_controls(self):
        for index in range(4):
            self._mixer.channel_strip(index).set_volume_control(self._fader[index])

        for index in range(2):
            self._mixer.return_strip(index).set_volume_control(self._fader[index + 4])

        self._mixer.master_strip().set_volume_control(self._fader[7])
        self._mixer.set_prehear_volume_control(self._fader[6])

    def assign_alternate_mappings(self, chan):
        chan = min(16, max(chan, 0))
        for index in range(8):
            self._encoder_button[index + 4].set_channel(chan)
            self._encoder_button[index + 4].set_enabled(chan is 0)
            self._encoder_button[index + 4].force_next_send()

        for encoder in self._encoder:
            encoder.set_channel(chan)
            encoder.set_enabled(chan is 0)
            encoder.force_next_send()

        for button in self._button:
            button.set_channel(chan)
            button.set_enabled(chan is 0)
            button.force_next_send()

        for cell in self._grid:
            cell.set_channel(chan)
            cell.set_enabled(chan is 0)
            cell.force_next_send()

        self.request_rebuild_midi_map()

    def assign_original_mappings(self):
        for index in range(8):
            self._encoder_button[index + 4].set_channel(self._encoder_button[index + 4]._original_channel)
            self._encoder_button[index + 4].set_enabled(True)
            self._encoder_button[index + 4].force_next_send()

        for encoder in self._encoder:
            encoder.set_channel(encoder._original_channel)
            encoder.set_enabled(True)
            encoder.force_next_send()

        for button in self._button:
            button.set_channel(button._original_channel)
            button.set_enabled(True)
            button.force_next_send()

        for cell in self._grid:
            cell.set_channel(cell._original_channel)
            cell.set_enabled(True)
            cell.force_next_send()

        self.request_rebuild_midi_map()

    def update_display(self):
        super(Cntrlr, self).update_display()
        self._timer = (self._timer + 1) % 256
        if self._local_ring_control is False:
            self.send_ring_leds()
        self.flash()

    def flash(self):
        if self.flash_status > 0:
            for control in self.controls:
                if isinstance(control, MonoButtonElement):
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
        ret = ret.replace(' ', '_')
        raise len(ret) == NUM_CHARS_PER_DISPLAY_STRIP or AssertionError
        return ret

    def notification_to_bridge(self, name, value, sender):
        if isinstance(sender, (MonoEncoderElement, CodecEncoderElement)):
            pn = str(self.generate_strip_string(name))
            pv = str(self.generate_strip_string(value))
            self._monobridge._send(sender.name, 'lcd_name', pn)
            self._monobridge._send(sender.name, 'lcd_value', pv)

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

    def get_clip_names(self):
        clip_names = []
        for scene in self._session._scenes:
            for clip_slot in scene._clip_slots:
                if clip_slot.has_clip() is True:
                    clip_names.append(clip_slot._clip_slot)
                    return clip_slot._clip_slot

        return clip_names

    def handle_sysex(self, midi_bytes):
        pass

    def to_encoder(self, num, val):
        rv = int(val * 127)
        self._device._parameter_controls[num].receive_value(rv)
        p = self._device._parameter_controls[num]._parameter_to_map_to
        newval = val * (p.max - p.min) + p.min
        p.value = newval

    def set_local_ring_control(self, val = 1):
        self._local_ring_control = val != 0
        if self._local_ring_control is True:
            self._send_midi(tuple([240,
             0,
             1,
             97,
             8,
             32,
             0,
             247]))
        else:
            self._send_midi(tuple([240,
             0,
             1,
             97,
             8,
             32,
             1,
             247]))

    def set_absolute_mode(self, val = 1):
        self._absolute_mode = val != 0
        if self._absolute_mode is True:
            self._send_midi(tuple([240,
             0,
             1,
             97,
             8,
             17,
             0,
             0,
             0,
             0,
             0,
             0,
             0,
             0,
             247]))
        else:
            self._send_midi(tuple([240,
             0,
             1,
             97,
             8,
             17,
             127,
             127,
             127,
             127,
             127,
             127,
             127,
             127,
             247]))

    def send_ring_leds(self):
        if self._host._is_enabled == True:
            leds = [240,
             0,
             1,
             97,
             8,
             31]
            for index in range(12):
                wheel = self._encoder[index]
                bytes = wheel._get_ring()
                leds.append(bytes[0])
                leds.append(int(bytes[1]) + int(bytes[2]))

            leds.append(247)
            if not leds == self._leds_last:
                self._send_midi(tuple(leds))
                self._leds_last = leds

    def _release_mod_dials(self):
        if self._client is not None:
            for client in self._client:
                if not client._mod_dial == None:
                    client._mod_dial.release_parameter()

    def _assign_mod_dials(self):
        if self._client is not None:
            for client in self._client:
                param = client._mod_dial_parameter()
                if not client._mod_dial == None:
                    if not param == None:
                        client._mod_dial.connect_to(param)
                    else:
                        client._mod_dial.release_parameter()

            self.request_rebuild_midi_map()

    def disconnect(self):
        """clean things up on disconnect"""
        if self.song().view.selected_track_has_listener(self._update_selected_device):
            self.song().view.remove_selected_track_listener(self._update_selected_device)
        self._hosts = []
        self.log_message('<<<<<<<<<<<<<<<<<<<<<<<<< ' + str(self._host_name) + ' log closed >>>>>>>>>>>>>>>>>>>>>>>>>')
        super(Cntrlr, self).disconnect()

    def device_follows_track(self, val):
        self._device_selection_follows_track_selection = val == 1
        return self

    def _update_selected_device(self):
        if self._device_selection_follows_track_selection is True:
            track = self.song().view.selected_track
            device_to_select = track.view.selected_device
            if device_to_select == None and len(track.devices) > 0:
                device_to_select = track.devices[0]
            if device_to_select != None:
                self.song().view.select_device(device_to_select)
            self.set_appointed_device(device_to_select)
        self.request_rebuild_midi_map()

    def _get_num_tracks(self):
        return self.num_tracks

    def _device_update(self, device):

        def _update():
            DeviceComponent.update(device)
            self.request_rebuild_midi_map()

        return _update

    def _device_set_device(self, device_component):

        def set_device(device):
            is_monodevice = False
            for client in self._client:
                if device != None and client.device == device:
                    is_monodevice = client

            if is_monodevice != False:
                self.log_message('is monodevice' + str(device.name))
                if not (device == None or isinstance(device, Live.Device.Device)):
                    raise AssertionError
                    if not device_component._locked_to_device and device != device_component._device:
                        if device_component._device != None:
                            device_component._device.remove_name_listener(device_component._on_device_name_changed)
                            device_component._device.remove_parameters_listener(device_component._on_parameters_changed)
                            parameter = device_component._on_off_parameter()
                            if parameter != None:
                                parameter.remove_value_listener(device_component._on_on_off_changed)
                            if device_component._parameter_controls != None:
                                for control in device_component._parameter_controls:
                                    control.release_parameter()

                        device_component._device = device
                        if device_component._device != None:
                            device_component._bank_index = 0
                            device_component._device.add_name_listener(self._on_device_name_changed)
                            device_component._device.add_parameters_listener(self._on_parameters_changed)
                            parameter = device_component._on_off_parameter()
                            parameter != None and parameter.add_value_listener(device_component._on_on_off_changed)
                    for key in device_component._device_bank_registry.keys():
                        if key == device_component._device:
                            device_component._bank_index = device_component._device_bank_registry.get(key, 0)
                            del device_component._device_bank_registry[key]
                            break

                    device_component._bank_name = '<No Bank>'
                    device_component._bank_index = max(is_monodevice._cntrl_offset, device_component._bank_index)
                    device_component._on_device_name_changed()
                    device_component.update()
            else:
                DeviceComponent.set_device(device_component, device)

        return set_device

    def mixer_on_cf_assign_changed(self, channel_strip):

        def _on_cf_assign_changed():
            if channel_strip.is_enabled() and channel_strip._crossfade_toggle != None:
                if channel_strip._track != None and channel_strip._track in channel_strip.song().tracks + channel_strip.song().return_tracks:
                    if channel_strip._track.mixer_device.crossfade_assign == 1:
                        channel_strip._crossfade_toggle.turn_off()
                    elif channel_strip._track.mixer_device.crossfade_assign == 0:
                        channel_strip._crossfade_toggle.send_value(1)
                    else:
                        channel_strip._crossfade_toggle.send_value(2)

        return _on_cf_assign_changed

    def device_is_banking_enabled(self, device):

        def _is_banking_enabled():
            return True

        return _is_banking_enabled