
from __future__ import absolute_import, print_function
from ableton.v2.control_surface.components import SessionNavigationComponent

class MixerNavigationComponent(SessionNavigationComponent):

    def _can_scroll_page_left(self):
        return True

    def _can_scroll_page_right(self):
        return True

    def _scroll_page_left(self):
        width = self._session_ring.num_tracks
        track_offset = self._session_ring.track_offset
        new_track_offset = track_offset - width
        if new_track_offset < 0:
            new_track_offset = (len(self._session_ring.tracks_to_use()) - 1) / width * width
        self._session_ring.set_offsets(new_track_offset, self._session_ring.scene_offset)

    def _scroll_page_right(self):
        new_track_offset = self._session_ring.track_offset + self._session_ring.num_tracks
        if new_track_offset >= len(self._session_ring.tracks_to_use()):
            new_track_offset = 0
        self._session_ring.set_offsets(new_track_offset, self._session_ring.scene_offset)