
from _APC.MixerComponent import MixerComponent as MixerComponentBase
from _APC.MixerComponent import ChanStripComponent as ChanStripComponentBase

class ChanStripComponent(ChanStripComponentBase):

    def set_select_button(self, button):
        if self._select_button != None:
            self._select_button.remove_value_listener(self._select_value)
            self._select_button = None
        super(ChanStripComponent, self).set_select_button(button)

    def set_mute_button(self, button):
        if self._mute_button != None:
            self._mute_button.remove_value_listener(self._mute_value)
            self._mute_button = None
        super(ChanStripComponent, self).set_mute_button(button)

    def set_solo_button(self, button):
        if self._solo_button != None:
            self._solo_button.remove_value_listener(self._solo_value)
            self._solo_button = None
        super(ChanStripComponent, self).set_solo_button(button)

    def set_arm_button(self, button):
        if self._arm_button != None:
            self._arm_button.remove_value_listener(self._arm_value)
            self._arm_button = None
        super(ChanStripComponent, self).set_arm_button(button)


class MixerComponent(MixerComponentBase):

    def on_num_sends_changed(self):
        if self.send_index is None and self.num_sends > 0:
            self.send_index = 0

    def _create_strip(self):
        return ChanStripComponent()