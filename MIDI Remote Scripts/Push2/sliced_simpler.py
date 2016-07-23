
from __future__ import absolute_import, print_function
from pushbase.colors import Pulse
from pushbase.sliced_simpler_component import SlicedSimplerComponent
from .colors import determine_shaded_color_index, IndexedColor, translate_color_index
NEXT_SLICE_PULSE_SPEED = 48

def make_shaded_color_from_index(color_index, shade_level):
    return IndexedColor(determine_shaded_color_index(translate_color_index(color_index), shade_level))


def next_slice_color(track_color_index):
    return Pulse(color1=make_shaded_color_from_index(track_color_index, 2), color2=make_shaded_color_from_index(track_color_index, 1), speed=NEXT_SLICE_PULSE_SPEED)


class Push2SlicedSimplerComponent(SlicedSimplerComponent):

    def _next_slice_color(self):
        return next_slice_color(self.song.view.selected_track.color_index)