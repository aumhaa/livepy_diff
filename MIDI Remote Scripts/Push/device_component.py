
from __future__ import absolute_import, print_function
from pushbase.device_component import DeviceComponent as DeviceComponentBase
from pushbase.parameter_provider import ParameterInfo
from .parameter_mapping_sensitivities import parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity

class DeviceComponent(DeviceComponentBase):

    def _create_parameter_info(self, parameter):
        return ParameterInfo(parameter=parameter, default_encoder_sensitivity=parameter_mapping_sensitivity(parameter), fine_grain_encoder_sensitivity=fine_grain_parameter_mapping_sensitivity(parameter))