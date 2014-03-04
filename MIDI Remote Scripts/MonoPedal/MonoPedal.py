
from __future__ import with_statement
import Live
import time
import math
import sys
from _Tools.re import *
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
from _Framework.Layer import Layer
from _Framework.ModesComponent import AddLayerMode, MultiEntryMode, ModesComponent, SetAttributeMode, CancellableBehaviour, AlternativeBehaviour, ReenterBehaviour, DynamicBehaviourMixin, ExcludingBehaviourMixin, EnablingModesComponent
from Push.ComboElement import ComboElement, DoublePressElement, MultiElement, DoublePressContext
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
PEDAL_DEFS = [64,
 65,
 66,
 67,
 68,
 69,
 70]
LED_DEFS = [4,
 3,
 2,
 1,
 8,
 7,
 6,
 5,
 12,
 11,
 10,
 9]
VALUES = [[1, 1, 1],
 [1, 1, 0],
 [0, 1, 1],
 [1, 0, 1],
 [1, 0, 0],
 [0, 1, 0],
 [0, 0, 1]]
STATE_COLORS = [5,
 1,
 6,
 3,
 4,
 7]
LIVE_STATE_COLORS = [7,
 5,
 6,
 3]

class LoopPedalButtonElement(MonoButtonElement):

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


class RGB_LED(MonoButtonElement):

    def __init__(self, red, green, blue, *a, **k):
        super(RGB_LED, self).__init__(*a, **k)
        self._color_map = [1,
         2,
         3,
         4,
         5,
         6,
         7]
        self._red = red
        self._green = green
        self._blue = blue

    def send_value(self, value, force = False):
        raise type(self) != type(None) and (value != None or AssertionError)
        raise isinstance(value, int) or AssertionError
        if not value in range(128):
            raise AssertionError
            if force or self._force_next_send or value != self._last_sent_value and self._is_being_forwarded:
                data_byte1 = self._original_identifier
                if value in range(1, 127):
                    data_byte2 = self._color_map[(value - 1) % self._num_colors]
                elif value == 127:
                    data_byte2 = self._color_map[self._num_colors - 1]
                else:
                    data_byte2 = self._darkened
                self._color = data_byte2
                self.send_RGB(data_byte2)
                self._last_sent_message = [value]
                if self._report_output:
                    is_input = True
                    self._report_value(value, not is_input)
                self._flash_state = round((value - 1) / self._num_colors)
                self._force_next_value = False

    def flash(self, timer):
        if self._is_being_forwarded and self._flash_state in range(1, self._num_flash_states) and timer % self._flash_state == 0:
            data_byte2 = self._color * int(timer % (self._flash_state * 2) > 0)
            status_byte = self._original_channel
            self.send_RGB(data_byte2)

    def send_RGB(self, value):
        values = [0, 0, 0]
        if not value == 0:
            values = VALUES[(value - 1) % 7]
        self._red.send_value(values[0] * 127, True)
        self._green.send_value(values[1] * 127, True)
        self._blue.send_value(values[2] * 127, True)


class MonolooperComponent(CompoundComponent):

    def __init__(self, leds, script, *a, **k):
        super(MonolooperComponent, self).__init__(*a, **k)
        self._script = script
        self._leds = leds
        self._all_loops_selected = False
        self._selected_loop = None
        self._select_buttons_pressed = []
        self._select_buttons = None
        self._doublepress_select_buttons = None
        self._record_button = None
        self._overdub_button = None
        self._mute_button = None
        self._loopers = [ Monoloop(self, index, self._leds[index]) for index in range(4) ]
        for looper in self._loopers:
            self.register_components(looper)

        self.song().add_appointed_device_listener(self.on_enabled_changed)
        self._select_looper(0)

    def disconnect(self, *a, **k):
        super(MonolooperComponent, self).disconnect()
        if self.song().appointed_device_has_listener(self.on_enabled_changed):
            self.song().remove_appointed_device_listener(self.on_enabled_changed)

    def update(self):
        if self.is_enabled():
            for index in range(len(self._loopers)):
                key = str('@loop' + str(index + 1))
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

                self._loopers[index].set_device(preset)

    def on_enabled_changed(self):
        if self.is_enabled():
            self.update()

    def set_select_buttons(self, matrix):
        self._select_buttons = matrix
        self._on_select_value.subject = matrix

    def set_doublepress_select_buttons(self, matrix):
        self._doublepress_select_buttons = matrix
        self._on_doublepress_select_value.subject = matrix

    def set_record_button(self, button):
        self._record_button = button
        self._on_record_value.subject = button

    def set_mute_button(self, button):
        self._mute_button = button
        self._on_mute_value.subject = button

    def set_overdub_button(self, button):
        self._overdub_button = button
        self._on_overdub_value.subject = button

    def set_expression_pedal(self, pedal):
        self._expression_pedal = pedal
        self._on_expression_value.subject = pedal

    def set_leds(self, leds):
        raise len(leds) == len(self._loopers) or AssertionError
        for index in range(len(self._loopers)):
            self._loopers[index]._set_led(leds[index])

    @subject_slot('value')
    def _on_select_value(self, value, x, y, is_momentary):
        buttons = self._on_select_value.subject
        button = self._on_select_value.subject.get_button(x, y)
        if value:
            self._select_buttons_pressed.append(button)
            if buttons[1] in self._select_buttons_pressed and buttons[2] in self._select_buttons_pressed:
                self._select_buttons_pressed.remove(buttons[1])
                self._select_buttons_pressed.remove(buttons[2])
                self._select_all_loops()
            if buttons[0] in self._select_buttons_pressed and buttons[1] in self._select_buttons_pressed:
                self._select_buttons_pressed.remove(buttons[0])
                self._select_buttons_pressed.remove(buttons[1])
                self._select_prev_loop()
            if buttons[2] in self._select_buttons_pressed and buttons[3] in self._select_buttons_pressed:
                self._select_buttons_pressed.remove(buttons[2])
                self._select_buttons_pressed.remove(buttons[3])
                self._select_next_loop()
        elif button in self._select_buttons_pressed:
            self._select_buttons_pressed.remove(button)
            self._select_looper(x)

    @subject_slot('value')
    def _on_doublepress_select_value(self, value, x, y, is_momentary):
        self._script.toggle_device_control(x)

    @subject_slot('value')
    def _on_record_value(self, value):
        if not self._all_loops_selected:
            self._selected_loop.hit_record(value)

    @subject_slot('value')
    def _on_mute_value(self, value):
        loops = self._loopers if self._all_loops_selected else [self._selected_loop]
        if self._on_select_value.subject and self._on_select_value.subject.get_button(3, 0) in self._select_buttons_pressed:
            self._select_buttons_pressed.remove(self._on_select_value.subject.get_button(3, 0))
            if value:
                for loop in loops:
                    loop.hit_reverse()

        elif len(loops) > 1:
            for loop in loops:
                loop.set_mute(1)

        else:
            for loop in loops:
                loop.hit_mute(value)

    @subject_slot('value')
    def _on_overdub_value(self, value):
        loops = self._loopers if self._all_loops_selected else [self._selected_loop]
        if self._on_select_value.subject and self._on_select_value.subject.get_button(0, 0) in self._select_buttons_pressed:
            if value:
                self._select_buttons_pressed.remove(self._on_select_value.subject.get_button(0, 0))
                for loop in loops:
                    loop.hit_clear()

        else:
            for loop in loops:
                loop.hit_overdub(value)

    @subject_slot('value')
    def _on_expression_value(self, value):
        loops = self._loopers if self._all_loops_selected else [self._selected_loop]
        for loop in loops:
            loop.set_feedback(value)

    def _select_looper(self, number):
        self._all_loops_selected = False
        self._selected_loop = self._loopers[number]
        self._selected_loop.display_looper()
        self.update()

    def _select_all_loops(self):
        if self._all_loops_selected:
            self._all_loops_selected = False
            self._script.toggle_mode()
        else:
            self._all_loops_selected = True
            self.update()

    def _select_prev_loop(self):
        self._select_looper(max(0, self._selected_loop._index - 1))

    def _select_next_loop(self):
        self._select_looper(min(3, self._selected_loop._index + 1))

    def enumerate_track_device(self, track):
        devices = []
        if hasattr(track, 'devices'):
            for device in track.devices:
                devices.append(device)
                if device.can_have_chains:
                    for chain in device.chains:
                        for chain_device in self.enumerate_track_device(chain):
                            devices.append(chain_device)

        return devices


class Monoloop(ControlSurfaceComponent):

    def __init__(self, parent, index, led, *a, **k):
        super(Monoloop, self).__init__()
        self._parent = parent
        self._script = parent._script
        self._index = index
        self._led = led
        self._parameters = None
        self._controls = None
        self._device = None
        self._record = None
        self._overdub = None
        self._mute = None
        self._clear = None
        self._reverse = None
        self._feedback = None
        self._volume = None
        self._speed = None
        self._livereverse = None
        self._livefeedback = None

    def set_device(self, device):
        self._device = None
        self.on_state_change.subject = None
        self.on_position_change.subject = None
        self._record = None
        self._overdub = None
        self._mute = None
        self._clear = None
        self._reverse = None
        self.on_livelooper_state_change.subject = None
        self._livereverse = None
        if isinstance(device, Live.Device.Device):
            if str(device.class_name) == 'MxDeviceAudioEffect':
                self._device = device
                for parameter in device.parameters:
                    if parameter.name == 'state':
                        self.on_state_change.subject = parameter
                    elif parameter.name == 'position':
                        self.on_position_change.subject = parameter
                    elif parameter.name == 'loop':
                        self._record = parameter
                    elif parameter.name == 'overdub':
                        self._overdub = parameter
                    elif parameter.name == 'mute':
                        self._mute = parameter
                    elif parameter.name == 'clear':
                        self._clear = parameter
                    elif parameter.name == 'reverse':
                        self._reverse = parameter
                    elif parameter.name == 'feedback':
                        self._feedback = parameter
                    elif parameter.name == 'volume':
                        self._volume = parameter
                    elif parameter.name == 'speed':
                        self._speed = parameter

            elif str(device.class_name == 'Looper'):
                self._device = device
                for parameter in device.parameters:
                    if parameter.name == 'State':
                        self.on_livelooper_state_change.subject = parameter
                    elif parameter.name == 'Reverse':
                        self._livereverse = parameter
                    elif parameter.name == 'Feedback':
                        self._livefeedback = parameter

        self.update()

    @subject_slot('value')
    def on_state_change(self):
        if self.is_enabled():
            if not self.on_state_change.subject == None:
                val = int(self.on_state_change.subject.value)
                if val < len(STATE_COLORS):
                    self._led.send_value(STATE_COLORS[val] + self.is_selected() * 7, True)

    @subject_slot('value')
    def on_livelooper_state_change(self):
        if self.is_enabled():
            if not self.on_livelooper_state_change.subject == None:
                self._led.send_value(LIVE_STATE_COLORS[int(self.on_livelooper_state_change.subject.value)] + self.is_selected() * 7, True)

    @subject_slot('value')
    def on_position_change(self):
        pass

    @subject_slot('value')
    def on_mute_change(self):
        self.on_state_change()

    @subject_slot('value')
    def on_record_change(self):
        self.on_state_change()

    @subject_slot('value')
    def on_overdub_change(self):
        self.on_state_change()

    def update(self):
        if self._device is not None:
            self.on_state_change()
            self.on_livelooper_state_change()
        else:
            self._led.send_value(0, True)

    def hit_record(self, value):
        if self._record is not None:
            self._record.begin_gesture()
            self._record.value = self._record.max if value else self._record.min
            self._record.end_gesture()
        elif self.on_livelooper_state_change.subject is not None and value:
            self.on_livelooper_state_change.subject.value = 2 if not self.on_livelooper_state_change.subject.value != 1 else 1

    def hit_overdub(self, value):
        if self._overdub is not None:
            self._overdub.begin_gesture()
            self._overdub.value = self._overdub.max if value else self._overdub.min
            self._overdub.end_gesture()
        elif self.on_livelooper_state_change.subject is not None and value:
            self.on_livelooper_state_change.subject.value = 3 if self.on_livelooper_state_change.subject.value != 3 else 2

    def hit_mute(self, value):
        if self._mute is not None:
            self._mute.begin_gesture()
            self._mute.value = self._mute.max if value else self._mute.min
            self._mute.end_gesture()
        elif self.on_livelooper_state_change.subject is not None and value:
            self.on_livelooper_state_change.subject.value = 0 if self.on_livelooper_state_change.subject.value != 0 else 2

    def set_mute(self, val):
        if self._mute is not None:
            if val:
                if not self.on_state_change.subject.value == 5:
                    self._mute.value = self._mute.max
                    self._mute.value = self._mute.min
            elif self.on_state_change.subject.value == 5:
                self._mute.value = self._mute.max
                self._mute.value = self._mute.min
        elif self.on_livelooper_state_change.subject is not None:
            if val:
                if not self.on_livelooper_state_change.subject.value == 0:
                    self.on_livelooper_state_change.subject.value = 0
                else:
                    self.on_livelooper_state_change.subject.value = 2

    def hit_clear(self):
        if self._clear is not None:
            self._clear.value = self._clear.max
            self._clear.value = self._clear.min

    def hit_reverse(self):
        if self._reverse is not None:
            self._reverse.value = self._reverse.max
            self._reverse.value = self._reverse.min
        elif self._livereverse is not None:
            self._livereverse.value = self._livereverse.max if self._livereverse.value == self._livereverse.min else self._livereverse.min

    def set_feedback(self, val):
        if self._feedback is not None:
            self._feedback.value = (self._feedback.max - self._feedback.min) * val / 127 + self._feedback.min
        elif self._livefeedback is not None:
            self._livefeedback.value = (self._livefeedback.max - self._livefeedback.min) * val / 127 + self._livefeedback.min

    def is_selected(self):
        return self is self._parent._selected_loop or self._parent._all_loops_selected

    def display_looper(self):
        if self._device is not None:
            self.song().view.select_device(self._device)


class LauncherSlot(ControlSurfaceComponent):

    def __init__(self, parent, number, led, *a, **k):
        super(LauncherSlot, self).__init__(*a, **k)
        self._script = parent._script
        self._parent = parent
        self._number = number
        self._clip = None
        self._scene = None
        self._bank = 0
        self._led = led

    def set_slot(self, slot):
        self._slot = slot
        if self.is_enabled():
            self.update()

    def update(self):
        pass

    def launch(self):
        if self.is_enabled() and self._slot is not None:
            self._slot.fire()


class LauncherComponent(CompoundComponent):

    def __init__(self, leds, script, *a, **k):
        super(LauncherComponent, self).__init__(*a, **k)
        self._script = script
        self._leds = leds
        self._all_loops_selected = False
        self._selected_loop = None
        self._select_buttons_pressed = []
        self._select_buttons = None
        self._doublepress_select_buttons = None
        self._fire1_button = None
        self._fire2_button = None
        self._fire3_button = None
        self._bank = 0
        self._launchers = [ LauncherSlot(self, index, self._leds[index]) for index in range(3) ]
        for launcher in self._launchers:
            self.register_components(launcher)

    def disconnect(self, *a, **k):
        super(LauncherComponent, self).disconnect()

    def update(self):
        if self.is_enabled():
            for launcher in self._launchers:
                key = str('@launch ' + str(self._bank + 1) + ' ' + str(launcher._number + 1))
                slot = None
                for scene in self.song().scenes:
                    if match(key, str(scene.name)) != None:
                        slot = scene
                        break

                launcher.set_slot(slot)

            for index in range(len(self._leds)):
                self._leds[index].send_value(int(index == self._bank), True)

    def on_enabled_changed(self):
        if self.is_enabled():
            self.update()

    def set_select_buttons(self, matrix):
        self._select_buttons = matrix
        self._on_select_value.subject = matrix

    def set_doublepress_select_buttons(self, matrix):
        self._doublepress_select_buttons = matrix
        self._on_doublepress_select_value.subject = matrix

    def set_fire1_button(self, button):
        self._fire1_button = button
        self.on_fire1_value.subject = button

    def set_fire2_button(self, button):
        self._fire2_button = button
        self.on_fire2_value.subject = button

    def set_fire3_button(self, button):
        self._fire3_button = button
        self.on_fire3_value.subject = button

    def set_expression_pedal(self, pedal):
        self._expression_pedal = pedal
        self._on_expression_value.subject = pedal

    @subject_slot('value')
    def _on_select_value(self, value, x, y, is_momentary):
        buttons = self._on_select_value.subject
        button = self._on_select_value.subject.get_button(x, y)
        if value:
            self._select_buttons_pressed.append(button)
            if buttons[1] in self._select_buttons_pressed and buttons[2] in self._select_buttons_pressed:
                self._select_buttons_pressed.remove(buttons[1])
                self._select_buttons_pressed.remove(buttons[2])
                self._script.toggle_mode()
            if buttons[0] in self._select_buttons_pressed and buttons[1] in self._select_buttons_pressed:
                self._select_buttons_pressed.remove(buttons[0])
                self._select_buttons_pressed.remove(buttons[1])
                self._reset_loopers()
            if buttons[2] in self._select_buttons_pressed and buttons[3] in self._select_buttons_pressed:
                self._select_buttons_pressed.remove(buttons[2])
                self._select_buttons_pressed.remove(buttons[3])
                self._stop_clips()
        elif button in self._select_buttons_pressed:
            self._select_buttons_pressed.remove(button)
            self.set_bank(x)

    @subject_slot('value')
    def _on_doublepress_select_value(self, value, x, y, is_momentary):
        self._script.toggle_device_control(x)

    @subject_slot('value')
    def on_fire1_value(self, value):
        self._launchers[0].launch()

    @subject_slot('value')
    def on_fire2_value(self, value):
        self._launchers[1].launch()

    @subject_slot('value')
    def on_fire3_value(self, value):
        self._launchers[2].launch()

    @subject_slot('value')
    def _on_expression_value(self, value):
        pass

    def set_bank(self, val):
        self._bank = val
        self.update()

    def _reset_loopers(self):
        pass

    def _stop_clips(self):
        pass


class ParameterSlot(ControlSurfaceComponent):

    def __init__(self, parent, number, led, *a, **k):
        super(ParameterSlot, self).__init__(*a, **k)
        self._script = parent._script
        self._parent = parent
        self._number = number
        self._parameter = None
        self._led = led

    def set_parameter(self, parameter):
        self._parameter = parameter
        if self.is_enabled():
            self.update()

    def update(self):
        pass

    def set_value(self, value):
        if self.is_enabled() and self._parameter is not None:
            self._parameter.value = (self._parameter.max - self._parameter.min) * (value / 127.0) + self._parameter.min

    def toggle(self):
        if self.is_enabled() and self._parameter is not None:
            self._parameter.value = self._parameter.max if self._parameter.value == self._parameter.min else self._parameter.min


class DeviceControlComponent(CompoundComponent):

    def __init__(self, leds, script, *a, **k):
        super(DeviceControlComponent, self).__init__(*a, **k)
        self._script = script
        self._leds = leds
        self._all_loops_selected = False
        self._selected_loop = None
        self._select_buttons_pressed = []
        self._select_buttons = None
        self._doublepress_select_buttons = None
        self._toggle1_button = None
        self._toggle2_button = None
        self._toggle3_button = None
        self._bank = 0
        self._parameters = [ ParameterSlot(self, index, self._leds[index]) for index in range(3) ]
        self._exp_parameter = ParameterSlot(self, 3, None)

    def disconnect(self, *a, **k):
        super(DeviceControlComponent, self).disconnect()

    def update(self):
        if self.is_enabled():
            key = str('@fx' + str(self._bank + 1))
            found_device = None
            for track in self.song().tracks:
                for device in self.enumerate_track_device(track):
                    if match(key, str(device.name)) != None:
                        found_device = device
                        break

            for return_track in self.song().return_tracks:
                for device in self.enumerate_track_device(return_track):
                    if match(key, str(device.name)) != None:
                        found_device = device
                        break

            for device in self.enumerate_track_device(self.song().master_track):
                if match(key, str(device.name)) != None:
                    found_device = device
                    break

            if found_device != None:
                self.song().view.select_device(found_device)
            if found_device is not None:
                for slot in self._parameters:
                    key = str('@param' + str(slot._number + 1))
                    param = None
                    for parameter in found_device.parameters:
                        if match(key, str(parameter.name)) != None:
                            param = parameter
                            break

                    slot.set_parameter(param)

                key = str('@exp')
                param = None
                for parameter in found_device.parameters:
                    if match(key, str(parameter.name)) != None:
                        param = parameter
                        break

                self._exp_parameter.set_parameter(param)
            for index in range(len(self._leds)):
                self._leds[index].send_value(int(index == self._bank) * 7, True)

    def on_enabled_changed(self):
        if self.is_enabled():
            self.update()

    def set_select_buttons(self, matrix):
        self._select_buttons = matrix
        self._on_select_value.subject = matrix

    def set_doublepress_select_buttons(self, matrix):
        self._doublepress_select_buttons = matrix
        self._on_doublepress_select_value.subject = matrix

    def set_toggle1_button(self, button):
        self._toggle1_button = button
        self.on_toggle1_value.subject = button

    def set_toggle2_button(self, button):
        self._toggle2_button = button
        self.on_toggle2_value.subject = button

    def set_toggle3_button(self, button):
        self._toggle3_button = button
        self.on_toggle3_value.subject = button

    def set_expression_pedal(self, pedal):
        self._expression_pedal = pedal
        self._on_expression_value.subject = pedal

    @subject_slot('value')
    def _on_select_value(self, value, x, y, is_momentary):
        buttons = self._on_select_value.subject
        button = self._on_select_value.subject.get_button(x, y)
        if value:
            self._select_buttons_pressed.append(button)
            if buttons[1] in self._select_buttons_pressed and buttons[2] in self._select_buttons_pressed:
                self._select_buttons_pressed.remove(buttons[1])
                self._select_buttons_pressed.remove(buttons[2])
            if buttons[0] in self._select_buttons_pressed and buttons[1] in self._select_buttons_pressed:
                self._select_buttons_pressed.remove(buttons[0])
                self._select_buttons_pressed.remove(buttons[1])
            if buttons[2] in self._select_buttons_pressed and buttons[3] in self._select_buttons_pressed:
                self._select_buttons_pressed.remove(buttons[2])
                self._select_buttons_pressed.remove(buttons[3])
        elif button in self._select_buttons_pressed:
            self._select_buttons_pressed.remove(button)
            self.set_bank(x)

    @subject_slot('value')
    def _on_doublepress_select_value(self, value, x, y, is_momentary):
        self._script.toggle_device_control(x)

    @subject_slot('value')
    def on_toggle1_value(self, value):
        if value:
            self._parameters[0].toggle()

    @subject_slot('value')
    def on_toggle2_value(self, value):
        if value:
            self._parameters[1].toggle()

    @subject_slot('value')
    def on_toggle3_value(self, value):
        if value:
            self._parameters[2].toggle()

    @subject_slot('value')
    def _on_expression_value(self, value):
        self._exp_parameter.set_value(value)

    def enumerate_track_device(self, track):
        devices = []
        if hasattr(track, 'devices'):
            for device in track.devices:
                devices.append(device)
                if device.can_have_chains:
                    for chain in device.chains:
                        for chain_device in self.enumerate_track_device(chain):
                            devices.append(chain_device)

        return devices

    def set_bank(self, val):
        self._bank = val
        self.update()


class MonoPedal(ControlSurface):

    def __init__(self, *a, **k):
        super(MonoPedal, self).__init__(*a, **k)
        self._monomod_version = 'b995'
        self._codec_version = 'b996'
        self._cntrlr_version = 'b996'
        self._cntrlr = None
        self._host_name = 'MonoPedal'
        self._color_type = 'OhmRGB'
        self.hosts = []
        self._timer = 0
        self.flash_status = 1
        self._touched = 0
        self._last_main_mode = 'looper'
        with self.component_guard():
            self._setup_monobridge()
            self._setup_controls()
            self._setup_looper()
            self._setup_launcher()
            self._setup_device_control()
            self._setup_modes()
        self.schedule_message(1, self._open_log)

    def _open_log(self):
        self.log_message('<<<<<<<<<<<<<<<<<<<<= ' + str(self._host_name) + ' ' + str(self._monomod_version) + ' log opened =>>>>>>>>>>>>>>>>>>>')
        self.show_message(str(self._host_name) + ' Control Surface Loaded')

    def _setup_monobridge(self):
        self._monobridge = MonoBridgeElement(self)
        self._monobridge.name = 'MonoBridge'

    def _setup_controls(self):
        self._pedal = [ None for index in range(8) ]
        for index in range(7):
            self._pedal[index] = DoublePressElement(MonoButtonElement(True, MIDI_CC_TYPE, 0, PEDAL_DEFS[index], 'Pedal_' + str(index), self))
            self._pedal[index].name = 'Pedal_' + str(index)
            self._pedal[index]._report = False

        self._pedal[7] = LoopPedalExpressionElement(self, MIDI_CC_TYPE, 0, 1, Live.MidiMap.MapMode.absolute)
        self._pedal[7].name = 'Pedal_' + str(7)
        self._pedal[7]._report = False
        self._leds = [ None for index in range(4) ]
        for index in range(4):
            red_led = ButtonElement(True, MIDI_NOTE_TYPE, 0, LED_DEFS[index])
            green_led = ButtonElement(True, MIDI_NOTE_TYPE, 0, LED_DEFS[index] + 4)
            blue_led = ButtonElement(True, MIDI_NOTE_TYPE, 0, LED_DEFS[index] + 8)
            self._leds[index] = RGB_LED(red_led, green_led, blue_led, True, MIDI_NOTE_TYPE, 0, index + 13, 'LED_' + str(index), self)

        self._select_buttons = ButtonMatrixElement()
        self._select_buttons.name = 'SelectMatrix'
        self._select_buttons.add_row([self._pedal[6],
         self._pedal[5],
         self._pedal[4],
         self._pedal[3]])
        self._doublepress_select_buttons = ButtonMatrixElement()
        self._doublepress_select_buttons.name = 'DoublepressSelectMatrix'
        self._doublepress_select_buttons.add_row([self._pedal[6].double_press,
         self._pedal[5].double_press,
         self._pedal[4].double_press,
         self._pedal[3].double_press])
        self._record_button = self._pedal[1]
        self._mute_button = self._pedal[2]
        self._overdub_button = self._pedal[0]

    def _setup_looper(self):
        self._looper = MonolooperComponent(self._leds, self)
        self._looper.layer = Layer(select_buttons=self._select_buttons, doublepress_select_buttons=self._doublepress_select_buttons, overdub_button=self._pedal[2], record_button=self._pedal[1], mute_button=self._pedal[0], expression_pedal=self._pedal[7])

    def _setup_launcher(self):
        self._launcher = LauncherComponent(self._leds, self)
        self._launcher.set_enabled(False)
        self._launcher.layer = Layer(select_buttons=self._select_buttons, doublepress_select_buttons=self._doublepress_select_buttons, fire1_button=self._pedal[2], fire2_button=self._pedal[1], fire3_button=self._pedal[0], expression_pedal=self._pedal[7])

    def _setup_device_control(self):
        self._device_control = DeviceControlComponent(self._leds, self)
        self._device_control.set_enabled(False)
        self._device_control.layer = Layer(select_buttons=self._select_buttons, doublepress_select_buttons=self._doublepress_select_buttons, toggle1_button=self._pedal[2], toggle2_button=self._pedal[1], toggle3_button=self._pedal[0], expression_pedal=self._pedal[7])

    def _setup_modes(self):
        self._button_modes = ModesComponent(name='Button_Modes')
        self._button_modes.add_mode('launcher', self._launcher)
        self._button_modes.add_mode('looper', self._looper)
        self._button_modes.add_mode('device', self._device_control)
        self._button_modes.selected_mode = 'device'
        self._button_modes.set_enabled(True)

    def receive_led(self, button, value):
        pass

    def toggle_mode(self):
        self._button_modes.selected_mode = 'launcher' if self._button_modes.selected_mode is 'looper' else 'looper'
        self._last_main_mode = self._button_modes.selected_mode

    def toggle_device_control(self, x):
        self._button_modes.selected_mode = 'device' if self._button_modes.selected_mode is not 'device' else self._last_main_mode
        if self._button_modes.selected_mode is 'device':
            self._device_control.set_bank(x)

    def update_display(self):
        super(MonoPedal, self).update_display()
        self._timer = (self._timer + 1) % 256
        self.flash()

    def flash(self):
        if self.flash_status > 0:
            for control in self.controls:
                if isinstance(control, MonoButtonElement):
                    control.flash(self._timer)