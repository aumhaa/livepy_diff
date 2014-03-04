
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent

class ShiftModeComponent(ModeSelectorComponent):
    __module__ = __name__
    __doc__ = ' Special Class that uses two shift buttons and is lockable '

    def __init__(self, script, buttons):
        ModeSelectorComponent.__init__(self)
        self._script = script
        self._modes_buttons = []
        self._mode_index = 0
        self.set_mode_buttons(buttons)

    def number_of_modes(self):
        return 5

    def update(self):
        self._script.deassign_matrix()
        for index in range(self.number_of_modes()):
            if index == self._mode_index:
                self._modes_buttons[index].turn_on()
            else:
                self._modes_buttons[index].turn_off()

        if self._mode_index is 0:
            self._script.assign_page_0()
        elif self._mode_index is 1:
            self._script.assign_page_1()
        elif self._mode_index is 2:
            self._script.assign_pages_2_3()
        elif self._mode_index is 3:
            self._script.assign_pages_2_3()
        elif self._mode_index is 4:
            self._script.assign_page_4()

    def on_selected_track_changed(self):
        self.update()