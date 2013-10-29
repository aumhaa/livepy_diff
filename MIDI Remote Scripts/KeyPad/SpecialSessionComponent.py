#Embedded file name: /Users/versonator/Jenkins/live/Projects/AppLive/Resources/MIDI Remote Scripts/KeyPad/SpecialSessionComponent.py
from _Framework.SessionComponent import SessionComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.ClipSlotComponent import ClipSlotComponent

class SpecialClipSlotComponent(ClipSlotComponent):

    def _do_launch_clip(self, value):
        button = self._launch_button_value_slot.subject
        object_to_launch = self._clip_slot
        if not value:
            launch_pressed = not button.is_momentary()
            if self.has_clip():
                object_to_launch = self._clip_slot.clip
            else:
                self._has_fired_slot = True
            if button.is_momentary():
                object_to_launch.set_fire_button_state(value != 0)
            elif launch_pressed:
                object_to_launch.fire()
            self.song().view.highlighted_clip_slot = launch_pressed and self.has_clip() and self.song().select_on_launch and self._clip_slot


class SpecialSceneComponent(SceneComponent):
    clip_slot_component_type = SpecialClipSlotComponent


class SpecialSessionComponent(SessionComponent):
    scene_component_type = SpecialSceneComponent

    def _update_select_buttons(self):
        selected_scene = self.song().view.selected_scene
        if self._next_scene_button != None:
            self._next_scene_button.set_light(selected_scene != self.song().scenes[-1])
        if self._prev_scene_button != None:
            self._prev_scene_button.set_light(selected_scene != self.song().scenes[0])