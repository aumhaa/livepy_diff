#Embedded file name: /Applications/Ableton Live 9.05 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Codec_b995_9/CodecDeviceSelectorComponent.py
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Tools.re import *

class CodecDeviceSelectorComponent(ModeSelectorComponent):
    __module__ = __name__
    __doc__ = ' Class for selecting a device based on a prefix added to its name'

    def __init__(self, script, prefix, devices, *a, **k):
        super(CodecDeviceSelectorComponent, self).__init__(*a, **k)
        self._script = script
        self._mode_index = 0
        self._number_of_modes = 0
        self._prefix = prefix

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
                self._number_of_modes = len(self._modes_buttons)

            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()

    def set_mode_toggle(self, button):
        if not (button == None or isinstance(button, ButtonElement)):
            raise AssertionError
            if self._mode_toggle != None:
                self._mode_toggle.remove_value_listener(self._toggle_value)
            self._mode_toggle = button
            self._mode_toggle != None and self._mode_toggle.add_value_listener(self._toggle_value)

    def number_of_modes(self):
        return self._number_of_modes

    def update(self):
        if self.is_enabled():
            for button in range(len(self._modes_buttons)):
                if button is self._mode_index:
                    self._modes_buttons[button].turn_on()
                else:
                    self._modes_buttons[button].turn_off()

    def set_mode(self, mode):
        raise self.is_enabled() and (isinstance(mode, int) or AssertionError)
        if not mode in range(self.number_of_modes()):
            raise AssertionError
            if self._mode_index != mode:
                self._mode_index = mode
                keys = (str('c' + str(self._mode_index + 1)), str('p' + str(self._mode_index + 1)))
                preset = None
                for key in keys:
                    if preset == None:
                        for track_type in (self.song().tracks, self.song().return_tracks, [self.song().master_track]):
                            for track in track_type:
                                for device in track.devices:
                                    if match(key, str(device.name)) != None:
                                        preset = device
                                        break
                                    elif device.can_have_chains:
                                        for chain in device.chains:
                                            for chain_device in chain.devices:
                                                if match(key, str(chain_device.name)) != None:
                                                    preset = chain_device
                                                    break

                if preset != None:
                    self._script._device_component.set_device(preset)
                    self._script.request_rebuild_midi_map()
                self.update()

    def set_preset(self, preset):
        pass

    def on_enabled_changed(self):
        self.update()