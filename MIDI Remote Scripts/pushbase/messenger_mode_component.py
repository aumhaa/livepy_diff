
from __future__ import absolute_import, print_function
from ableton.v2.base import BooleanContext
from ableton.v2.control_surface.mode import ModesComponent
from .message_box_component import Messenger

class MessengerModesComponent(ModesComponent, Messenger):
    notify_when_enabled = False

    def __init__(self, *a, **k):
        super(MessengerModesComponent, self).__init__(*a, **k)
        self._mode_message_map = {}
        self._is_being_enabled = BooleanContext()

    def add_mode(self, name, mode_or_component, message = None, **k):
        super(MessengerModesComponent, self).add_mode(name, mode_or_component, **k)
        self._mode_message_map[name] = message

    def on_enabled_changed(self):
        with self._is_being_enabled():
            super(MessengerModesComponent, self).on_enabled_changed()

    def _do_enter_mode(self, name):
        super(MessengerModesComponent, self)._do_enter_mode(name)
        if not self._is_being_enabled or self.notify_when_enabled:
            message = self._mode_message_map.get(name, None)
            if message:
                self.show_notification(message)