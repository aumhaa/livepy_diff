#Embedded file name: /Users/versonator/Jenkins/live/Projects/AppLive/Resources/MIDI Remote Scripts/Push/DisplayingDeviceComponent.py
import Live
AutomationState = Live.DeviceParameter.AutomationState
from _Framework.DeviceComponent import DeviceComponent
from DeviceParameterComponent import DeviceParameterComponent
import consts
DISCRETE_PARAMETERS_DICT = {'GlueCompressor': ('Ratio', 'Attack', 'Release', 'Peak Clip In')}

def is_parameter_quantized(parameter, parent_device):
    is_quantized = False
    if parameter != None:
        device_class = parent_device.class_name
        is_quantized = parameter.is_quantized or device_class in DISCRETE_PARAMETERS_DICT and parameter.name in DISCRETE_PARAMETERS_DICT[device_class]
    return is_quantized


class DisplayingDeviceComponent(DeviceParameterComponent, DeviceComponent):
    """
    Special device class that displays parameter values
    """

    def __init__(self, *a, **k):
        super(DisplayingDeviceComponent, self).__init__(*a, **k)
        self._mapped_parameters = []

    def set_device(self, device):
        super(DisplayingDeviceComponent, self).set_device(device)
        if self._device == None:
            self._mapped_parameters = []
            self.clear_display()

    @property
    def parameters(self):
        return self._mapped_parameters

    def _is_banking_enabled(self):
        return True

    def _assign_parameters(self):
        super(DisplayingDeviceComponent, self)._assign_parameters()
        self._update_mapping_sensitivity()
        _, self._mapped_parameters = self._current_bank_details()
        self._update_parameters()

    def _update_mapping_sensitivity(self):
        device = self.device()
        if device != None:
            for control in self._parameter_controls:
                if control != None:
                    parameter = control.mapped_parameter()
                    is_quantized = is_parameter_quantized(parameter, device)
                    control.mapping_sensitivity = consts.QUANTIZED_MAPPING_SENSITIVITY if is_quantized else consts.CONTINUOUS_MAPPING_SENSITIVITY