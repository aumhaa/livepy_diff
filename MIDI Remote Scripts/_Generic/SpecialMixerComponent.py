
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.MixerComponent import MixerComponent
from .SelectChanStripComponent import SelectChanStripComponent

class SpecialMixerComponent(MixerComponent):
    u""" Class encompassing several selecting channel strips to form a mixer """

    def _create_strip(self):
        return SelectChanStripComponent()