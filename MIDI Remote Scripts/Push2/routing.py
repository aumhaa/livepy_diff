
from __future__ import absolute_import, print_function
from functools import partial
import Live
from ableton.v2.base import listenable_property, listens, EventObject, MultiSlot
from ableton.v2.base.util import index_if
from ableton.v2.control_surface.mode import ModesComponent, SetAttributeMode
from ableton.v2.control_surface.control import control_list, ListValueEncoderControl
from pushbase.song_utils import is_return_track
from .mixable_utilities import is_chain
MASTER_OUTPUT_TARGET_ID = u'Master'
NO_INPUT_TARGET_ID = u'No Input'

class TrackOrRoutingControlChooserComponent(ModesComponent):

    def __init__(self, tracks_provider = None, track_mixer_component = None, routing_control_component = None, *a, **k):
        super(TrackOrRoutingControlChooserComponent, self).__init__(*a, **k)
        self._tracks_provider = tracks_provider
        self._track_mixer = track_mixer_component
        self._routing_control = routing_control_component
        self.add_mode('mix', track_mixer_component)
        self.add_mode('routing', routing_control_component)
        self.selected_mode = 'mix'
        for mode in ['mix', 'routing']:
            button = self.get_mode_button(mode)
            button.mode_selected_color = 'MixOrRoutingChooser.ModeActive'
            button.mode_unselected_color = 'MixOrRoutingChooser.ModeInactive'

        self._routing_previously_available = False
        self._update_buttons(False)
        self.__on_selected_item_changed.subject = self._tracks_provider
        self.__on_selected_item_changed()

    @property
    def track_mix(self):
        return self._track_mixer

    @property
    def routing(self):
        return self._routing_control

    @listenable_property
    def routing_mode_available(self):
        return self._can_enable_routing_mode()

    def update(self):
        super(TrackOrRoutingControlChooserComponent, self).update()
        if self.is_enabled():
            self._update_routing_mode_availability()

    @listens('selected_item')
    def __on_selected_item_changed(self):
        if self.is_enabled():
            self._update_routing_mode_availability()

    def _update_routing_mode_availability(self):
        is_available = self._can_enable_routing_mode()
        if is_available != self._routing_previously_available:
            self._update_buttons(enable_buttons=is_available)
            if is_available and 'routing' in self.active_modes:
                self.pop_mode('mix')
            else:
                self.push_mode('mix')
            self.notify_routing_mode_available()
            self._routing_previously_available = is_available

    def _can_enable_routing_mode(self):
        return not is_chain(self._tracks_provider.selected_item) and Live.Application.get_application().has_option('_Push2RoutingSettings')

    def _update_buttons(self, enable_buttons):
        for mode in ['mix', 'routing']:
            self.get_mode_button(mode).enabled = enable_buttons


def reorder_routing_targets(targets, desired_first_target_display_name):
    targets = list(targets)
    index_of_desired_first_target = None
    index_of_desired_first_target = index_if(lambda target: target.display_name == desired_first_target_display_name, targets)
    if index_of_desired_first_target >= 0 and index_of_desired_first_target < len(targets):
        return [targets[index_of_desired_first_target]] + targets[:index_of_desired_first_target] + targets[index_of_desired_first_target + 1:]
    else:
        return targets


class Router(EventObject):
    current_target_index = listenable_property.managed(-1)

    def __init__(self, routing_level = None, routing_direction = None, song = None, *a, **k):
        raise song is not None or AssertionError
        raise routing_level is not None or AssertionError
        raise routing_direction is not None or AssertionError
        super(Router, self).__init__(*a, **k)
        self._song = song
        self._current_target_property = '%s_routing_%s' % (routing_direction, routing_level)
        self.register_slot(MultiSlot(subject=song.view, event_name_list=('selected_track', self._current_target_property), listener=self.__on_current_routing_changed))
        self.register_slot(MultiSlot(subject=song.view, event_name_list=('selected_track', 'available_%s_routing_%ss' % (routing_direction, routing_level)), listener=self.__on_routings_changed))
        self.current_target_index = self._current_target_index()

    @listenable_property
    def routing_targets(self):
        return self._get_targets()

    def _current_target_index(self):
        try:
            return self._get_targets().index(self._get_current_target())
        except ValueError:
            return -1

    @property
    def current_target(self):
        return self._get_current_target()

    @current_target.setter
    def current_target(self, new_target):
        self._set_current_target(new_target)

    def __on_current_routing_changed(self):
        self.current_target_index = self._current_target_index()

    def __on_routings_changed(self):
        self.notify_routing_targets()

    def _track(self):
        return self._song.view.selected_track

    def _get_targets(self):
        raise NotImplementedError

    def _get_current_target(self):
        return getattr(self._track(), self._current_target_property)

    def _set_current_target(self, new_target_id):
        setattr(self._track(), self._current_target_property, new_target_id)


class InputTypeRouter(Router):

    def __init__(self, *a, **k):
        super(InputTypeRouter, self).__init__(routing_direction='input', routing_level='type', *a, **k)

    def _get_targets(self):
        return reorder_routing_targets(self._track().available_input_routing_types, NO_INPUT_TARGET_ID)


class OutputTypeRouter(Router):

    def __init__(self, *a, **k):
        super(OutputTypeRouter, self).__init__(routing_direction='output', routing_level='type', *a, **k)

    def _get_targets(self):
        return reorder_routing_targets(self._track().available_output_routing_types, MASTER_OUTPUT_TARGET_ID)


class InputChannelRouter(Router):

    def __init__(self, *a, **k):
        super(InputChannelRouter, self).__init__(routing_direction='input', routing_level='channel', *a, **k)

    def _get_targets(self):
        return list(self._track().available_input_routing_channels)


class OutputChannelRouter(Router):

    def __init__(self, *a, **k):
        super(OutputChannelRouter, self).__init__(routing_direction='output', routing_level='channel', *a, **k)

    def _get_targets(self):
        return list(self._track().available_output_routing_channels)


class RoutingTargetList(EventObject):

    def __init__(self, router = None, *a, **k):
        super(RoutingTargetList, self).__init__(*a, **k)
        self._router = router
        self.__on_current_target_index_changed.subject = router
        self.__on_routing_targets_changed.subject = router

    @listenable_property
    def targets(self):
        return [ target.display_name for target in self._router.routing_targets ]

    @listenable_property
    def selected_index(self):
        return self._router.current_target_index

    @listens('routing_targets')
    def __on_routing_targets_changed(self):
        self.notify_targets()

    @listens('current_target_index')
    def __on_current_target_index_changed(self, _):
        self.notify_selected_index()


def can_set_input_routing(track, song):
    return track.has_audio_input and not is_return_track(song, track)


def can_set_output_routing(track, _):
    return track.has_audio_output


class RoutingControlComponent(ModesComponent):
    monitor_state_encoder = ListValueEncoderControl(num_steps=10)
    input_output_choice_encoder = ListValueEncoderControl(num_steps=10)
    routing_target_encoder = ListValueEncoderControl(num_steps=10)
    routing_sub_target_encoders = control_list(ListValueEncoderControl, control_count=4, num_steps=10)
    can_route = listenable_property.managed(False)

    def __init__(self, *a, **k):
        super(RoutingControlComponent, self).__init__(*a, **k)
        self.__on_current_monitoring_state_changed.subject = self.song.view
        self.__on_has_audio_input_changed.subject = self.song.view
        self.__on_has_audio_output_changed.subject = self.song.view
        input_type_router, output_type_router, input_channel_router, output_channel_router = self.register_disconnectables([InputTypeRouter(song=self.song),
         OutputTypeRouter(song=self.song),
         InputChannelRouter(song=self.song),
         OutputChannelRouter(song=self.song)])
        self._active_type_router = input_type_router
        self._active_channel_router = input_channel_router
        self._can_route = can_set_input_routing
        self._update_can_route()
        self._routing_type_list, self._routing_channel_list = self.register_disconnectables([RoutingTargetList(self._active_type_router), RoutingTargetList(self._active_channel_router)])
        self.add_mode('input', [partial(self._set_active_routers, input_type_router, input_channel_router), SetAttributeMode(self, '_can_route', can_set_input_routing)])
        self.add_mode('output', [partial(self._set_active_routers, output_type_router, output_channel_router), SetAttributeMode(self, '_can_route', can_set_output_routing)])
        self.selected_mode = 'input'
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()
        self._connect_monitoring_state_encoder()
        self.input_output_choice_encoder.connect_static_list(self, 'selected_mode', list_values=['input', 'output'])
        self.__on_selected_mode_changed.subject = self

    @listenable_property
    def can_monitor(self):
        return hasattr(self.song.view.selected_track, 'current_monitoring_state')

    @listenable_property
    def monitoring_state_index(self):
        if self.can_monitor:
            return self.song.view.selected_track.current_monitoring_state

    @listenable_property
    def is_choosing_output(self):
        return self.selected_mode == 'output'

    @listenable_property
    def routing_type_list(self):
        return self._routing_type_list

    @listenable_property
    def routing_channel_list(self):
        return self._routing_channel_list

    @listens('selected_mode')
    def __on_selected_mode_changed(self, _):
        self.notify_is_choosing_output()
        self._update_can_route()

    @listens('selected_track.current_monitoring_state')
    def __on_current_monitoring_state_changed(self):
        self.notify_monitoring_state_index()

    @listens('selected_track.has_audio_input')
    def __on_has_audio_input_changed(self):
        self._update_can_route()

    @listens('selected_track.has_audio_output')
    def __on_has_audio_output_changed(self):
        self._update_can_route()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._connect_monitoring_state_encoder()
        self.notify_can_monitor()
        self._update_routing_type_list()
        self._update_routing_channel_list()

    @listens('current_target_index')
    def __on_selected_target_changed(self, _):
        self._update_routing_channel_list()

    def _update_can_route(self):
        track = self.song.view.selected_track
        self.can_route = self._can_route(track, self.song) and track != self.song.master_track
        self.routing_target_encoder.enabled = self.can_route

    def _set_active_routers(self, type_router, channel_router):
        self._active_type_router = type_router
        self._active_channel_router = channel_router
        self._update_routing_type_list()
        self._update_routing_channel_list()
        self.routing_target_encoder.connect_list_property(self._active_type_router, current_value_property_name='current_target', list_property_name='routing_targets')
        for encoder in self.routing_sub_target_encoders:
            encoder.connect_list_property(self._active_channel_router, current_value_property_name='current_target', list_property_name='routing_targets')

        self.__on_selected_target_changed.subject = type_router

    def _update_routing_type_list(self):
        self.unregister_disconnectable(self._routing_type_list)
        self._routing_type_list.disconnect()
        self._routing_type_list = self.register_disconnectable(RoutingTargetList(self._active_type_router))
        self.notify_routing_type_list()

    def _update_routing_channel_list(self):
        self.unregister_disconnectable(self._routing_channel_list)
        self._routing_channel_list.disconnect()
        self._routing_channel_list = self.register_disconnectable(RoutingTargetList(self._active_channel_router))
        self.notify_routing_channel_list()

    def _connect_monitoring_state_encoder(self):
        if self.can_monitor:
            self.monitor_state_encoder.connect_static_list(self.song.view.selected_track, 'current_monitoring_state', list_values=[Live.Track.Track.monitoring_states.IN, Live.Track.Track.monitoring_states.AUTO, Live.Track.Track.monitoring_states.OFF])
        else:
            self.monitor_state_encoder.disconnect_property()