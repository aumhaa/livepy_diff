
from __future__ import absolute_import, print_function, unicode_literals
from pushbase.parameter_provider import ParameterInfo
from pushbase.selected_track_parameter_provider import SelectedTrackParameterProvider as SelectedTrackParameterProviderBase
from .parameter_mapping_sensitivities import parameter_mapping_sensitivity, fine_grain_parameter_mapping_sensitivity

class SelectedTrackParameterProvider(SelectedTrackParameterProviderBase):

    def _create_parameter_info(self, parameter, name):
        raise name is not None or AssertionError
        return ParameterInfo(name=name, parameter=parameter, default_encoder_sensitivity=parameter_mapping_sensitivity(parameter), fine_grain_encoder_sensitivity=fine_grain_parameter_mapping_sensitivity(parameter))