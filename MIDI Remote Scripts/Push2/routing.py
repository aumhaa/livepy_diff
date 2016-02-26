
from __future__ import absolute_import, print_function
import Live
from ableton.v2.base import clamp, listenable_property, listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.mode import ModesComponent
from ableton.v2.control_surface.control import StepEncoderControl
from .mixable_utilities import is_chain

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

        self._previous_selection_was_chain = None
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

    @listens('selected_item')
    def __on_selected_item_changed(self):
        chain_selected = is_chain(self._tracks_provider.selected_item)
        if chain_selected != self._previous_selection_was_chain:
            self._update_routing_mode_availability()
        self._previous_selection_was_chain = chain_selected

    def _update_routing_mode_availability(self):
        is_available = self._can_enable_routing_mode()
        self._update_buttons(enable_buttons=is_available)
        if is_available and 'routing' in self.active_modes:
            self.pop_mode('mix')
        else:
            self.push_mode('mix')
        self.notify_routing_mode_available()

    def _can_enable_routing_mode(self):
        return not is_chain(self._tracks_provider.selected_item) and Live.Application.get_application().has_option('_Push2RoutingSettings')

    def _update_buttons(self, enable_buttons):
        for mode in ['mix', 'routing']:
            self.get_mode_button(mode).enabled = enable_buttons


class RoutingControlComponent(Component):
    monitor_state_encoder = StepEncoderControl(num_steps=10)

    def __init__(self, *a, **k):
        super(RoutingControlComponent, self).__init__(*a, **k)
        self.__on_current_monitoring_state_changed.subject = self.song.view
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()

    @listenable_property
    def can_monitor(self):
        return hasattr(self.song.view.selected_track, 'current_monitoring_state')

    @monitor_state_encoder.value
    def monitor_state_encoder(self, value, encoder):
        if self.can_monitor:
            track = self.song.view.selected_track
            monitoring_state = track.current_monitoring_state
            track.current_monitoring_state = clamp(monitoring_state + value, Live.Track.Track.monitoring_states.IN, Live.Track.Track.monitoring_states.OFF)

    @listenable_property
    def monitoring_state_index(self):
        if self.can_monitor:
            return self.song.view.selected_track.current_monitoring_state

    @listens('selected_track.current_monitoring_state')
    def __on_current_monitoring_state_changed(self):
        self.notify_monitoring_state_index()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self.notify_can_monitor()