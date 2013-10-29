#Embedded file name: /Applications/Ableton Live 9.05 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Tweaker/DetailViewControllerComponent.py
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ControlSurface import ControlSurface
SHOW_PLAYING_CLIP_DELAY = 5

class DetailViewControllerComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Component that can toggle the device chain- and clip view of the selected track '

    def __init__(self, script, channelstrip):
        ControlSurfaceComponent.__init__(self)
        self._script = script
        self._channelstrip = channelstrip
        self._device_clip_toggle_button = None
        self._detail_toggle_button = None
        self._left_button = None
        self._right_button = None
        self._shift_button = None
        self._shift_pressed = False
        self._show_playing_clip_ticks_delay = -1
        self.application().view.add_is_view_visible_listener('Detail', self._detail_view_visibility_changed)
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        self.application().view.remove_is_view_visible_listener('Detail', self._detail_view_visibility_changed)
        if self._device_clip_toggle_button != None:
            self._device_clip_toggle_button.remove_value_listener(self._device_clip_toggle_value)
            self._device_clip_toggle_button = None
        if self._detail_toggle_button != None:
            self._detail_toggle_button.remove_value_listener(self._detail_toggle_value)
            self._detail_toggle_button = None
        if self._left_button != None:
            self._left_button.remove_value_listener(self._nav_value)
            self._left_button = None
        if self._right_button != None:
            self._right_button.remove_value_listener(self._nav_value)
            self._right_button = None
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None

    def set_device_clip_toggle_button(self, button):
        if not button == None:
            if not isinstance(button, ButtonElement):
                isinstance(button, ButtonElement)
                raise AssertionError
            if self._device_clip_toggle_button != button:
                if self._device_clip_toggle_button != None:
                    self._device_clip_toggle_button.remove_value_listener(self._device_clip_toggle_value)
                self._device_clip_toggle_button = button
                self._device_clip_toggle_button != None and self._device_clip_toggle_button.add_value_listener(self._device_clip_toggle_value)
            self._rebuild_callback()
            self.update()

    def set_detail_toggle_button(self, button):
        if not button == None:
            if not isinstance(button, ButtonElement):
                isinstance(button, ButtonElement)
                raise AssertionError
            if self._detail_toggle_button != button:
                if self._detail_toggle_button != None:
                    self._detail_toggle_button.remove_value_listener(self._detail_toggle_value)
                self._detail_toggle_button = button
                self._detail_toggle_button != None and self._detail_toggle_button.add_value_listener(self._detail_toggle_value)
            self._rebuild_callback()
            self.update()

    def set_device_nav_buttons(self, left_button, right_button):
        if not left_button == None:
            if not isinstance(left_button, ButtonElement):
                isinstance(left_button, ButtonElement)
                raise AssertionError
            if not right_button == None:
                if not isinstance(right_button, ButtonElement):
                    isinstance(right_button, ButtonElement)
                    raise AssertionError
                identify_sender = True
                if self._left_button != None:
                    self._left_button.remove_value_listener(self._nav_value)
                self._left_button = left_button
                if self._left_button != None:
                    self._left_button.add_value_listener(self._nav_value, identify_sender)
                self._right_button != None and self._right_button.remove_value_listener(self._nav_value)
            self._right_button = right_button
            self._right_button != None and self._right_button.add_value_listener(self._nav_value, identify_sender)
        self.update()

    def set_shift_button(self, button):
        if not button == None:
            if isinstance(button, ButtonElement):
                if not button.is_momentary():
                    isinstance(button, ButtonElement)
                    raise AssertionError
                if self._shift_button != button:
                    self._shift_button != None and self._shift_button.remove_value_listener(self._shift_value)
                self._shift_button = button
                self._shift_button != None and self._shift_button.add_value_listener(self._shift_value)
            self._rebuild_callback()
            self.update()

    def on_enabled_changed(self):
        self.update()

    def update(self):
        if self.is_enabled():
            self.is_enabled()
            if not self._shift_pressed:
                self._shift_pressed
                if self._left_button != None:
                    self._left_button.turn_off()
                if self._right_button != None:
                    self._right_button.turn_off()
                if self._device_clip_toggle_button != None:
                    self._device_clip_toggle_button.turn_off()
                self._detail_view_visibility_changed()
            else:
                self._shift_pressed
        else:
            self.is_enabled()

    def _detail_view_visibility_changed(self):
        if self.is_enabled() and not self._shift_pressed and self._detail_toggle_button != None:
            if self.application().view.is_view_visible('Detail'):
                self.application().view.is_view_visible('Detail')
                self._detail_toggle_button.turn_on()
            else:
                self.application().view.is_view_visible('Detail')
                self._detail_toggle_button.turn_off()
        else:
            self.is_enabled()

    def _device_clip_toggle_value(self, value):
        if not self._device_clip_toggle_button != None:
            raise AssertionError
        if value not in range(128):
            raise AssertionError
        if self.is_enabled() and not self._shift_pressed:
            not self._shift_pressed
            button_is_momentary = self._device_clip_toggle_button.is_momentary()
            if not button_is_momentary or value != 0:
                not button_is_momentary
                if not self.application().view.is_view_visible('Detail'):
                    self.application().view.is_view_visible('Detail')
                    self.application().view.show_view('Detail')
                else:
                    self.application().view.is_view_visible('Detail')
                if not self.application().view.is_view_visible('Detail/DeviceChain'):
                    self.application().view.is_view_visible('Detail/DeviceChain')
                    self.application().view.show_view('Detail/DeviceChain')
                else:
                    self.application().view.is_view_visible('Detail/DeviceChain')
                    self.application().view.show_view('Detail/Clip')
            if button_is_momentary and value != 0:
                self._show_playing_clip_ticks_delay = SHOW_PLAYING_CLIP_DELAY
            else:
                button_is_momentary
                self._show_playing_clip_ticks_delay = -1
        else:
            self.is_enabled()

    def _detail_toggle_value(self, value):
        if not self._detail_toggle_button != None:
            raise AssertionError
            if not value in range(128):
                raise AssertionError
                if self.is_enabled() and not self._shift_pressed:
                    (not self._detail_toggle_button.is_momentary() or value != 0) and (self.application().view.is_view_visible('Detail') or self.application().view.show_view('Detail'))
                else:
                    self.application().view.hide_view('Detail')

    def _shift_value(self, value):
        if not self._shift_button != None:
            raise AssertionError
        if value not in range(128):
            raise AssertionError
        self._shift_pressed = value != 0
        self.update()

    def _nav_value(self, value, sender):
        if not (sender != None and sender in (self._left_button, self._right_button)):
            raise AssertionError
            if self.is_enabled() and not self._shift_pressed and value > 0:
                track = self._channelstrip._track
                selected_device = self._channelstrip._device_component._device
                if selected_device == None and len(track.devices) > 0:
                    selected_device = track.devices[0]
                device_number = -1
                for index in range(len(track.devices)):
                    if track.devices[index] == selected_device:
                        device_number = index
                        break

                if device_number > -1:
                    if sender == self._right_button:
                        device_number += 1
                    elif sender == self._left_button:
                        device_number -= 1
                    device_number in range(len(track.devices)) and self._channelstrip._device_component.set_device(track.devices[device_number])
                    self._channelstrip._device_component._on_on_off_changed()
                    self.song().view.select_device(track.devices[device_number])

    def _on_timer(self):
        if self.is_enabled() and not self._shift_pressed:
            if self._show_playing_clip_ticks_delay > -1:
                if self._show_playing_clip_ticks_delay == 0:
                    song = self.song()
                    playing_slot_index = song.view.selected_track.playing_slot_index
                    if playing_slot_index > -1:
                        song.view.selected_scene = song.scenes[playing_slot_index]
                        if song.view.highlighted_clip_slot.has_clip:
                            self.application().view.show_view('Detail/Clip')
                self._show_playing_clip_ticks_delay -= 1