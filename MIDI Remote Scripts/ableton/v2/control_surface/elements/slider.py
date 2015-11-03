
from __future__ import absolute_import
import Live
from ..input_control_element import MIDI_NOTE_TYPE
from .encoder import EncoderElement

class SliderElement(EncoderElement):
    """ Class representing a slider on the controller """

    def __init__(self, msg_type, channel, identifier, *a, **k):
        raise msg_type is not MIDI_NOTE_TYPE or AssertionError
        super(SliderElement, self).__init__(msg_type, channel, identifier, map_mode=Live.MidiMap.MapMode.absolute, *a, **k)