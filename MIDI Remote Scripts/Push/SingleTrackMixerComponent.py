#Embedded file name: /Users/versonator/Jenkins/live/Projects/AppLive/Resources/MIDI Remote Scripts/Push/SingleTrackMixerComponent.py
from itertools import izip
from _Framework.SubjectSlot import subject_slot
from DeviceParameterComponent import DeviceParameterComponent
from SpecialChanStripComponent import TRACK_PARAMETER_NAMES

class SingleTrackMixerComponent(DeviceParameterComponent):

    def __init__(self, *a, **k):
        super(SingleTrackMixerComponent, self).__init__(*a, **k)
        self._track = None
        self._encoders = []
        self._on_visible_tracks.subject = self.song()

    def _get_track(self):
        return self._track

    def _set_track(self, track):
        self._track = track
        self._update_parameters()

    track = property(_get_track, _set_track)

    @property
    def parameters(self):
        if self._track:
            return [self._track.mixer_device.volume, self._track.mixer_device.panning] + list(self._track.mixer_device.sends)
        return []

    def get_parameter_name(self, parameter, index):
        if 0 <= index < len(TRACK_PARAMETER_NAMES):
            return TRACK_PARAMETER_NAMES[index]
        return parameter.name if parameter else ''

    def set_encoders(self, encoders):
        self._release_parameters()
        self._encoders = encoders or []
        self._connect_parameters()

    def _update_parameters(self):
        super(SingleTrackMixerComponent, self)._update_parameters()
        self._connect_parameters()

    def _release_parameters(self):
        for encoder in self._encoders or []:
            encoder.release_parameter()

    def _connect_parameters(self):
        for parameter, encoder in izip(self.parameters, self._encoders or []):
            encoder.connect_to(parameter)

    @subject_slot('visible_tracks')
    def _on_visible_tracks(self):
        self._update_parameters()

    def update(self):
        pass


class SelectedTrackMixerComponent(SingleTrackMixerComponent):

    def __init__(self, *a, **k):
        super(SelectedTrackMixerComponent, self).__init__(*a, **k)
        self._update_selected_track()
        self._on_selected_track.subject = self.song().view

    @subject_slot('selected_track')
    def _on_selected_track(self):
        if self.is_enabled():
            self._update_selected_track()

    def _update_selected_track(self):
        self.track = self.song().view.selected_track

    def update(self):
        super(SelectedTrackMixerComponent, self).update()
        if self.is_enabled():
            self._update_selected_track()