
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import BasicSceneScroller, ScrollComponent, ViewControlComponent as ViewControlComponentBase
from ableton.v2.control_surface.control import StepEncoderControl

class ViewControlComponent(ViewControlComponentBase):
    scene_scroll_encoder = StepEncoderControl(num_steps=64)

    def __init__(self, *a, **k):
        super(ViewControlComponent, self).__init__(*a, **k)
        self._scroll_scenes = self.register_component(ScrollComponent(BasicSceneScroller()))

    @scene_scroll_encoder.value
    def scene_scroll_encoder(self, value, _):
        if value > 0:
            self._scroll_scenes.scroll_down()
        elif value < 0:
            self._scroll_scenes.scroll_up()