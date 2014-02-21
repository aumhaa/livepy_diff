#Embedded file name: /Applications/Ableton Live 9 Beta.app/Contents/App-Resources/MIDI Remote Scripts/AumTroll_b995_9/AumTroll.py
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
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Mono_Framework.CodecEncoderElement import CodecEncoderElement
from _Mono_Framework.EncoderMatrixElement import EncoderMatrixElement
from _Mono_Framework.MonoChopperComponent import MonoChopperComponent
from _Mono_Framework.MonoBridgeElement import MonoBridgeElement
from _Mono_Framework.MonoButtonElement import MonoButtonElement
from _Mono_Framework.MonoEncoderElement import MonoEncoderElement
from _Mono_Framework.ResetSendsComponent import ResetSendsComponent
from _Mono_Framework.DeviceSelectorComponent import DeviceSelectorComponent
from _Mono_Framework.DetailViewControllerComponent import DetailViewControllerComponent
from _Mono_Framework.MonomodComponent import MonomodComponent
from _Mono_Framework.MonoDeviceComponent import MonoDeviceComponent
from _Mono_Framework.LiveUtils import *
from CNTRLR_9.Cntrlr import Cntrlr
from ModDevices import *
from Map import *
from _Tools.re import *
switchxfader = (240, 0, 1, 97, 2, 15, 1, 247)
switchxfaderrgb = (240, 0, 1, 97, 7, 15, 1, 247)
assigncolors = (240, 0, 1, 97, 7, 34, 0, 7, 3, 6, 5, 1, 2, 4, 247)
assign_default_colors = (240, 0, 1, 97, 7, 34, 0, 7, 6, 5, 1, 4, 3, 2, 247)
check_model = (240, 126, 127, 6, 1, 247)
request_snapshot = (240, 0, 1, 97, 8, 7, 6, 247)
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
ENDCODER_BANK_CONTROL = [['ModDevice_knob0',
  'ModDevice_knob1',
  'ModDevice_knob2',
  'ModDevice_knob3'], ['ModDevice_knob4',
  'ModDevice_knob5',
  'ModDevice_knob6',
  'ModDevice_knob7']]
ENDCODER_BANKS = {'NoDevice': [ ENDCODER_BANK_CONTROL[int(bank > 3)] + [ 'CustomParameter_' + str(index + bank * 24) for index in range(8) ] for bank in range(8) ]}
ALT_DEVICE_BANKS = {'EndCoders': ENDCODER_BANKS}
INITIAL_SCROLLING_DELAY = 5
INTERVAL_SCROLLING_DELAY = 1

class LoopPedalButtonElement(EncoderElement):

    def __init__(self, *a, **k):
        self._last = 0
        super(LoopPedalButtonElement, self).__init__(*a, **k)

    def receive_value(self, value):
        self._verify_value(value)
        value = int(value > 120) * 127
        self._last_sent_message = None
        if value != self._last:
            self.notify_value(value)
            self._last = value
            if self._report_input:
                is_input = True
                self._report_value(value, is_input)


class LoopPedalExpressionElement(EncoderElement):

    def __init__(self, script, *a, **k):
        self._last = 0
        self._script = script
        super(LoopPedalExpressionElement, self).__init__(*a, **k)

    def receive_value(self, value):
        self._verify_value(value)
        if value > self._last and value - self._last < 10 or value < self._last and self._last - value < 10:
            self.notify_value(value)
            self._last = value
            if self._report_input:
                is_input = True
                self._report_value(value, is_input)
        else:
            orig_value = value
            value += int(value - self._last > 0) * 5
            self.notify_value(value)
            self._script.schedule_message(1, self.update_value, [orig_value, value])
            self._last = value

    def update_value(self, values):
        if values[1] is self._last:
            self.receive_value(values[0])


class AumTrollDeviceSelectorComponent(DeviceSelectorComponent):

    def __init__(self, *a, **k):
        super(AumTrollDeviceSelectorComponent, self).__init__(*a, **k)
        self.song().add_appointed_device_listener(self._device_listener)

    def disconnect(self, *a, **k):
        super(AumTrollDeviceSelectorComponent, self).disconnect()
        if self.song().appointed_device_has_listener(self._device_listener):
            self.song().remove_appointed_device_listener(self._device_listener)

    def set_matrix(self, matrix):
        buttons = []
        if matrix is not None:
            for button, address in matrix.iterbuttons():
                button.use_default_message()
                button.set_enabled(True)
                buttons.append(button)

        self.set_mode_buttons(tuple(buttons))

    def set_mode_buttons(self, buttons):
        if buttons == None:
            buttons = []
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        for button in buttons:
            if button is not None:
                button.add_value_listener(self._mode_value, identify_sender=True)
                self._modes_buttons.append(button)
            self._number_of_modes = len(self._modes_buttons) + self._offset

        self.update()

    def update(self):
        if self.is_enabled():
            name = 'None'
            dev = self.song().appointed_device
            if hasattr(dev, 'name'):
                name = dev.name
                dev_type = dev.type
                dev_class = dev.class_name
            if self._modes_buttons:
                for index in range(len(self._modes_buttons)):
                    if match('p' + str(index + 1) + ' ', name) != None:
                        val = dev_class in DEVICE_COLORS and DEVICE_COLORS[dev_class] or dev_type in DEVICE_COLORS and DEVICE_COLORS[dev_type]
                        self._modes_buttons[index].send_value(val, True)
                    else:
                        self._modes_buttons[index].send_value(0, True)

    def _update_mode(self):
        mode = self._modes_heap[-1][0]
        if not mode in range(self.number_of_modes()):
            raise AssertionError
            if self._mode_index != mode:
                self._mode_index = mode
            if self.is_enabled():
                key = str('p' + str(self._mode_index + 1 + self._offset) + ' ')
                preset = None
                for track in self.song().tracks:
                    for device in self.enumerate_track_device(track):
                        if match(key, str(device.name)) != None:
                            preset = device
                            break

                for return_track in self.song().return_tracks:
                    for device in self.enumerate_track_device(return_track):
                        if match(key, str(device.name)) != None:
                            preset = device
                            break

                for device in self.enumerate_track_device(self.song().master_track):
                    if match(key, str(device.name)) != None:
                        preset = device
                        break

                preset != None and self._script.set_appointed_device(preset)
                self.song().view.select_device(preset)
            self.update()

    def set_mode(self, mode):
        self._clean_heap()
        self._modes_heap = [(mode, None, None)]
        self._update_mode()

    def _device_listener(self, *a, **k):
        if self.is_enabled():
            self.update()


class AumTrollMonoDevice(MonoDeviceComponent):

    def __init__(self, *a, **k):
        super(AumTrollMonoDevice, self).__init__(*a, **k)


class AumTrollMonomodComponent(MonomodComponent):

    def __init__(self, *a, **k):
        super(AumTrollMonomodComponent, self).__init__(*a, **k)
        self._alt_device_banks = MOD_TYPES
        self._host_name = 'AumTroll'

    def disconnect(self, *a, **k):
        self._release_mod_dials()
        super(AumTrollMonomodComponent, self).disconnect(*a, **k)

    def connect_to_clients(self, *a, **k):
        super(AumTrollMonomodComponent, self).connect_to_clients(*a, **k)
        for index in range(4):
            self._client[index]._mod_dial = self._script._encoder[index]

    def _select_client(self, *a, **k):
        super(AumTrollMonomodComponent, self)._select_client(*a, **k)
        self._script.set_local_ring_control(self._active_client._c_local_ring_control)
        self._script.set_absolute_mode(self._active_client._c_absolute_mode)
        if not self._active_client._device_component == None:
            self._active_client._device_component.update()

    def _matrix_value(self, value, x, y, is_momentary):
        if not self._grid != None:
            raise AssertionError
            raise value in range(128) or AssertionError
            raise isinstance(is_momentary, type(False)) or AssertionError
            self.is_enabled() and self._active_client._send_c_grid(x + self._x, y + self._y, value)

    def _send_grid(self, *a):
        pass

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

    def _update_grid(self):
        if self.is_enabled() and self._grid != None:
            for column in range(self._grid.width()):
                for row in range(self._grid.height()):
                    self._send_c_grid(column, row, self._active_client._c_grid[column][row])

    def _send_key(self, *a):
        pass

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

    def on_enabled_changed(self, *a, **k):
        super(AumTrollMonomodComponent, self).on_enabled_changed(*a, **k)
        if self._active_client != None:
            if self.is_enabled():
                if self._active_client._device_component is not None:
                    self._active_client._device_component.update()
                self._script.set_absolute_mode(self._active_client._c_absolute_mode)
                self._script.set_local_ring_control(self._active_client._c_local_ring_control)
            else:
                for control in self._parameter_controls:
                    control.release_parameter()

                self._script.set_absolute_mode(1)
                self._script.set_local_ring_control(1)

    def _dial_matrix_value(self, value, x, y):
        if self.is_enabled() and self._active_client != None:
            if self._script._absolute_mode == 0:
                value = RELATIVE[int(value == 1)]
            self._active_client._send_c_dial(x, y, value)

    def _reset_encoder(self, coord):
        self._dial_matrix.get_dial(coord[0], coord[1])._reset_to_center()

    def _dial_button_matrix_value(self, value, x, y, force):
        if self.is_enabled() and self._active_client != None:
            self._active_client._send_c_dial_button(x, y, value)

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


class ShiftModeComponent(ModeSelectorComponent):
    __module__ = __name__
    __doc__ = ' Special Class that selects mode 0 if a mode button thats active is pressed'

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


class AumTrollDetailViewController(DetailViewControllerComponent):

    def __init__(self, script, *a, **k):
        super(AumTrollDetailViewController, self).__init__(*a, **k)
        self._script = script

    def _nav_value(self, value, sender):
        super(AumTrollDetailViewController, self)._nav_value(value, sender)
        if self.is_enabled() and not self._shift_pressed:
            if not sender.is_momentary() or value != 0:
                modifier_pressed = True
                if not not self.application().view.is_view_visible('Detail'):
                    not self.application().view.is_view_visible('Detail/DeviceChain') or self._script._update_selected_device()


class AumTroll(Cntrlr):
    __module__ = __name__
    __doc__ = ' MonOhmod companion controller script '

    def __init__(self, *a, **k):
        self._monohm = None
        self._aumpush = None
        self._shifted = False
        self._use_pedal = True
        self._suppress_next_mod_display = False
        self._monomod_version = 'b995'
        self._codec_version = 'b995'
        super(AumTroll, self).__init__(*a, **k)
        self._client = None
        self._active_client = None
        self._host_name = 'AumTroll'
        with self.component_guard():
            self._setup_alt_device_control()
            self._setup_alt_mixer()
            self._setup_pedal()
            self._setup_device_selector()
        self._send_midi(tuple(request_snapshot))

    def _open_log(self):
        self.log_message('<<<<<<<<<<<<<<<<<<<<= ' + str(self._host_name) + ' ' + str(self._monomod_version) + ' log opened =>>>>>>>>>>>>>>>>>>>')
        self.show_message(str(self._host_name) + ' Control Surface Loaded')

    def _setup_mod(self):
        self._host = AumTrollMonomodComponent(self)
        self._host.name = 'Monomod_Host'
        self.hosts = [self._host]
        self._host._set_parameter_controls(self._encoder)

    def _setup_modes(self):
        self._shift_mode = ShiftModeComponent(self, self.shift_update)
        self._shift_mode.name = 'Mod_Mode'
        self._shift_mode.set_mode_buttons([ self._encoder_button[index] for index in range(4) ])
        self._monohm_shift = self._create_monohm_shift()
        self._last_client = None

    def _setup_switchboard(self):
        pass

    def _setup_device_selector(self):
        self._device_selector = AumTrollDeviceSelectorComponent(self)
        self._device_selector.name = 'Device_Selector'

    def deassign_live_controls(self):
        self._leds_last = None
        self._device_selector.set_enabled(False)
        self._device._parameter_controls = None
        self._deassign_monomodular_controls()
        self._device1._parameter_controls = None
        self._device2._parameter_controls = None
        for index in range(8):
            self._mixer2.channel_strip(index).set_select_button(None)
            self._mixer2.channel_strip(index).set_volume_control(None)

        for index in range(4):
            self._mixer3.channel_strip(index).set_select_button(None)
            self._mixer3.channel_strip(index).set_volume_control(None)
            self._mixer3.return_strip(index).set_volume_control(None)

        if self._aumpush:
            self._aumpush._host._set_bank_buttons(None)
        self._on_shift_button_value.subject = None
        self._mixer.set_crossfader_control(None)
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
        self._session.set_track_bank_buttons(None, None)
        self._session.set_scene_bank_buttons(None, None)
        self._transport.set_play_button(None)
        self._transport.set_record_button(None)
        self._transport.set_stop_button(None)
        for index in range(16):
            self._grid[index].set_on_off_values(127, 0)
            self._grid[index].reset()

        for index in range(32):
            self._button[index].set_on_off_values(127, 0)
            self._button[index].release_parameter()
            self._button[index].send_value(0, True)

        self._device_navigator.set_device_nav_buttons(None, None)
        self._device_navigator.set_enabled(False)
        self._device.set_on_off_button(None)
        self._device.set_lock_button(None)
        self._device.set_bank_nav_buttons(None, None)
        self._device.set_enabled(False)
        self._session.set_enabled(False)
        self._session_zoom.set_enabled(False)
        for index in range(16):
            self._grid[index].force_next_send()

        for index in range(32):
            self._button[index].force_next_send()

        for index in range(12):
            self._device._parameter_controls = None
            self._encoder[index].release_parameter()
            self._encoder[index].send_value(0, True)
            self._encoder[index].force_next_send()

        for index in range(8):
            self._encoder_button[index + 4].send_value(0, True)
            self._encoder_button[index + 4].force_next_send()

        for index in range(8):
            self._mixer2.channel_strip(index).set_select_button(None)
            self._mixer2.channel_strip(index).set_mute_button(None)
            self._mixer2.channel_strip(index).set_select_button(None)

        self._session_zoom.set_zoom_button(None)
        self.request_rebuild_midi_map()

    def assign_live_controls(self):
        """the following lines update all of the controls' last_sent properties, so that they forward the next value they receive regardless of whether or not it is the same as the last it recieved"""
        for index in range(16):
            self._grid[index].force_next_send()

        for index in range(32):
            self._button[index].force_next_send()

        for index in range(8):
            self._encoder_button[index + 4].send_value(0, True)
            self._encoder_button[index + 4].force_next_send()

        for index in range(12):
            self._encoder[index].send_value(0, True)
            self._encoder[index].force_next_send()

        self._host._assign_mod_dials()
        if self._monohm == None and self._aumpush == None:
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

            for index in range(2):
                self._mixer.return_strip(index).set_volume_control(self._fader[index + 4])

            self._mixer.master_strip().set_volume_control(self._fader[7])
            self._mixer.set_prehear_volume_control(self._fader[6])
            for track in range(4):
                channel_strip_send_controls = []
                for control in range(2):
                    channel_strip_send_controls.append(self._dial_left[track + control * 4])

                self._mixer.channel_strip(track).set_volume_control(self._fader[track])
                self._mixer.channel_strip(track).set_send_controls(tuple(channel_strip_send_controls))
                self._mixer.channel_strip(track).set_pan_control(self._dial_left[track + 8])
                self._mixer.track_eq(track).set_gain_controls(tuple([self._dial_right[track + 8], self._dial_right[track + 4], self._dial_right[track]]))
                self._mixer.track_eq(track).set_enabled(True)

            self._session_zoom.set_zoom_button(self._button[31])
            self._session.update()
            self._session.set_enabled(True)
            self._session_zoom.set_enabled(True)
        elif not self._aumpush == None:
            self.assign_aumpush_controls()
        elif not self._monohm == None:
            for index in range(8):
                self._mixer2.channel_strip(index).set_volume_control(self._fader[index])

            self._mixer2.set_track_offset(TROLL_OFFSET)
            self._device_selector.set_mode_buttons(tuple(self._grid))
            self._device_selector.set_enabled(True)
            if not self._shifted:
                self._assign_monomodular_controls()
            else:
                self._assign_shifted_controls()
            self._device1.set_parameter_controls(tuple([ self._knobs[index] for index in range(8) ]))
            self._device2.set_parameter_controls(tuple([ self._knobs[index + 12] for index in range(8) ]))
            self._device1.set_enabled(True)
            self._device2.set_enabled(True)
            self._find_devices()
            self._device1.update()
            self._device2.update()
        if self._aumpush == None:
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
            self._device.set_enabled(True)
            self._device_navigator.set_enabled(True)
            self._device.update()

    def assign_chopper_controls(self):
        """the following lines update all of the controls' last_sent properties, so that they forward the next value they receive regardless of whether or not it is the same as the last it recieved"""
        for index in range(16):
            self._grid[index].force_next_send()

        for index in range(32):
            self._button[index].force_next_send()

        for index in range(8):
            self._encoder_button[index + 4].send_value(0, True)
            self._encoder_button[index + 4].force_next_send()

        for index in range(12):
            self._encoder[index].send_value(0, True)
            self._encoder[index].force_next_send()

        self._host._assign_mod_dials()
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

    def shift_update(self):
        self.assign_alternate_mappings(0)
        self._chopper.set_enabled(False)
        if self._shift_mode._mode_index is 0:
            self._host._set_dial_matrix(None, None)
            self._host._set_button_matrix(None)
            self._host._set_key_buttons(None)
            self._host.set_enabled(False)
            self.deassign_live_controls()
            self.schedule_message(1, self.assign_live_controls)
            self.schedule_message(1, self._host._display_mod_colors)
        elif CHOPPER_ENABLE and self._host._client is not None and not self._host._client[3].is_connected() and self._shift_mode._mode_index == 4:
            self.deassign_live_controls()
            self._host._assign_mod_dials()
            self._host._set_dial_matrix(None, None)
            self._host._set_button_matrix(None)
            self._host._set_key_buttons(None)
            self._host.set_enabled(False)
            self.set_local_ring_control(1)
            self.assign_chopper_controls()
            self._chopper.set_enabled(True)
            self._host._display_mod_colors()
            self._shift_mode._modes_buttons[3].send_value(8)
        else:
            self.deassign_live_controls()
            if self._aumpush == None:
                for index in range(8):
                    self._mixer2.channel_strip(index).set_volume_control(self._fader[index])

                self._mixer2.set_track_offset(TROLL_OFFSET)
                self._device1.set_parameter_controls(tuple([ self._knobs[index] for index in range(8) ]))
                self._device2.set_parameter_controls(tuple([ self._knobs[index + 12] for index in range(8) ]))
                self._device1.set_enabled(True)
                self._device2.set_enabled(True)
                self._find_devices()
                self._device1.update()
                self._device2.update()
            else:
                self.assign_aumpush_controls()
            if self._host._client is None or not self._host._client[self._shift_mode._mode_index - 1].is_connected():
                self.assign_alternate_mappings(self._shift_mode._mode_index)
                for index in range(4):
                    self._shift_mode._modes_buttons[index].send_value(self._shift_mode._mode_index == index + 1)

            else:
                self._host._set_button_matrix(self._matrix)
                self._host._set_dial_matrix(self._dial_matrix, self._dial_button_matrix)
                if self._shifted is not True:
                    self._host._set_key_buttons(tuple(self._button))
                    if self._host._active_client._monomodular > 0:
                        if self._aumpush is None:
                            self._assign_monomodular_controls()
                else:
                    self._host._set_key_buttons(None)
                    self._assign_shifted_controls()
                self._host._select_client(self._shift_mode._mode_index - 1)
                if self._suppress_next_mod_display:
                    self._suppress_next_mod_display = False
                else:
                    self._host.display_active_client()
                self._host.set_enabled(True)
                self._host._display_mod_colors()

    def find_inputs(self):
        found_device = None
        tracks = self.song().tracks
        for track in tracks:
            if track.name == 'Inputs':
                for device in track.devices:
                    if bool(device.can_have_chains) and device.name == 'Inputs':
                        found_device = device

        return found_device

    def find_perc_crossfader(self):
        found_parameter = None
        tracks = self.song().tracks
        for track in tracks:
            if track.name == 'Perc':
                for device in track.devices:
                    if bool(device.can_have_chains) and device.name == 'Perc':
                        for parameter in device.parameters:
                            if parameter.name == 'XFade':
                                found_parameter = parameter

        return found_parameter

    def assign_aumpush_controls(self):
        if self._aumpush:
            inputs = self.find_inputs()
            if inputs is not None:
                for index in range(4):
                    self._knobs[index + 8].connect_to(inputs.parameters[index + 1])

            self._mixer.set_crossfader_control(self._knobs[23])
            xfade = self.find_perc_crossfader()
            if xfade is not None:
                self._knobs[20].connect_to(xfade)
            for index in range(4):
                self._mixer3.return_strip(index).set_volume_control(self._encoder[index + 4])
                self._encoder_button[index + 4].send_value(127, True)

            if self._shift_mode._mode_index is 0:
                self._on_shift_button_value.subject = self._grid[15]
                if self._aumpush._host._is_connected:
                    self._aumpush._host._set_bank_buttons(tuple(self._button[4:12] + self._button[20:28]))
                for index in range(4):
                    self._send_reset.set_buttons(tuple(self._encoder_button[4:8]))
                    self._button[index].set_on_off_values(SELECT[self._rgb], 1)
                    self._mixer.channel_strip(index).set_select_button(self._button[index])
                    self._mixer.channel_strip(index).set_mute_button(self._button[index + 16])
                    self._button[index + 12].set_on_off_values(SELECT[self._rgb], 1)
                    self._mixer2.channel_strip(index).set_select_button(self._button[index + 12])
                    self._mixer2.channel_strip(index).set_mute_button(self._button[index + 28])

                if not self._shifted:
                    self._mixer.selected_strip().set_send_controls(self._encoder[8:12])
                    for index in range(4):
                        self._encoder_button[index + 8].send_value(3, True)

                else:
                    self._mixer.return_strip(0).set_send_controls(tuple([None, self._encoder[8]]))
                    self._mixer.return_strip(1).set_send_controls(tuple([self._encoder[9], None]))
                    self._mixer3.channel_strip(0).set_volume_control(self._encoder[11])
                    self._encoder_button[8].send_value(5, True)
                    self._encoder_button[9].send_value(5, True)
                    self._encoder_button[11].send_value(1, True)
            for index in range(4):
                self._mixer.channel_strip(index).set_volume_control(self._fader[index])
                self._mixer2.channel_strip(index).set_volume_control(self._fader[index + 4])

            self._device1.set_parameter_controls(tuple([ self._knobs[index] for index in range(8) ]))
            self._device2.set_parameter_controls(tuple([ self._knobs[index + 12] for index in range(8) ]))
            self._device1.set_enabled(True)
            self._device2.set_enabled(True)
            self._find_devices()
            self._device1.update()
            self._device2.update()
            self._device_selector.set_mode_buttons(tuple(self._grid[:15]))
            self._device_selector.set_enabled(True)
            self._device_selector.update()
            self.request_rebuild_midi_map()

    def connect_script_instances(self, instanciated_scripts):
        if AUMPUSH_LINK is True:
            link = False
            for s in instanciated_scripts:
                if link == False:
                    if '_cntrlr_version' in dir(s):
                        if s._cntrlr_version == self._monomod_version and s._host_name == 'AumPush':
                            link = True
                            with self.component_guard():
                                self._connect_aumpush(s)
                            break

        elif MONOHM_LINK is True:
            link = False
            for s in instanciated_scripts:
                if link == False:
                    if '_cntrlr_version' in dir(s):
                        if s._cntrlr_version == self._monomod_version:
                            link = True
                            with self.component_guard():
                                self._connect_monohm(s)
                            break

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

            if not (is_monodevice != False and (device == None or isinstance(device, Live.Device.Device))):
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
                        if parameter != None:
                            parameter.add_value_listener(device_component._on_on_off_changed)
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

    def _connect_monohm(self, monohm):
        self.log_message('_connect_monohm')
        self._monohm = monohm
        self._monohm._cntrlr = self
        self._mixer2.set_track_offset(TROLL_OFFSET)
        self._monohm._shift_mode._mode_index = 3
        self._monohm._shift_mode.update()
        self._monohm._r_function_mode._mode_index = TROLL_RIGHT_MODE
        self._monohm._r_function_mode.update()
        self._monohm._shift_mode._mode_index = 0
        self._monohm._session_main.set_offsets(TROLL_MAIN_OFFSET, self._monohm._session_main._scene_offset)
        self._monohm.schedule_message(10, self._monohm._shift_mode.update)
        self._monohm_shift(0)

    def _connect_aumpush(self, aumpush):
        self.log_message('AumTroll connecting to AumPush...')
        self._aumpush = aumpush
        self._aumpush._cntrlr = self
        with self.component_guard():
            self.deassign_live_controls()
            self.schedule_message(3, self.assign_live_controls)

    def _make_device_selector_update(self, selector):

        def update():
            key = str('p' + str(selector._mode_index + 1) + ' ')
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
                self.set_appointed_device(preset)
                self.song().view.select_device(preset)
                selector._last_preset = selector._mode_index
                for button in selector._modes_buttons:
                    if selector._modes_buttons.index(button) == selector._mode_index:
                        button.turn_on()
                    else:
                        button.turn_off()

        return update

    def display_active_client(self):
        if self._device._device is not None:
            self.song().view.select_device(self._device._device)
            if not self.application().view.is_view_visible('Detail') or not self.application().view.is_view_visible('Detail/DeviceChain'):
                self.application().view.show_view('Detail')
                self.application().view.show_view('Detail/DeviceChain')

    def _setup_alt_device_control(self):
        self._device1 = DeviceComponent()
        self._device1.name = 'Device_Component1'
        self._device2 = DeviceComponent()
        self._device2.name = 'Device_Component2'

    def _find_devices(self):
        if self._device1:
            if len(self.song().return_tracks) > 0:
                if len(self.song().return_tracks[0].devices) > 0:
                    if self._device1._locked_to_device:
                        self._device1.set_lock_to_device(False, self._device1._device)
                    self._device1.set_lock_to_device(True, self.song().return_tracks[0].devices[0])
        if self._device2:
            if len(self.song().return_tracks) > 1:
                if len(self.song().return_tracks[1].devices) > 0:
                    if self._device2._locked_to_device:
                        self._device2.set_lock_to_device(False, self._device2._device)
                    self._device2.set_lock_to_device(True, self.song().return_tracks[1].devices[0])

    def _setup_alt_mixer(self):
        is_momentary = True
        self._num_tracks = 8
        self._mixer2 = MixerComponent(8, 0, False, False)
        self._mixer2.name = 'Mixer_2'
        self._mixer2.set_track_offset(4)
        for index in range(8):
            self._mixer2.channel_strip(index).name = 'Mixer_2_ChannelStrip_' + str(index)
            self._mixer2.channel_strip(index)._invert_mute_feedback = True

        self._mixer3 = MixerComponent(4, 4, False, False)
        self._mixer3.name = 'Mixer_3'
        self._mixer3.set_track_offset(8)
        for index in range(4):
            self._mixer3.channel_strip(index).name = 'Mixer_3_ChannelStrip_' + str(index)
            self._mixer3.channel_strip(index)._invert_mute_feedback = True

    def _setup_pedal(self):
        self._pedal = [ None for index in range(8) ]
        if self._use_pedal is True:
            for index in range(7):
                self._pedal[index] = LoopPedalButtonElement(MIDI_CC_TYPE, 0, 33 + index, Live.MidiMap.MapMode.absolute)
                self._pedal[index].name = 'Pedal_' + str(index)
                self._pedal[index]._report = False

            self._pedal[7] = LoopPedalExpressionElement(self, MIDI_CC_TYPE, 0, 40, Live.MidiMap.MapMode.absolute)
            self._pedal[7].name = 'Pedal_' + str(7)
            self._pedal[7]._report = False

    def _create_monohm_shift(self):

        def _monohm_shift(mode):
            self._shifted = mode > 1
            self._suppress_next_mod_display = True
            self.shift_update()

        return _monohm_shift

    def _assign_monomodular_controls(self):
        if self._monohm != None:
            self._monohm._host._set_key_buttons(tuple(self._button[4:12]))
            self._monohm._host._set_bank_buttons(tuple(self._button[16:32]))
            for index in range(4):
                self._button[index].set_on_off_values(SELECT[self._rgb], 1)
                self._mixer2.channel_strip(index).set_select_button(self._button[index])
                self._button[index + 12].set_on_off_values(SELECT[self._rgb], 1)
                self._mixer2.channel_strip(index + 4).set_select_button(self._button[index + 12])

    def _deassign_monomodular_controls(self):
        if self._monohm != None:
            self._monohm._host._set_key_buttons(None)
            self._monohm._host._set_bank_buttons(None)
            for index in range(8):
                self._mixer2.channel_strip(index).set_select_button(None)

    def _assign_shifted_controls(self):
        if self._monohm != None:
            self._monohm._host._set_key_buttons(tuple(self._button[4:12]))
            for index in range(4):
                self._button[index].set_on_off_values(SELECT[self._rgb], 1)
                self._mixer2.channel_strip(index).set_select_button(self._button[index])
                self._button[index + 12].set_on_off_values(SELECT[self._rgb], 1)
                self._mixer2.channel_strip(index + 4).set_select_button(self._button[index + 12])
                self._button[index + 16].set_on_off_values(MUTE[self._rgb], 0)
                self._mixer2.channel_strip(index).set_mute_button(self._button[index + 16])
                self._button[index + 28].set_on_off_values(MUTE[self._rgb], 0)
                self._mixer2.channel_strip(index + 4).set_mute_button(self._button[index + 28])

    def tick(self):
        self._chopper.get_pos()

    def _assign_mod_dials(self):
        pass

    @subject_slot('value')
    def _on_shift_button_value(self, value):
        shifted = value > 0
        if self._shifted is not shifted:
            self._shifted = shifted
            self.deassign_live_controls()
            self.assign_live_controls()
            if self._shifted and self._on_shift_button_value.subject:
                self._on_shift_button_value.subject.send_value(12, True)