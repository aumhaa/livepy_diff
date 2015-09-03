
from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.ButtonElement import *
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.Layer import Layer
from _Framework.ModesComponent import AddLayerMode
from _Framework.Skin import Skin
from Launchpad.Launchpad import Launchpad
from Launchpad.SubSelectorComponent import SubSelectorComponent as LaunchpadSubSelectorComponent
from Launchpad.SpecialMixerComponent import SpecialMixerComponent as LaunchpadSpecialMixerComponent
from Launchpad.MainSelectorComponent import MainSelectorComponent as LaunchpadMainSelectorComponent
from Launchpad.DefChannelStripComponent import DefChannelStripComponent as LaunchpadDefChannelStripComponent
from _Mono_Framework.MonoBridgeElement import MonoBridgeElement
from _Mono_Framework.MonoButtonElement import MonoButtonElement
from _Mono_Framework.Mod import *
from _Mono_Framework.Debug import *
debug = initialize_debug()
SIDE_NOTES = (8, 24, 40, 56, 72, 88, 104, 120)
DRUM_NOTES = (41, 42, 43, 44, 45, 46, 47, 57, 58, 59, 60, 61, 62, 63, 73, 74, 75, 76, 77, 78, 79, 89, 90, 91, 92, 93, 94, 95, 105, 106, 107)
START_IN_MOD = False
from _Mono_Framework.LividColors import *

class LaunchModColors:

    class DefaultButton:
        On = Color(127)
        Off = Color(0)
        Disabled = Color(0)
        Alert = Color(64)

    class Mod:

        class Nav:
            OnValue = Color(64)
            OffValue = Color(5)


class LaunchMod(Launchpad):

    def __init__(self, *a, **k):
        ControlSurface.__init__(self, *a, **k)
        self._skin = Skin(LaunchModColors)
        with self.component_guard():
            self._monomod_version = 'b996'
            self._host_name = 'LaunchMod'
            self._color_type = 'Launchpad'
            self._timer = 0
            self._suppress_send_midi = True
            self._suppress_session_highlight = True
            self._suppress_highlight = False
            is_momentary = True
            self._suggested_input_port = 'Launchpad'
            self._suggested_output_port = 'Launchpad'
            self._control_is_with_automap = False
            self._user_byte_write_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 16)
            self._user_byte_write_button.name = 'User_Byte_Button'
            self._user_byte_write_button.send_value(1)
            self._user_byte_write_button.add_value_listener(self._user_byte_value)
            self._wrote_user_byte = False
            self._challenge = Live.Application.get_random_int(0, 400000000) & 2139062143
            matrix = ButtonMatrixElement(name='Button_Matrix')
            for row in range(8):
                button_row = [ ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, row * 16 + column, str(column) + '_Clip_' + str(row) + '_Button', self, skin=self._skin) for column in range(8) ]
                matrix.add_row(tuple(button_row))

            self._matrix = matrix
            self._config_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 0, optimized_send_midi=False)
            self._config_button.add_value_listener(self._config_value)
            top_button_names = ['Bank_Select_Up_Button',
             'Bank_Select_Down_Button',
             'Bank_Select_Left_Button',
             'Bank_Select_Right_Button',
             'Session_Button',
             'User1_Button',
             'User2_Button',
             'Mixer_Button']
            side_button_names = ['Vol_Button',
             'Pan_Button',
             'SndA_Button',
             'SndB_Button',
             'Stop_Button',
             'Trk_On_Button',
             'Solo_Button',
             'Arm_Button']
            top_buttons = [ ConfigurableButtonElement(is_momentary, MIDI_CC_TYPE, 0, 104 + index, top_button_names[index], self, skin=self._skin) for index in range(8) ]
            self._top_buttons = top_buttons
            side_buttons = [ ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, SIDE_NOTES[index], side_button_names[index], self, skin=self._skin) for index in range(8) ]
            self._side_buttons = ButtonMatrixElement(name='SideButtons', rows=[side_buttons])
            self._setup_monobridge()
            self._setup_mod()
            self._selector = MainSelectorComponent(self, matrix, tuple(top_buttons), tuple(side_buttons), self._config_button)
            self._selector.name = 'Main_Modes'
            for control in self.controls:
                isinstance(control, MonoButtonElement) and control.add_value_listener(self._button_value)

            self.set_highlighting_session_component(self._selector.session_component())
            self._suppress_session_highlight = False
        self.log_message('--------------= ' + str(self._monomod_version) + ' log opened =--------------')

    def _setup_monobridge(self):
        self._monobridge = MonoBridgeElement(self)
        self._monobridge.name = 'MonoBridge'

    def _setup_mod(self):
        self.monomodular = get_monomodular(self)
        self.monomodular.name = 'monomodular_switcher'
        self.modhandler = LaunchModHandler(self)
        self.modhandler.name = 'ModHandler'
        self.modhandler.layer = Layer(shift_button=self._top_buttons[4], lock_button=self._top_buttons[5], alt_button=self._top_buttons[6], key_buttons=self._side_buttons, nav_up_button=self._top_buttons[0], nav_down_button=self._top_buttons[1], nav_left_button=self._top_buttons[2], nav_right_button=self._top_buttons[3])
        self.modhandler.shift_layer = AddLayerMode(self.modhandler, Layer(device_selector_matrix=self._matrix.submatrix[:, :1]))
        self.modhandler.legacy_shift_layer = AddLayerMode(self.modhandler, Layer(channel_buttons=self._matrix.submatrix[:, 1:2], nav_matrix=self._matrix.submatrix[2:6, 2:6]))

    def update_display(self):
        ControlSurface.update_display(self)
        self._timer = (self._timer + 1) % 256
        self.flash()

    def flash(self):
        if self.modhandler.is_enabled():
            for control in self.controls:
                if isinstance(control, MonoButtonElement):
                    control.flash(self._timer)

    def disconnect(self):
        super(LaunchMod, self).disconnect()
        rebuild_sys()


class LaunchModHandler(ModHandler):

    def __init__(self, *a, **k):
        super(LaunchModHandler, self).__init__(*a, **k)
        self._color_type = 'RGB'
        self._colors = range(128)
        self._is_shifted = False
        self.nav_box = self.register_component(NavigationBox(self, 16, 16, 8, 8, self.set_offset))

    def _receive_grid(self, x, y, value, *a, **k):
        if self.is_enabled() and self._grid:
            mod = self.active_mod()
            if mod:
                if mod.legacy:
                    x = x - self.x_offset
                    y = y - self.y_offset
                if x in range(8) and y in range(8):
                    self._grid.send_value(x, y, self._colors[value], True)

    def set_grid(self, grid):
        self._grid = grid
        self._grid_value.subject = self._grid

    @subject_slot('value')
    def _grid_value(self, value, x, y, *a, **k):
        mod = self.active_mod()
        if mod:
            if mod.legacy:
                x = x + self.x_offset
                y = y + self.y_offset
            mod.send('grid', x, y, value)

    @subject_slot('value')
    def _shift_value(self, value, *a, **k):
        self._is_shifted = value is not 0
        mod = self.active_mod()
        if mod:
            mod.send('shift', value)
        self.update()

    def update(self, *a, **k):
        if self.is_enabled():
            mod = self.active_mod()
            if mod:
                mod.restore()
            else:
                if self._grid_value.subject is not None:
                    self._grid_value.subject.reset()
                if self._keys_value.subject is not None:
                    self._keys_value.subject.reset()
            self.update_buttons()


class MainSelectorComponent(LaunchpadMainSelectorComponent):

    def __init__(self, script, *a, **k):
        self._script = script
        LaunchpadMainSelectorComponent.__init__(self, *a, **k)
        self._sub_modes._mixer = SpecialMixerComponent(self._matrix.width())
        if START_IN_MOD is True:
            self._set_protected_mode_index(4)

    def set_mode(self, mode):
        if not mode in range(self.number_of_modes()):
            raise AssertionError
            self._mode_index = (self._mode_index != mode or mode == 3) and mode
            self.update()

    def update(self):
        raise self._modes_buttons != None or AssertionError
        if self.is_enabled():
            for scene_index in range(8):
                self._side_buttons[scene_index].set_enabled(True)
                for track_index in range(8):
                    button = self._matrix.get_button(track_index, scene_index)
                    button and button.set_enabled(True)

            for button in self._nav_buttons:
                button.set_enabled(True)

            as_active = True
            as_enabled = True
            self._session.set_allow_update(False)
            self._zooming.set_allow_update(False)
            self._config_button.send_value(40)
            self._config_button.send_value(1)
            release_buttons = self._mode_index == 1
            if self._mode_index < 4:
                self._script.modhandler.legacy_shift_layer.leave_mode()
                self._script.modhandler.shift_layer.leave_mode()
                self._script.modhandler.set_grid(None)
                self._script.modhandler.set_enabled(False)
                self._script._suppress_session_highlight = False
                self._session.set_show_highlight(True)
                for button in self._modes_buttons:
                    button.set_on_off_values(127, 4)

                if self._mode_index == 0:
                    self._setup_mixer(not as_active)
                    self._setup_session(as_active, as_enabled)
                elif self._mode_index == 1:
                    self._setup_session(not as_active, not as_enabled)
                    self._setup_mixer(not as_active)
                    self._setup_user(release_buttons)
                elif self._mode_index == 2:
                    self._setup_session(not as_active, not as_enabled)
                    self._setup_mixer(not as_active)
                    self._setup_user(release_buttons)
                elif self._mode_index == 3:
                    self._setup_session(not as_active, as_enabled)
                    self._setup_mixer(as_active)
            elif self._mode_index == 4:
                self._session.set_show_highlight(False)
                self._script._suppress_session_highlight = True
                self._setup_session(not as_active, not as_enabled)
                self._setup_mixer(not as_active)
                self._setup_user(release_buttons)
                self._modes_buttons[3].send_value(9)
                self._script.modhandler.set_enabled(True)
                self._script.modhandler.set_grid(self._matrix)
            else:
                raise False or AssertionError
            self._session.set_allow_update(True)
            self._zooming.set_allow_update(True)
            self._update_control_channels()
            if self._mode_index < 4:
                for index in range(len(self._modes_buttons)):
                    if index == self._mode_index:
                        self._modes_buttons[index].turn_on()
                    else:
                        self._modes_buttons[index].turn_off()

            self._script.schedule_message(1, self._session.update)

    def _update_control_channels(self):
        if self._mode_index < 4:
            new_channel = self.channel_for_current_mode()
        else:
            new_channel = 15
        for button in self._all_buttons:
            button.set_channel(new_channel)
            button.set_force_next_value()

    def _mode_value(self, value, sender):
        if not len(self._modes_buttons) > 0:
            raise AssertionError
            raise isinstance(value, int) or AssertionError
            raise isinstance(sender, ButtonElement) or AssertionError
            if not self._modes_buttons.count(sender) == 1:
                raise AssertionError
                if self._script.modhandler.is_enabled() != True:
                    (value is not 0 or not sender.is_momentary()) and (self._modes_buttons[1]._last_received_value > 0 and self._modes_buttons.index(sender) == 2 or self._modes_buttons[2]._last_received_value > 0 and self._modes_buttons.index(sender) == 1) and self.set_mode(4)
                else:
                    self.set_mode(self._modes_buttons.index(sender))
        elif self._modes_buttons.index(sender) == 3 and value > 0:
            self.set_mode(0)

    def number_of_modes(self):
        return 5


class ConfigurableButtonElement(MonoButtonElement):
    """ Special button class that can be configured with custom on- and off-values """

    def __init__(self, *a, **k):
        MonoButtonElement.__init__(self, *a, **k)
        self._color_map = [20,
         21,
         5,
         36,
         38,
         6,
         52,
         55,
         7]
        self._num_flash_states = 13
        self._num_colors = 9
        self._darkened = 4
        self._on_value = 127
        self._off_value = 4
        self._is_enabled = True
        self._is_notifying = False
        self._force_next_value = False
        self._pending_listeners = []

    def set_on_off_values(self, on_value, off_value):
        self.clear_send_cache()
        self._on_value = on_value
        self._off_value = off_value

    def set_force_next_value(self):
        self._force_next_value = True

    def add_value_listener(self, callback, identify_sender = False):
        if not self._is_notifying:
            ButtonElement.add_value_listener(self, callback, identify_sender)
        else:
            self._pending_listeners.append((callback, identify_sender))

    def receive_value(self, value):
        self._is_notifying = True
        MonoButtonElement.receive_value(self, value)
        self._is_notifying = False
        for listener in self._pending_listeners:
            self.add_value_listener(listener[0], listener[1])

        self._pending_listeners = []

    def send_value(self, *a, **k):
        if self._script.modhandler.is_enabled():
            super(ConfigurableButtonElement, self).send_value(*a, **k)
        else:
            ButtonElement.send_value(self, *a, **k)
            self._force_next_value = False

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        if self._is_enabled:
            MonoButtonElement.install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback)
        elif self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
            install_translation_callback(self._msg_type, self._original_identifier, self._original_channel, self._msg_identifier, self._msg_channel)


class DefChannelStripComponent(LaunchpadDefChannelStripComponent):

    def set_default_buttons(self, volume, panning, send1, send2):
        if not (volume == None or isinstance(volume, ConfigurableButtonElement or MonoButtonElement)):
            raise AssertionError
            if not (panning == None or isinstance(panning, ConfigurableButtonElement or MonoButtonElement)):
                raise AssertionError
                if not (send1 == None or isinstance(send1, ConfigurableButtonElement or MonoButtonElement)):
                    raise AssertionError
                    if not (send2 == None or isinstance(send2, ConfigurableButtonElement or MonoButtonElement)):
                        raise AssertionError
                        if volume != self._default_volume_button:
                            if self._default_volume_button != None:
                                self._default_volume_button.remove_value_listener(self._default_volume_value)
                            self._default_volume_button = volume
                            if self._default_volume_button != None:
                                self._default_volume_button.add_value_listener(self._default_volume_value)
                        if panning != self._default_panning_button:
                            if self._default_panning_button != None:
                                self._default_panning_button.remove_value_listener(self._default_panning_value)
                            self._default_panning_button = panning
                            if self._default_panning_button != None:
                                self._default_panning_button.add_value_listener(self._default_panning_value)
                        if send1 != self._default_send1_button:
                            if self._default_send1_button != None:
                                self._default_send1_button.remove_value_listener(self._default_send1_value)
                            self._default_send1_button = send1
                            self._default_send1_button != None and self._default_send1_button.add_value_listener(self._default_send1_value)
                    send2 != self._default_send2_button and self._default_send2_button != None and self._default_send2_button.remove_value_listener(self._default_send2_value)
                self._default_send2_button = send2
                self._default_send2_button != None and self._default_send2_button.add_value_listener(self._default_send2_value)
        self.update()


class SpecialMixerComponent(LaunchpadSpecialMixerComponent):

    def _create_strip(self):
        return DefChannelStripComponent()