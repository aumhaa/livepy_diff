
from ableton.v2.control_surface.control import ToggleButtonControl
from pushbase.user_component import UserComponentBase

class UserComponent(UserComponentBase):
    user_mode_toggle_button = ToggleButtonControl()

    @user_mode_toggle_button.toggled
    def user_mode_toggle_button(self, toggled, button):
        self.toggle_mode()