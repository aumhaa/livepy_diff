#Embedded file name: /Volumes/Jenkins2045_2/versonator2/Hudson/live/Projects/AppLive/Resources/MIDI Remote Scripts/LV2_LX2_LC2_LD2/LV2DeviceController.py
import Live
from FaderfoxDeviceController import FaderfoxDeviceController

class LV2DeviceController(FaderfoxDeviceController):
    __module__ = __name__

    def __init__(self, parent):
        LV2DeviceController.realinit(self, parent)

    def realinit(self, parent):
        FaderfoxDeviceController.realinit(self, parent)