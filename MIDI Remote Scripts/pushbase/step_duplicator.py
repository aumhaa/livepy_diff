from __future__ import absolute_import, print_function
from functools import partial
from ableton.v2.base import liveobj_valid, nop
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl
from .consts import MessageBoxText
from .message_box_component import Messenger

class StepDuplicatorComponent(Component, Messenger):
    button = ButtonControl()

    def __init__(self, *a, **k):
        super(StepDuplicatorComponent, self).__init__(*a, **k)
        self._clip = None
        self._source_step = None
        self._notification_reference = partial(nop, None)

    @property
    def is_duplicating(self):
        return self.button.is_pressed and liveobj_valid(self._clip)

    def set_clip(self, clip):
        self._cancel_duplicate()
        self._clip = clip

    def add_step(self, note, step_start, step_end, nudge_offset = 0):
        if self.is_enabled() and self.is_duplicating:
            current_step = (note,
             step_start,
             step_end - step_start,
             nudge_offset)
            if self._source_step is not None:
                self._duplicate_to(current_step)
            else:
                self._duplicate_from(current_step)

    def _duplicate_from(self, source_step):
        message = MessageBoxText.CANNOT_COPY_EMPTY_STEP
        notes = self._clip.get_notes(source_step[1], source_step[0], source_step[2], 1)
        if len(notes) > 0:
            message = MessageBoxText.COPIED_STEP
            self._source_step = source_step
        self._notification_reference = self.show_notification(message)

    def _duplicate_to(self, destination_step):
        message = MessageBoxText.CANNOT_PASTE_TO_SOURCE_STEP
        if destination_step != self._source_step:
            message = MessageBoxText.PASTED_STEP
            self._clip.duplicate_region(self._source_step[1], self._source_step[2], destination_step[1] + self._source_step[3], self._source_step[0], destination_step[0] - self._source_step[0])
        self._notification_reference = self.show_notification(message)
        self._source_step = None

    def _cancel_duplicate(self):
        self._source_step = None
        if self._notification_reference() is not None:
            self._notification_reference().hide()

    @button.released
    def button(self, _):
        self._cancel_duplicate()

    def update(self):
        super(StepDuplicatorComponent, self).update()
        self._cancel_duplicate()
