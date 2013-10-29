#Embedded file name: /Users/versonator/Jenkins/live/Projects/AppLive/Resources/MIDI Remote Scripts/Launch_Control/SpecialSessionComponent.py
from _Framework.SessionComponent import SessionComponent

class SpecialSessionComponent(SessionComponent):

    def set_clip_launch_buttons(self, buttons):
        for i, button in map(None, xrange(self._num_tracks), buttons or []):
            scene = self.selected_scene()
            slot = scene.clip_slot(i)
            slot.set_launch_button(button)

    def _update_select_buttons(self):
        selected_scene = self.song().view.selected_scene
        if self._next_scene_button != None:
            self._next_scene_button.set_light(selected_scene != self.song().scenes[-1])
        if self._prev_scene_button != None:
            self._prev_scene_button.set_light(selected_scene != self.song().scenes[0])