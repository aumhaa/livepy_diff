import Live
from _Framework.SceneComponent import SceneComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from SpecialClipSlotComponent import SpecialClipSlotComponent

class SpecialSceneComponent(SceneComponent):

    def __init__(self, num_tracks, tracks_to_use_callback):
        SceneComponent.__init__(self, num_tracks, tracks_to_use_callback)
        self._index = -1
        self._serato_interface = None
        self._last_name_sent = None

    def disconnect(self):
        if self._scene != None:
            self._scene.remove_name_listener(self._on_name_changed)
            self._scene.remove_color_listener(self._on_color_changed)
        SceneComponent.disconnect(self)
        self._serato_interface = None

    def set_serato_interface(self, serato_interface):
        assert serato_interface != None
        self._serato_interface = serato_interface
        if self._scene != None:
            self._on_is_triggered_changed()
        self._on_name_changed()
        self._on_color_changed()

    def set_scene(self, scene):
        if self._scene != scene:
            if self._scene != None:
                self._scene.remove_name_listener(self._on_name_changed)
                self._scene.remove_color_listener(self._on_color_changed)
            SceneComponent.set_scene(self, scene)
            if self._scene != None:
                self._scene.add_name_listener(self._on_name_changed)
                self._scene.add_color_listener(self._on_color_changed)
            self._on_name_changed()
            self._on_color_changed()

    def set_index(self, index):
        assert index >= 0
        self._index = index
        for clip_index in range(len(self._clip_slots)):
            self._clip_slots[clip_index].set_indexes(self._index, clip_index)

        if self._scene != None:
            self._on_is_triggered_changed()
        self._on_name_changed()
        self._on_color_changed()

    def is_selected(self):
        return self._scene == self.song().view.selected_scene

    def _create_clip_slot(self):
        return SpecialClipSlotComponent()

    def _on_name_changed(self):
        if self._serato_interface != None and self._index > -1:
            name = ''
            if self._scene != None:
                name = self._scene.name
            if self._last_name_sent != name:
                self._serato_interface.PySCA_SetSceneLabel(self._index + 1, name)
                self._last_name_sent = name

    def _on_color_changed(self):
        if self._serato_interface != None and self._index > -1:
            value_to_send = 0
            if self._scene != None:
                value_to_send = self._scene.color
            self._serato_interface.PySCA_SetSceneColor(self._index + 1, value_to_send)
