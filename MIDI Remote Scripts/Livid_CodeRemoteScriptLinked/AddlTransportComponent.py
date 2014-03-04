
import Live
from TransportComponent import TransportComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement

class AddlTransportComponent(TransportComponent):
    """ TransportComponent that only uses certain buttons if a shift button is pressed """

    def __init__(self):
        TransportComponent.__init__(self)
        self._shift_button = None
        self._shift_pressed = False
        self._undo_button = None
        self._redo_button = None
        self._bts_button = None
        self._tempo_encoder_control = None

    def disconnect(self):
        TransportComponent.disconnect(self)
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None
        if self._undo_button != None:
            self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = None
        if self._redo_button != None:
            self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = None
        if self._bts_button != None:
            self._bts_button.remove_value_listener(self._bts_value)
            self._bts_button = None
        if self._tempo_encoder_control != None:
            self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
            self._tempo_encoder_control = None

    def set_shift_button(self, button):
        if not button == None:
            if isinstance(button, ButtonElement):
                if not button.is_momentary():
                    isinstance(button, ButtonElement)
                    raise AssertionError
                if self._shift_button != button:
                    self._shift_button != None and self._shift_button.remove_value_listener(self._shift_value)
                self._shift_button = button
                self._shift_button != None and self._shift_button.add_value_listener(self._shift_value)
            self._rebuild_callback()
            self.update()

    def update(self):
        self._on_metronome_changed()
        self._on_overdub_changed()
        self._on_nudge_up_changed()
        self._on_nudge_down_changed

    def _shift_value(self, value):
        if not self._shift_button != None:
            raise AssertionError
        if value not in range(128):
            raise AssertionError
        self._shift_pressed = value != 0
        if self.is_enabled():
            self.is_enabled()
            self.update()
        else:
            self.is_enabled()

    def _metronome_value(self, value):
        if not self._shift_pressed:
            TransportComponent._metronome_value(self, value)

    def _overdub_value(self, value):
        if not self._shift_pressed:
            TransportComponent._overdub_value(self, value)

    def _nudge_up_value(self, value):
        if not self._shift_pressed:
            TransportComponent._nudge_up_value(self, value)

    def _nudge_down_value(self, value):
        if not self._shift_pressed:
            TransportComponent._nudge_down_value(self, value)

    def _tap_tempo_value(self, value):
        if not self._shift_pressed:
            TransportComponent._tap_tempo_value(self, value)

    def _quant_toggle_value(self, value):
        if not self._quant_toggle_button != None:
            raise AssertionError
            raise value in range(128) or AssertionError
            if not self._last_quant_value != Live.Song.RecordingQuantization.rec_q_no_q:
                raise AssertionError
                if self.is_enabled() and not self._shift_pressed:
                    quant_value = (value != 0 or not self._quant_toggle_button.is_momentary()) and self.song().midi_recording_quantization
                    self._last_quant_value = quant_value != Live.Song.RecordingQuantization.rec_q_no_q and quant_value
                    self.song().midi_recording_quantization = Live.Song.RecordingQuantization.rec_q_no_q
                else:
                    self.song().midi_recording_quantization = self._last_quant_value

    def _on_metronome_changed(self):
        if not self._shift_pressed:
            TransportComponent._on_metronome_changed(self)

    def _on_overdub_changed(self):
        if not self._shift_pressed:
            TransportComponent._on_overdub_changed(self)

    def _on_nudge_up_changed(self):
        if not self._shift_pressed:
            TransportComponent._on_nudge_up_changed(self)

    def _on_nudge_down_changed(self):
        if not self._shift_pressed:
            TransportComponent._on_nudge_down_changed(self)

    def set_undo_button(self, undo_button):
        if not isinstance(undo_button, (ButtonElement, type(None))):
            raise AssertionError
            if undo_button != self._undo_button:
                if self._undo_button != None:
                    self._undo_button.remove_value_listener(self._undo_value)
                self._undo_button = undo_button
                self._undo_button != None and self._undo_button.add_value_listener(self._undo_value)
            self.update()

    def set_redo_button(self, redo_button):
        if not isinstance(redo_button, (ButtonElement, type(None))):
            raise AssertionError
            if redo_button != self._redo_button:
                if self._redo_button != None:
                    self._redo_button.remove_value_listener(self._redo_value)
                self._redo_button = redo_button
                self._redo_button != None and self._redo_button.add_value_listener(self._redo_value)
            self.update()

    def set_bts_button(self, bts_button):
        if not isinstance(bts_button, (ButtonElement, type(None))):
            raise AssertionError
            if bts_button != self._bts_button:
                if self._bts_button != None:
                    self._bts_button.remove_value_listener(self._bts_value)
                self._bts_button = bts_button
                self._bts_button != None and self._bts_button.add_value_listener(self._bts_value)
            self.update()

    def _undo_value(self, value):
        raise self._shift_pressed or self._undo_button != None or AssertionError
        if not value in range(128):
            raise AssertionError
            if self.is_enabled():
                if value != 0 or not self._undo_button.is_momentary():
                    if self.song().can_undo:
                        self.song().undo()

    def _redo_value(self, value):
        raise self._shift_pressed or self._redo_button != None or AssertionError
        if not value in range(128):
            raise AssertionError
            if self.is_enabled():
                if value != 0 or not self._redo_button.is_momentary():
                    if self.song().can_redo:
                        self.song().redo()

    def _bts_value(self, value):
        if not self._bts_button != None:
            raise AssertionError
            if not value in range(128):
                raise AssertionError
                self.song().current_song_time = self.is_enabled() and (value != 0 or not self._bts_button.is_momentary()) and 0.0

    def _tempo_encoder_value(self, value):
        raise self._shift_pressed and (self._tempo_encoder_control != None or AssertionError)
        if not value in range(128):
            raise AssertionError
            backwards = value >= 64
            step = 0.1
            if backwards:
                amount = value - 128
            else:
                amount = value
            tempo = max(20, min(999, self.song().tempo + amount * step))
            self.song().tempo = tempo

    def set_tempo_encoder(self, control):
        if not (control == None or isinstance(control, EncoderElement) and control.message_map_mode() is Live.MidiMap.MapMode.relative_two_compliment):
            raise AssertionError
            if self._tempo_encoder_control != None:
                self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
            self._tempo_encoder_control = control
            self._tempo_encoder_control != None and self._tempo_encoder_control.add_value_listener(self._tempo_encoder_value)
        self.update()