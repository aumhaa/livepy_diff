
from __future__ import absolute_import, print_function
from pushbase.note_editor_component import NoteEditorComponent

class Push2NoteEditorComponent(NoteEditorComponent):
    __events__ = ('mute_solo_stop_cancel_action_performed',)

    def _on_pad_pressed(self, value, x, y, is_momentary):
        super(Push2NoteEditorComponent, self)._on_pad_pressed(value, x, y, is_momentary)
        self.notify_mute_solo_stop_cancel_action_performed()