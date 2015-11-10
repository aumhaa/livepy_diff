
from __future__ import absolute_import, print_function
import Live
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.mode import LazyComponentMode, Mode, ModeButtonBehaviour
from pushbase.browser_modes import BrowserHotswapMode

def get_filter_type_for_track(song):
    has_midi_support = song.view.selected_track.has_midi_input
    if has_midi_support:
        return Live.Browser.FilterType.midi_track_devices
    return Live.Browser.FilterType.audio_effect_hotswap


class BrowserModeBehaviour(ModeButtonBehaviour):

    def press_immediate(self, component, mode):
        if mode == component.selected_mode:
            component.selected_mode = component.active_modes[0]
        else:
            component.push_mode(mode)


class BrowserComponentMode(LazyComponentMode):

    def __init__(self, model_ref, *a, **k):
        super(BrowserComponentMode, self).__init__(*a, **k)
        self._model_ref = model_ref

    def enter_mode(self):
        model = self._model_ref()
        model.browserView = self.component
        model.browserData = self.component
        super(BrowserComponentMode, self).enter_mode()


class BrowseModeBase(Mode):

    def __init__(self, component_mode = None, *a, **k):
        raise component_mode is not None or AssertionError
        super(BrowseModeBase, self).__init__()
        self._component_mode = component_mode

    def enter_mode(self):
        self._component_mode.enter_mode()

    def leave_mode(self):
        self._component_mode.leave_mode()


class AddDeviceMode(BrowseModeBase):

    def __init__(self, song, browser, *a, **k):
        super(AddDeviceMode, self).__init__(*a, **k)
        self._song = song
        self._browser = browser

    def enter_mode(self):
        self._browser.hotswap_target = None
        self._browser.filter_type = get_filter_type_for_track(self._song)
        super(AddDeviceMode, self).enter_mode()


class AddTrackMode(BrowseModeBase):

    def __init__(self, browser, *a, **k):
        super(AddTrackMode, self).__init__(*a, **k)
        self._browser = browser

    def enter_mode(self):
        self._browser.hotswap_target = None
        super(AddTrackMode, self).enter_mode()


class BrowseMode(BrowseModeBase):

    def __init__(self, application, song, browser, *a, **k):
        super(BrowseMode, self).__init__(*a, **k)
        self._song = song
        self._browser = browser
        self._hotswap_mode = BrowserHotswapMode(application=application)
        self._in_hotswap_mode = False

    def enter_mode(self):
        if self._component_mode.component.browse_for_audio_clip:
            self._browser.filter_type = Live.Browser.FilterType.samples
        else:
            self._hotswap_mode.enter_mode()
            self._in_hotswap_mode = True
            if liveobj_valid(self._browser.hotswap_target):
                self._browser.filter_type = Live.Browser.FilterType.disabled
            else:
                self._browser.filter_type = get_filter_type_for_track(self._song)
        super(BrowseMode, self).enter_mode()

    def leave_mode(self):
        super(BrowseMode, self).leave_mode()
        if self._in_hotswap_mode:
            self._hotswap_mode.leave_mode()