#Embedded file name: /Applications/Ableton Live 9.05 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Codec_b995_9/CodecResetSendsComponent.py
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement

class CodecResetSendsComponent(ControlSurfaceComponent):
    """ Special Component to reset all track sends to zero for the first four returns """
    __module__ = __name__

    def __init__(self, script, *a, **k):
        super(CodecResetSendsComponent, self).__init__(*a, **k)
        self._script = script
        self._buttons = [ [ None for index in range(4) ] for index in range(8) ]

    def disconnect(self):
        if self._buttons != None:
            for column in self._buttons:
                for button in column:
                    if button != None:
                        button.remove_value_listener(self.reset_send)

        self._buttons = []

    def on_enabled_changed(self):
        self.update()

    def set_buttons(self, buttons):
        for column in buttons:
            for button in column:
                raise isinstance(button, ButtonElement) or button == None or AssertionError

        for column in self._buttons:
            for button in column:
                if button != None:
                    button.remove_value_listener(self.reset_send)

        self._buttons = buttons
        for column in self._buttons:
            for button in column:
                if button != None:
                    button.add_value_listener(self.reset_send, identify_sender=True)

    def update(self):
        pass

    def reset_send(self, value, sender):
        raise self.is_enabled() and not self._script._shift_pressed and (self._buttons != None or AssertionError)
        if not isinstance(value, int):
            raise AssertionError
            tracks = self.tracks_to_use()
            returns = self.returns_to_use()
            if value is not 0 or not sender.is_momentary():
                for column in range(8):
                    for row in range(4):
                        if sender is self._buttons[column][row]:
                            if row < len(returns):
                                for track in tracks:
                                    track.mixer_device.sends[row].value = 0

                                for track in returns:
                                    track.mixer_device.sends[row].value = 0

                            break

    def tracks_to_use(self):
        return self.song().tracks

    def returns_to_use(self):
        return self.song().return_tracks