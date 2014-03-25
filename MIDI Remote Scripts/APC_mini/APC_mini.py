
from __future__ import with_statement
from _Framework.BackgroundComponent import BackgroundComponent
from _Framework.Layer import Layer
from _APC.ControlElementUtils import make_slider
from APC_Key_25.APC_Key_25 import APC_Key_25, MODE_PRIORITY

class APC_mini(APC_Key_25):
    SESSION_HEIGHT = 8
    HAS_TRANSPORT = False

    def __init__(self, *a, **k):
        super(APC_mini, self).__init__(*a, **k)
        with self.component_guard():
            self._unused_container = BackgroundComponent(layer=Layer(priority=MODE_PRIORITY, unused_buttons=self.wrap_matrix(self._unused_buttons)), is_enabled=False)

    def _make_stop_all_button(self):
        return self.make_shifted_button(self._scene_launch_buttons[7])

    def _create_controls(self):
        super(APC_mini, self)._create_controls()
        self._unused_buttons = map(self.make_shifted_button, self._scene_launch_buttons[5:7])
        self._master_volume_control = make_slider(0, 56, name='Master_Volume')

    def _create_mixer(self):
        mixer = super(APC_mini, self)._create_mixer()
        mixer.master_strip().layer = Layer(volume_control=self._master_volume_control)
        return mixer

    def _product_model_id_byte(self):
        return 40