#Embedded file name: /Applications/Ableton Live 9.05 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Codec_b995_9/Codec.py
from __future__ import with_statement
import Live
import time
import math
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.NotifyingControlElement import NotifyingControlElement
from _Framework.SessionComponent import SessionComponent
from _Framework.TransportComponent import TransportComponent
from _Generic.Devices import *
from _Mono_Framework.DetailViewControllerComponent import DetailViewControllerComponent
from _Mono_Framework.CodecEncoderElement import CodecEncoderElement
from _Mono_Framework.EncoderMatrixElement import EncoderMatrixElement
from _Mono_Framework.MonoBridgeElement import MonoBridgeElement
from _Mono_Framework.MonoButtonElement import MonoButtonElement
from _Mono_Framework.MonoEncoderElement import MonoEncoderElement
from _Mono_Framework.MonomodComponent import MonomodComponent
from _Mono_Framework.Live8DeviceComponent import Live8DeviceComponent as DeviceComponent
from _Mono_Framework.LiveUtils import *
from CodecDeviceSelectorComponent import CodecDeviceSelectorComponent
from CodecResetSendsComponent import CodecResetSendsComponent
from CodecDeviceComponent import CodecDeviceComponent
from SpecialCodecDeviceComponent import SpecialCodecDeviceComponent
from Map import *

def tracks_to_use(self):
    return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)


MixerComponent.tracks_to_use = tracks_to_use
factoryreset = (240,
 0,
 1,
 97,
 4,
 6,
 247)
btn_channels = (240,
 0,
 1,
 97,
 4,
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
 4,
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
SLOWENCODER = (240,
 0,
 1,
 97,
 4,
 30,
 0,
 0,
 247)
NORMALENCODER = (240,
 0,
 1,
 97,
 4,
 30,
 2,
 0,
 247)
FASTENCODER = (240,
 0,
 1,
 97,
 4,
 30,
 4,
 0,
 247)

class CodecMonoButtonElement(MonoButtonElement):

    def __init__(self, *a, **k):
        super(CodecMonoButtonElement, self).__init__(*a, **k)
        self.set_color_map(tuple(COLOR_MAP))


class CodecMonomodComponent(MonomodComponent):

    def __init__(self, *a, **k):
        super(CodecMonomodComponent, self).__init__(*a, **k)
        self._host_name = 'Code'

    def select_client(self, number, *a, **k):
        self._script.set_local_ring_control(self._active_client._local_ring_control)
        self._script.set_absolute_mode(self._active_client._absolute_mode)
        super(CodecMonomodComponent, self)._select_client(number, *a, **k)

    def _matrix_value(self, value, x, y, is_momentary):
        raise self._grid != None or AssertionError
        raise value in range(128) or AssertionError
        raise isinstance(is_momentary, type(False)) or AssertionError
        if self.is_enabled():
            if self._shift_pressed == 1:
                if value > 0:
                    if y == 0:
                        self._select_client(x + self._bank_add * 8)
                        self._display_bank()
                    elif y == 1:
                        self._active_client._set_channel(x + self._chan_add * 8)
                        self._display_channel()
                    elif x == 0 and y == 2:
                        self._bank_add = abs(self._bank_add - 1)
                        self._display_bank()
                    elif x == 7 and y == 2:
                        self._chan_add = abs(self._chan_add - 1)
                        self._display_channel()
                    elif x in range(2, 4) and y in range(2, 4):
                        self._change_offset(0, 0)
                    elif x in range(4, 6) and y in range(2, 4):
                        self._change_offset(8, 0)
                    elif x in range(2, 4) and y in range(4, 6):
                        self._change_offset(0, 8)
                    elif x in range(4, 6) and y in range(4, 6):
                        self._change_offset(8, 8)
                    elif y == 7:
                        if self._alt_pressed > 0:
                            if x == 7:
                                self.select_active_client()
                        else:
                            self._active_client._send_key(x, value)
            elif self._shift_pressed == 0:
                if self._locked == 1:
                    if y == 7:
                        if self._alt_pressed > 0:
                            if x == 7:
                                self.select_active_client()
                            else:
                                self._active_client._send_key(x, value)
                        else:
                            self._active_client._send_key(x, value)
                    else:
                        self._active_client._send_grid(x + self._x, y + self._y, value)
                else:
                    self._active_client._send_grid(x + self._x, y + self._y, value)

    def _alt_value(self, value):
        if self._shift_pressed == 0:
            self._alt_pressed = value != 0
            self._active_client._send('alt', int(self._alt_pressed))
            self.update()

    def _key_value(self, value, sender):
        if self.is_enabled():
            self._active_client._send_key(self._keys.index(sender), int(value != 0))

    def _send_key(self, index, value):
        if self.is_enabled():
            if self._shift_pressed > 0 or self._locked > 0:
                if self._grid != None:
                    self._grid.get_button(index, 7).send_value(int(self._colors[value]))
                if self._dial_button_matrix != None:
                    for index in range(8):
                        self._dial_button_matrix.get_button(index, 4).send_value(int(self._colors[self._active_client._key[index]]))

            if self._keys != None and len(self._keys) > index:
                self._keys[index].send_value(int(self._colors[value]))

    def on_enabled_changed(self):
        super(CodecMonomodComponent, self).on_enabled_changed()
        if self._active_client != None:
            if self.is_enabled():
                self._active_client._device_component.update()
                self._script.set_absolute_mode(self._active_client._absolute_mode)
                self._script.set_local_ring_control(self._active_client._local_ring_control)
            else:
                for control in self._parameter_controls:
                    control.release_parameter()

                self._script.set_absolute_mode(1)
                self._script.set_local_ring_control(1)

    def _dial_matrix_value(self, value, x, y):
        if self.is_enabled() and self._active_client != None:
            if self._script._absolute_mode == 0:
                value = RELATIVE[int(value == 1)]
            self._active_client._send_dial(x, y, value)

    def _reset_encoder(self, coord):
        self._dial_matrix.get_dial(coord[0], coord[1])._reset_to_center()

    def _dial_button_matrix_value(self, value, x, y, force):
        if self.is_enabled() and self._shift_pressed is False and self._active_client != None:
            if self._locked == 1 and y == 4:
                self._active_client._send_key(x, value)
                self._update_keys()
            else:
                self._active_client._send_dial_button(x, y, value)
        elif self.is_enabled() and self._shift_pressed is True:
            if y == 0 and value > 0:
                if x < 8:
                    self._select_client(x + self._bank_add * 8)
                    self._display_bank()
                else:
                    self._locked = abs(self._locked - 1)
                    self.update()
            elif y == 1:
                if y < 8 and value > 0:
                    self._active_client._set_channel(x + self._chan_add * 8)
                    self._display_channel()
                else:
                    self._alt_pressed = int(value != 0)
                    self._active_client._send('alt', int(self._alt_pressed))
                    self.update()
            elif y == 2:
                if x == 0 and value > 0:
                    self._bank_add = abs(self._bank_add - 1)
                    self._display_bank()
                elif x == 7 and value > 0:
                    self._chan_add = abs(self._chan_add - 1)
                    self._display_channel()
            elif y == 4:
                if self._alt_pressed > 0 and x == 7 and val > 0:
                    self.select_active_client()
                else:
                    self._active_client._send_key(x, value)
                    self._update_keys()

    def _send_wheel(self, column, row, wheel, parameter = None):
        if self.is_enabled() and wheel != None:
            if column < 8 and row < 4:
                dial = self._dial_matrix.get_dial(column, row)
                if parameter == 'value':
                    dial._ring_value = int(wheel['value'])
                dial._ring_mode = int(wheel['mode'])
                dial._ring_green = int(wheel['green'] != 0)
                if parameter == 'custom':
                    dial._ring_custom = dial._calculate_custom(str(wheel['custom']))
            if self._shift_pressed == True:
                if row in range(2, 3) and column in range(0, 7):
                    self._dial_button_matrix.send_value(column, row, wheel['white'])
            elif self._locked == True:
                if row in range(0, 3):
                    self._dial_button_matrix.send_value(column, row, wheel['white'])
            else:
                self._dial_button_matrix.send_value(column, row, wheel['white'])

    def _update_wheel(self):
        if self._dial_button_matrix != None:
            if self._shift_pressed is False:
                for column in range(9):
                    for row in range(5):
                        self._send_wheel(column, row, self._active_client._wheel[column][row])

    def set_local_ring_control(self, val = 1):
        self._local_ring_control = val != 0
        self._script.set_local_ring_control(self._local_ring_control)

    def set_absolute_mode(self, val = 1):
        self._absolute_mode = val != 0
        self._script.set_absolute_mode(self._absolute_mode)

    def set_appointed_device(self, *a, **k):
        pass


class MonomodModeComponent(ModeSelectorComponent):

    def __init__(self, callback, script, *a, **k):
        super(MonomodModeComponent, self).__init__(*a, **k)
        raise hasattr(callback, '__call__') or AssertionError
        self._set_protected_mode_index(0)
        self._script = script
        self.update = callback

    def number_of_modes(self):
        return 2

    def set_mode_toggle(self, button):
        if not (button == None or isinstance(button, ButtonElement)):
            raise AssertionError
            if self._mode_toggle != None:
                self._mode_toggle.remove_value_listener(self._toggle_value)
            self._mode_toggle = button
            self._mode_toggle != None and self._mode_toggle.add_value_listener(self._toggle_value)

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


class ShiftModeComponent(ModeSelectorComponent):

    def __init__(self, callback, script, *a, **k):
        super(ShiftModeComponent, self).__init__(*a, **k)
        raise hasattr(callback, '__call__') or AssertionError
        self._set_protected_mode_index(0)
        self._script = script
        self.update = callback

    def number_of_modes(self):
        return 4

    def set_mode_toggle(self, button):
        if not (button == None or isinstance(button, ButtonElement)):
            raise AssertionError
            if self._mode_toggle != None:
                self._mode_toggle.remove_value_listener(self._toggle_value)
            self._mode_toggle = button
            self._mode_toggle != None and self._mode_toggle.add_value_listener(self._toggle_value)

    def set_mode_buttons(self, buttons):
        raise buttons != None or AssertionError
        raise isinstance(buttons, tuple) or AssertionError
        raise len(buttons) - 1 in range(16) or AssertionError
        for button in buttons:
            raise isinstance(button, ButtonElement) or AssertionError
            identify_sender = True
            button.add_value_listener(self._mode_value, identify_sender)
            self._modes_buttons.append(button)


class Codec(ControlSurface):
    __module__ = __name__
    __doc__ = ' MonoCode controller script '

    def __init__(self, c_instance, *a, **k):
        super(Codec, self).__init__(c_instance, *a, **k)
        self._monomod_version = 'b995'
        self._version_check = 'b995'
        self._host_name = 'Codec'
        self._color_type = 'Monochrome'
        self._link_mixer = LINK_MIXER
        self._hosts = []
        self._linked_script = None
        self._local_ring_control = True
        self._last_device = None
        self._device_list = [None,
         None,
         None,
         None]
        self._device_select_buttons = None
        self._last_device_component = None
        self._timer = 0
        self._touched = 0
        self._locked = False
        self.flash_status = 1
        self._shift_button = None
        self._shift_pressed = 0
        self._shift_pressed_timer = 0
        self._shift_thresh = SHIFT_THRESH
        self._use_device_selector = USE_DEVICE_SELECTOR
        self._device_selection_follows_track_selection = FOLLOW
        with self.component_guard():
            self._setup_controls()
            self._setup_monobridge()
            self._setup_device_controls()
            self._setup_special_device_control()
            self._device.append(self._special_device)
            self._setup_device_chooser()
            self._setup_mixer_controls()
            self._setup_monomod()
            self._setup_modes()
            self._setup_device_selector()
            self._setup_send_reset()
            self._setup_default_buttons()
            self.set_local_ring_control(1)
            self.song().view.add_selected_track_listener(self._update_selected_device)
            self._initialize_code()
        self.log_message('<<<<<<<<<<<<<<<<<<<<<<<<< Codec ' + str(self._monomod_version) + ' log opened >>>>>>>>>>>>>>>>>>>>>>>>>')
        self.show_message('Codec Control Surface Loaded')
        self.request_rebuild_midi_map()

    def _initialize_code(self):
        self._send_midi(factoryreset)
        self._send_midi(btn_channels)
        self._send_midi(enc_channels)

    def _setup_monobridge(self):
        self._monobridge = MonoBridgeElement(self)
        self._monobridge.name = 'MonoBridge'

    def _setup_controls(self):
        is_momentary = True
        self._livid = CodecMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, LIVID, 'Livid_Button', self)
        self._dial = [ None for index in range(8) ]
        for column in range(8):
            self._dial[column] = [ None for index in range(4) ]
            for row in range(4):
                self._dial[column][row] = CodecEncoderElement(MIDI_CC_TYPE, CHANNEL, CODE_DIALS[row][column], Live.MidiMap.MapMode.absolute, 'Dial_' + str(column) + '_' + str(row), column + row * 8, self)

        self._button = [ None for index in range(8) ]
        for column in range(8):
            self._button[column] = [ None for index in range(4) ]
            for row in range(4):
                self._button[column][row] = CodecMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, CODE_BUTTONS[row][column], 'Button_' + str(column) + '_' + str(row), self)

        self._column_button = [ None for index in range(8) ]
        for index in range(8):
            self._column_button[index] = CodecMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, CODE_COLUMN_BUTTONS[index], 'Column_Button_' + str(index), self)

        self._row_button = [ None for index in range(4) ]
        for index in range(4):
            self._row_button[index] = CodecMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, CODE_ROW_BUTTONS[index], 'Row_Button_' + str(index), self)

        self._dial_matrix = EncoderMatrixElement(self)
        self._dial_matrix.name = 'Encoder_Matrix'
        for row in range(4):
            dial_row = tuple([ self._dial[column][row] for column in range(8) ])
            self._dial_matrix.add_row(dial_row)

        self._button_matrix = ButtonMatrixElement()
        self._button_matrix.name = 'Button_Matrix'
        for row in range(4):
            button_row = [ self._button[column][row] for column in range(8) ]
            button_row.append(self._row_button[row])
            self._button_matrix.add_row(tuple(button_row))

        self._button_matrix.add_row(tuple(self._column_button + [self._livid]))

    def _setup_modes(self):
        self._monomod_mode = MonomodModeComponent(self._mod_mode_update, self)
        self._monomod_mode.name = 'Monomod_Mode'
        self.set_shift_button(self._livid)
        self._shift_mode = ShiftModeComponent(self._shift_update, self)
        self._shift_mode.name = 'Shift_Mode'
        self._shift_mode.set_mode_buttons(tuple([self._row_button[0],
         self._row_button[1],
         self._row_button[2],
         self._row_button[3]]))

    def _setup_transport_control(self):
        self._transport = TransportComponent()
        self._transport.name = 'Transport'

    def _setup_monomod(self):
        self._host = CodecMonomodComponent(self)
        self._host.name = 'Monomod_Host'
        self._host._set_dial_matrix(self._dial_matrix, self._button_matrix)
        self.hosts = [self._host]
        encs = []
        for row in range(4):
            for col in range(8):
                encs.append(self._dial[col][row])

        self._host._set_parameter_controls(encs)

    def _setup_mixer_controls(self):
        is_momentary = True
        self._num_tracks = 8
        self._session = SessionComponent(self._num_tracks, 0)
        self._session.name = 'Session'
        self._mixer = MixerComponent(self._num_tracks, 0, False, False)
        self._mixer.name = 'Mixer'
        self._mixer._next_track_value = self._mixer_next_track_value(self._mixer)
        self._mixer._prev_track_value = self._mixer_prev_track_value(self._mixer)
        self._mixer.set_track_offset(0)
        for index in range(8):
            self._mixer.channel_strip(index).name = 'Mixer_ChannelStrip_' + str(index)
            self._mixer.channel_strip(index)._invert_mute_feedback = True
            self._mixer.channel_strip(index)._mute_value = self._channelstrip_mute_value(self._mixer.channel_strip(index))
            self._mixer.channel_strip(index)._solo_value = self._channelstrip_solo_value(self._mixer.channel_strip(index))

        self.song().view.selected_track = self._mixer.channel_strip(0)._track
        self._session.set_mixer(self._mixer)

    def _setup_device_controls(self):
        self._device = [ None for index in range(4) ]
        for index in range(4):
            self._device[index] = CodecDeviceComponent(self)
            self._device[index].name = 'CodecDevice_Component_' + str(index)
            device_param_controls = []
            for control in range(8):
                device_param_controls.append(self._dial[control][index])

            self._device[index].set_on_off_button(self._button[1][index])
            self._device[index].set_lock_button(self._button[2][index])
            self._device[index].set_bank_nav_buttons(self._button[4][index], self._button[5][index])
            self._device[index].set_nav_buttons(self._button[6][index], self._button[7][index])
            self._device[index].set_parameter_controls(tuple(device_param_controls))

        self.set_device_component(self._device[0])
        self._last_device_component = self._device[0]

    def _setup_special_device_control(self):
        self._special_device = SpecialCodecDeviceComponent(self)
        self._special_device.name = 'SpecialCodecDeviceComponent'
        self._special_device.set_on_off_button(self._button[1][0])
        self._special_device.set_lock_button(self._button[2][0])
        self._special_device.set_bank_nav_buttons(self._button[4][0], self._button[5][0])
        self._special_device.set_nav_buttons(self._button[6][0], self._button[7][0])
        device_param_controls = []
        for row in range(4):
            for column in range(8):
                device_param_controls.append(self._dial[column][row])

        self._special_device.set_parameter_controls(tuple(device_param_controls))

    def _setup_device_chooser(self):
        self._selected_device = self._device[0]
        self._last_selected_device = self._device[0]
        self._device_select_buttons = [ self._button[0][index] for index in range(4) ]
        for button in self._device_select_buttons:
            button.add_value_listener(self._device_select_value, True)

    def _setup_device_selector(self):
        self._device_selector = CodecDeviceSelectorComponent(self, 'c', self._device + [self._special_device])
        self._device_selector.name = 'Device_Selector'
        self._device_selector.set_mode_buttons(self._column_button)

    def _setup_send_reset(self):
        self._send_reset = CodecResetSendsComponent(self)
        self._send_reset.set_buttons(self._button)

    def _setup_default_buttons(self):
        self._value_default = ParameterDefaultComponent(self)
        buttons = []
        dials = []
        for column in self._button:
            for button in column:
                buttons.append(button)

        for column in self._dial:
            for dial in column:
                dials.append(dial)

        self._value_default.set_buttons(buttons)
        self._value_default.set_dials(dials)

    def _device_select_value(self, value, sender):
        if not self._shift_pressed:
            if sender.is_momentary or value > 0:
                if self._shift_mode._mode_index == 2:
                    self.set_device_component(self._device[self._device_select_buttons.index(sender)])
                    self._last_device_component = self._device_component
                    if self._device_component != None and isinstance(self._device_component._device, Live.Device.Device):
                        if self._device_component.find_track(self._device_component._device) == self.song().view.selected_track:
                            self._device_component.display_device()

    def set_shift_button(self, button):
        if not (button == None or isinstance(button, MonoButtonElement)):
            raise AssertionError
            if self._shift_button != None:
                self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = button
            self._shift_button != None and self._shift_button.add_value_listener(self._shift_value)

    def _shift_value(self, value):
        self._shift_pressed = int(value != 0)
        if self._shift_pressed > 0:
            self._send_midi(SLOWENCODER)
            if self._shift_pressed_timer + self._shift_thresh > self._timer:
                self.log_message('mod mode: ' + str(abs(self._monomod_mode._mode_index - 1)))
                self._monomod_mode.set_mode(max(0, min(1, abs(self._monomod_mode._mode_index - 1))))
            self._shift_pressed_timer = self._timer % 256
        else:
            self._send_midi(NORMALENCODER)

    def _mod_mode_update(self):
        if self._monomod_mode._mode_index == 0:
            self._host._set_shift_button(None)
            self._host.set_enabled(False)
            self._dial_matrix.reset()
            self._shift_mode.set_enabled(True)
            self._shift_update()
            self.request_rebuild_midi_map()
            self._livid.turn_off()
        elif self._monomod_mode._mode_index == 1:
            self._shift_mode.set_enabled(False)
            self._deassign_all()
            self._dial_matrix.reset()
            self._button_matrix.reset()
            self._livid.turn_on()
            if not self._host._active_client == None:
                self._host.set_enabled(True)
                self._host._set_shift_button(self._livid)
            else:
                self._assign_alternate_mappings(1)
            self.request_rebuild_midi_map()

    def _shift_update(self):
        if self._shift_mode.is_enabled():
            with self.component_guard():
                self.allow_updates(False)
                self._deassign_all()
                if self._shift_mode._mode_index is 0:
                    self._assign_volume()
                elif self._shift_mode._mode_index is 1:
                    self._assign_sends()
                elif self._shift_mode._mode_index is 2:
                    self._assign_devices()
                elif self._shift_mode._mode_index is 3:
                    self._assign_special_device()
                for index in range(self._shift_mode.number_of_modes()):
                    if index == self._shift_mode._mode_index:
                        self._shift_mode._modes_buttons[index].turn_on()
                    else:
                        self._shift_mode._modes_buttons[index].turn_off()

                self.allow_updates(True)
                self.request_rebuild_midi_map()

    def _deassign_all(self):
        self._assign_alternate_mappings(0)
        self._device_selector.set_enabled(False)
        for index in range(8):
            self._mixer.channel_strip(index).set_volume_control(None)
            self._mixer.channel_strip(index).set_pan_control(None)
            self._mixer.channel_strip(index).set_send_controls(tuple([None,
             None,
             None,
             None]))

        for index in range(4):
            self._device[index].set_enabled(False)
            self._device[index]._parameter_controls = None

        self._special_device.set_enabled(False)
        self._special_device._parameter_controls = None
        self._device_selector.set_enabled(False)
        self._deassign_buttons()
        for control in self.controls:
            control.reset()

        self.request_rebuild_midi_map()

    def _deassign_buttons(self):
        for index in range(8):
            self._mixer.channel_strip(index).set_select_button(None)
            self._mixer.channel_strip(index).set_solo_button(None)
            self._mixer.channel_strip(index).set_mute_button(None)

        self._mixer.set_select_buttons(None, None)
        self._send_reset.set_enabled(False)

    def _assign_volume(self):
        for index in range(8):
            self._mixer.channel_strip(index).set_volume_control(self._dial[index][3])
            self._mixer.channel_strip(index).set_pan_control(self._dial[index][2])
            self._mixer.channel_strip(index).set_send_controls(tuple([self._dial[index][0], self._dial[index][1]]))
            self._mixer.channel_strip(index).set_select_button(self._column_button[index])
            self._mixer.channel_strip(index).set_solo_button(self._button[index][2])
            self._mixer.channel_strip(index).set_mute_button(self._button[index][3])

        self._mixer.set_select_buttons(self._button[7][0], self._button[6][0])

    def _assign_sends(self):
        for index in range(8):
            self._mixer.channel_strip(index).set_send_controls(tuple([self._dial[index][0],
             self._dial[index][1],
             self._dial[index][2],
             self._dial[index][3]]))
            self._mixer.channel_strip(index).set_select_button(self._column_button[index])
            self._send_reset.set_enabled(True)

    def _assign_devices(self):
        self.set_device_component(self._last_device_component)
        self._device_select_value(1, self._device_select_buttons[self._device.index(self._device_component)])
        for index in range(4):
            device_param_controls = []
            for control in range(8):
                device_param_controls.append(self._dial[control][index])

            self._device[index].set_parameter_controls(tuple(device_param_controls))
            self._device[index].set_enabled(True)

        self._device_selector.set_enabled(self._use_device_selector)
        if not self._use_device_selector:
            for index in range(8):
                self._mixer.channel_strip(index).set_select_button(self._column_button[index])

    def _assign_special_device(self):
        self.set_device_component(self._special_device)
        device_param_controls = []
        for row in range(4):
            for column in range(8):
                device_param_controls.append(self._dial[column][row])

        self._special_device.set_parameter_controls(tuple(device_param_controls))
        self._special_device.set_enabled(True)
        self._device_selector.set_enabled(self._use_device_selector)
        if not self._use_device_selector:
            for index in range(8):
                self._mixer.channel_strip(index).set_select_button(self._column_button[index])

    def _assign_alternate_mappings(self, chan):
        for column in self._dial:
            for control in column:
                control.set_channel(chan)
                control.set_enabled(chan is 0)

        for column in self._button:
            for control in column:
                control.set_channel(chan)
                control.set_enabled(chan is 0)

        for control in self._column_button:
            control.set_channel(chan)
            control.set_enabled(chan is 0)

        for control in self._row_button:
            control.set_channel(chan)
            control.set_enabled(chan is 0)

    def disconnect(self):
        """clean things up on disconnect"""
        if self._shift_button is not None:
            if self._shift_button.value_has_listener(self._shift_value):
                self._shift_button.remove_value_listener(self._shift_value)
        for button in self._device_select_buttons:
            if button.value_has_listener(self._device_select_value):
                button.remove_value_listener(self._device_select_value)

        if self._session._is_linked():
            self._session._unlink()
        self.song().view.remove_selected_track_listener(self._update_selected_device)
        self._hosts = []
        if self._linked_script != None:
            self._linked_script._update_linked_device_selection = None
        self._linked_script = None
        self.log_message('<<<<<<<<<<<<<<<<<<<<<<<<< Codec log closed >>>>>>>>>>>>>>>>>>>>>>>>>')
        ControlSurface.disconnect(self)

    def connect_script_instances(self, instanciated_scripts):
        found = False
        for s in instanciated_scripts:
            if '_codec_version' in dir(s):
                if s._codec_version == self._version_check:
                    if s._host_name == 'MonOhm':
                        self.log_message('found codec version ' + str(s._codec_version) + ' in script ' + str(s._host_name))
                        found = True
                        self._linked_script = s
                        self._linked_script._update_linked_device_selection = self._update_linked_device_selection
                        if not self._session._is_linked() and self._link_mixer is True:
                            self._session.set_offsets(LINK_OFFSET[0], LINK_OFFSET[1])
                            self._session._link()
                else:
                    self.log_message('version mismatch: Monomod version ' + str(self._version_check) + ' vs. Host version ' + str(s._codec_version))

        if found == False:
            for s in instanciated_scripts:
                if '_codec_version' in dir(s):
                    if s._codec_version == self._version_check:
                        if s._host_name == 'BlockMod':
                            self.log_message('found codec version ' + str(s._codec_version) + ' in script ' + str(s._host_name))
                            self._linked_script = s
                            self._linked_script._update_linked_device_selection = self._update_linked_device_selection
                        if not self._session._is_linked() and self._link_mixer is True:
                            self._session.set_offsets(LINK_OFFSET[0], LINK_OFFSET[1])
                            self._session._link()
                    else:
                        self.log_message('version mismatch: Monomod version ' + str(self._version_check) + ' vs. Host version ' + str(s._codec_version))

    def update_display(self):
        ControlSurface.update_display(self)
        self._timer = (self._timer + 1) % 256
        if self._timer == 0:
            self._shift_pressed_timer = -12
        if self._local_ring_control is False:
            self.send_ring_leds()
        self.flash()

    def handle_sysex(self, midi_bytes):
        pass

    def flash(self):
        if self.flash_status > 0:
            for control in self.controls:
                if isinstance(control, MonoButtonElement):
                    control.flash(self._timer)

    def send_ring_leds(self):
        leds = [240,
         0,
         1,
         97,
         4,
         31]
        for column in range(8):
            for row in range(4):
                wheel = self._dial[column][row]
                bytes = wheel._get_ring()
                leds.append(bytes[0])
                leds.append(int(bytes[1]) + int(bytes[2]))

        leds.append(247)
        self._send_midi(tuple(leds))

    def set_absolute_mode(self, val = 1):
        self._absolute_mode = val != 0
        if self._absolute_mode is True:
            self._send_midi(tuple([240,
             0,
             1,
             97,
             4,
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
             4,
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

    def set_local_ring_control(self, val = 1):
        self._local_ring_control = val != 0
        if self._local_ring_control is True:
            self._send_midi(tuple([240,
             0,
             1,
             97,
             4,
             8,
             72,
             247]))
        else:
            self._send_midi(tuple([240,
             0,
             1,
             97,
             4,
             8,
             64,
             247]))

    def device_follows_track(self, val):
        self._device_selection_follows_track_selection = val == 1
        return self

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
        raise len(ret) == NUM_CHARS_PER_DISPLAY_STRIP or AssertionError
        return ret

    def notification_to_bridge(self, name, value, sender):
        if isinstance(sender, CodecEncoderElement):
            self._monobridge._send(sender.name, 'lcd_name', str(self.generate_strip_string(name)))
            self._monobridge._send(sender.name, 'lcd_value', str(self.generate_strip_string(value)))

    def touched(self):
        if not self._host.is_enabled():
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

    def allow_updates(self, allow_updates):
        for component in self.components:
            component.set_allow_update(int(allow_updates != 0))

    def set_device_component(self, device_component):
        if self._device_component != None:
            self._device_component._lock_callback = None
        raise device_component != None or AssertionError
        raise isinstance(device_component, DeviceComponent) or AssertionError
        self._device_component = device_component
        self._device_component._lock_callback = self._toggle_lock
        if self._device_select_buttons != None:
            for button in self._device_select_buttons:
                button.send_value(self._device_select_buttons.index(button) == self._device.index(self._device_component))

        self._update_device_selection()

    def _update_selected_device(self):
        if self._device_selection_follows_track_selection is True:
            self._update_device_selection()

    def _update_linked_device_selection(self, device):
        if self._device_component != None and device != None:
            if not self._device_component.is_locked():
                self._device_component.set_device(device)

    def _get_num_tracks(self):
        return self.num_tracks

    def _update_device_selection(self):
        if self._device_component != None:
            if not self._device_component.is_locked():
                track = self.song().view.selected_track
                device_to_select = track.view.selected_device
                if device_to_select == None and len(track.devices) > 0:
                    device_to_select = track.devices[0]
                if device_to_select != None:
                    self.song().view.select_device(device_to_select)
                self._device_component.set_device(device_to_select)

    def _channelstrip_mute_value(self, channelstrip):

        def _mute_value(value):
            if not self._shift_pressed:
                self.log_message('shift not pressed')
                ChannelStripComponent._mute_value(channelstrip, value)

        return _mute_value

    def _channelstrip_solo_value(self, channelstrip):

        def _solo_value(value):
            if not self._shift_pressed:
                ChannelStripComponent._solo_value(channelstrip, value)

        return _solo_value

    def _mixer_next_track_value(self, mixer):

        def _next_track_value(value):
            if not self._shift_pressed:
                MixerComponent._next_track_value(mixer, value)

        return _next_track_value

    def _mixer_prev_track_value(self, mixer):

        def _prev_track_value(value):
            if not self._shift_pressed:
                MixerComponent._prev_track_value(mixer, value)

        return _prev_track_value


class ParameterDefaultComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' MonoCode controller script '

    def __init__(self, script):
        """everything except the '_on_selected_track_changed' override and 'disconnect' runs from here"""
        ControlSurfaceComponent.__init__(self)
        self._script = script
        self._buttons = []
        self._dials = []

    def set_buttons(self, buttons):
        for button in self._buttons:
            if button.value_has_listener(self._value_to_default):
                button.remove_value_listener(self._value_to_default)

        self._buttons = buttons
        for button in self._buttons:
            button.add_value_listener(self._value_to_default, True)

    def set_dials(self, dials):
        raise len(dials) == len(self._buttons) or AssertionError
        self._dials = dials

    def _value_to_default(self, value, sender):
        if value > 0 and self._script._shift_pressed:
            dial = self._dials[self._buttons.index(sender)]
            if dial != None:
                if dial.mapped_parameter() != None:
                    if hasattr(dial.mapped_parameter(), 'default_value'):
                        dial.mapped_parameter().value = dial.mapped_parameter().default_value

    def update(self):
        pass

    def disconnect(self):
        for button in self._buttons:
            if button.value_has_listener(self._value_to_default):
                button.remove_value_listener(self._value_to_default)