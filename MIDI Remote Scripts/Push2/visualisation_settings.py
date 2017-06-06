
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Component
from .colors import COLOR_INDEX_TO_SCREEN_COLOR, COLOR_INDEX_TO_SCREEN_COLOR_SHADES

class VisualisationSettingsComponent(Component):
    base_colors = COLOR_INDEX_TO_SCREEN_COLOR
    shade1_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[0]
    shade2_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[1]
    shade3_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[2]
    shade4_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[3]
    shade5_colors = COLOR_INDEX_TO_SCREEN_COLOR_SHADES[4]