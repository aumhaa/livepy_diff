#Embedded file name: /Users/versonator/Jenkins/live/Projects/AppLive/Resources/MIDI Remote Scripts/Push/DeviceParameterComponent.py
from itertools import chain, ifilter
import Live
AutomationState = Live.DeviceParameter.AutomationState
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.SubjectSlot import subject_slot_group
from _Framework.Util import find_if
import consts

def graphic_bar_for_parameter(parameter):
    if parameter.min == -1 * parameter.max:
        return consts.GRAPH_PAN
    elif parameter.is_quantized:
        return consts.GRAPH_SIN
    return consts.GRAPH_VOL


def convert_parameter_value_to_graphic(param, param_to_value = lambda p: p.value):
    if param != None:
        param_range = param.max - param.min
        param_bar = graphic_bar_for_parameter(param)
        graph_range = len(param_bar) - 1
        value = int((param_to_value(param) - param.min) / param_range * graph_range)
        graphic_display_string = param_bar[value]
    else:
        graphic_display_string = ' '
    return graphic_display_string


class DeviceParameterComponent(ControlSurfaceComponent):

    def __init__(self, *a, **k):
        super(DeviceParameterComponent, self).__init__(*a, **k)
        self._parameter_name_data_sources = [ DisplayDataSource(' ') for _ in xrange(8) ]
        self._parameter_value_data_sources = [ DisplayDataSource(' ') for _ in xrange(8) ]
        self._parameter_graphic_data_sources = [ DisplayDataSource(' ') for _ in xrange(8) ]

    @property
    def parameters(self):
        raise NotImplementedError

    def get_parameter_name(self, parameter, index):
        return parameter.name if parameter else None

    def clear_display(self):
        for source in chain(self._parameter_name_data_sources, self._parameter_value_data_sources, self._parameter_graphic_data_sources):
            source.set_display_string(' ')

    def set_name_display_line(self, line):
        self._set_display_line(line, self._parameter_name_data_sources)

    def set_value_display_line(self, line):
        self._set_display_line(line, self._parameter_value_data_sources)

    def set_graphic_display_line(self, line):
        self._set_display_line(line, self._parameter_graphic_data_sources)

    def _set_display_line(self, line, sources):
        if line:
            line.set_num_segments(len(sources))
            for segment in xrange(len(sources)):
                line.segment(segment).set_data_source(sources[segment])

    def _update_parameters(self):
        self._on_parameter_value_changed.replace_subjects(self.parameters)
        self._on_parameter_automation_state_changed.replace_subjects(self.parameters)
        self._update_parameter_names()
        self._update_parameter_values()

    @subject_slot_group('value')
    def _on_parameter_value_changed(self, parameter):
        self._update_parameter_values()

    @subject_slot_group('automation_state')
    def _on_parameter_automation_state_changed(self, parameter):
        self._update_parameter_names()
        self._update_parameter_values()

    def _update_parameter_names(self):
        if self.is_enabled():
            for i, (parameter, name_data_source) in enumerate(map(None, self.parameters, self._parameter_name_data_sources)):

                def inidicate_automation(parameter):
                    param_name = self.get_parameter_name(parameter, i)
                    if parameter.automation_state != AutomationState.none:
                        param_name = consts.CHAR_FULL_BLOCK + param_name
                    return param_name

                name_data_source.set_display_string(inidicate_automation(parameter) if parameter else ' ')

    def _update_parameter_values(self):
        if self.is_enabled():
            for parameter, data_source in map(None, self.parameters, self._parameter_value_data_sources):
                value_string = self.parameter_to_string(parameter)
                if parameter and parameter.automation_state == AutomationState.overridden:
                    value_string = '[%s]' % value_string
                data_source.set_display_string(value_string)

            for param, data_source in map(None, self.parameters, self._parameter_graphic_data_sources):
                graph = convert_parameter_value_to_graphic(param, self.parameter_to_value)
                data_source.set_display_string(graph)

    def parameter_to_string(self, parameter):
        return ' ' if parameter == None else unicode(parameter)

    def parameter_to_value(self, parameter):
        return parameter.value