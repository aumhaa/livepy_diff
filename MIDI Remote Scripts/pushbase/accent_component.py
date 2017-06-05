
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.mode import ModesComponent

class DummyFullVelocity(object):
    enabled = False


class AccentComponent(ModesComponent):

    def __init__(self, *a, **k):
        super(AccentComponent, self).__init__(*a, **k)
        self._full_velocity = None
        self.add_mode(u'disabled', None, u'Accent.Off')
        self.add_mode(u'enabled', (self._on_accent_on, self._on_accent_off), u'Accent.On')
        self.selected_mode = u'disabled'
        self.set_full_velocity(None)

    def set_full_velocity(self, full_velocity):
        full_velocity = full_velocity or DummyFullVelocity()
        if self._full_velocity != None:
            self._full_velocity.enabled = False
        self._full_velocity = full_velocity
        self._full_velocity.enabled = self.selected_mode == u'enabled'

    @property
    def activated(self):
        return self._full_velocity.enabled

    def _on_accent_off(self):
        self._full_velocity.enabled = False

    def _on_accent_on(self):
        self._full_velocity.enabled = True