#Embedded file name: /Users/versonator/Jenkins/live/Projects/AppLive/Resources/MIDI Remote Scripts/Launch_Control/ConfigurableButtonElement.py
from Launchpad.ConfigurableButtonElement import ConfigurableButtonElement as LaunchpadButtonElement
import Colors

class ConfigurableButtonElement(LaunchpadButtonElement):

    def set_light(self, value):
        if value is Colors.LED_OFF:
            self.send_value(value)
        else:
            super(ConfigurableButtonElement, self).set_light(value)