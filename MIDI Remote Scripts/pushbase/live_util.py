
from __future__ import absolute_import, print_function

def get_position_for_new_track(song, selected_track_index):
    """
    Returns the index for a new track. The track will always be added to the
    right of the selected track. If a group track is selected, it will be added
    after the group.
    """
    if not -1 <= selected_track_index < len(song.tracks):
        raise IndexError('Index %i needs to be in [-1..%i]' % (selected_track_index, len(song.tracks)))
    if selected_track_index == -1:
        index = -1
    else:
        index = selected_track_index + 1
        if song.tracks[selected_track_index].is_foldable:
            while index < len(song.tracks) and song.tracks[index].is_grouped:
                index += 1

    return index