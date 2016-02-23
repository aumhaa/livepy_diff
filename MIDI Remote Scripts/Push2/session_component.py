
from __future__ import absolute_import, print_function
import Live
from itertools import imap
from pushbase.colors import Blink, Pulse
from pushbase.special_session_component import ClipSlotCopyHandler, SpecialClipSlotComponent, SpecialSceneComponent, SpecialSessionComponent
from .clip_decoration import ClipDecoratedPropertiesCopier
from .colors import determine_shaded_color_index, IndexedColor, translate_color_index, WHITE_COLOR_INDEX_FROM_LIVE, WHITE_MIDI_VALUE
from .skin_default import CLIP_PLAYING_COLOR, RECORDING_COLOR
PLAYING_CLIP_PULSE_SPEED = 48
TRIGGERED_CLIP_BLINK_SPEED = 24

class DecoratingCopyHandler(ClipSlotCopyHandler):

    def __init__(self, decorator_factory = None, *a, **k):
        raise decorator_factory is not None or AssertionError
        super(DecoratingCopyHandler, self).__init__(*a, **k)
        self._decorator_factory = decorator_factory

    def _on_duplicated(self, source_clip_slot, target_clip_slot):
        super(DecoratingCopyHandler, self)._on_duplicated(source_clip_slot, target_clip_slot)
        ClipDecoratedPropertiesCopier(source_clip=source_clip_slot.clip, destination_clip=target_clip_slot.clip, decorator_factory=self._decorator_factory).post_duplication_action()


class ClipSlotComponent(SpecialClipSlotComponent):
    _decorator_factory = None

    def _feedback_value(self, track, slot_or_clip):
        clip_color = self._color_value(slot_or_clip)
        if slot_or_clip.is_triggered and not slot_or_clip.will_record_on_start:
            if isinstance(slot_or_clip, Live.Clip.Clip):
                return Blink(color1=CLIP_PLAYING_COLOR, color2=IndexedColor(clip_color), speed=TRIGGERED_CLIP_BLINK_SPEED)
            return 'Session.EmptySlotTriggeredPlay'
        elif slot_or_clip.is_playing:
            animate_to_color = RECORDING_COLOR if slot_or_clip.is_recording else IndexedColor(clip_color)
            return Pulse(color1=IndexedColor(determine_shaded_color_index(clip_color, 2)), color2=animate_to_color, speed=PLAYING_CLIP_PULSE_SPEED)
        else:
            return super(ClipSlotComponent, self)._feedback_value(track, slot_or_clip)

    def _color_value(self, slot_or_clip):
        if slot_or_clip.color_index == WHITE_COLOR_INDEX_FROM_LIVE:
            return WHITE_MIDI_VALUE
        return translate_color_index(slot_or_clip.color_index)

    def _on_clip_duplicated(self, source_clip, destination_clip):
        super(ClipSlotComponent, self)._on_clip_duplicated(source_clip, destination_clip)
        if self._decorator_factory:
            ClipDecoratedPropertiesCopier(source_clip=source_clip, destination_clip=destination_clip, decorator_factory=self._decorator_factory).post_duplication_action()

    def set_decorator_factory(self, factory):
        self._decorator_factory = factory


class SceneComponent(SpecialSceneComponent):
    clip_slot_component_type = ClipSlotComponent

    def build_clip_slot_list(self):
        scene_index = list(self.song.scenes).index(self._scene)

        def slot_for_track(mixable):
            if not hasattr(mixable, 'clip_slots') or len(mixable.clip_slots) == 0:
                return None
            else:
                return mixable.clip_slots[scene_index]

        return imap(slot_for_track, self._session_ring.controlled_tracks())


class SessionComponent(SpecialSessionComponent):
    scene_component_type = SceneComponent