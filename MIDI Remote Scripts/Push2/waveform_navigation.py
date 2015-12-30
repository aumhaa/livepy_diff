
from __future__ import absolute_import, print_function
from collections import namedtuple
from ableton.v2.base import SlotManager, Subject, const, clamp, depends, lazy_attribute, listenable_property, listens, listens_group, liveobj_changed, task
from ableton.v2.control_surface.control import EncoderControl
FocusMarker = namedtuple('FocusMarker', ['name', 'position'])

class WaveformNavigation(SlotManager, Subject):
    """ Class for managing a visible area of a waveform """
    visible_start = listenable_property.managed(0)
    visible_end = listenable_property.managed(0)
    animate_visible_region = listenable_property.managed(False)
    show_focus = listenable_property.managed(False)
    ZOOM_SENSITIVITY = 12.0
    MIN_VISIBLE_LENGTH = 1000
    WAVEFORM_WIDTH_IN_PX = 933
    MARGIN_IN_PX = 121
    RELATIVE_FOCUS_MARGIN = float(MARGIN_IN_PX) / WAVEFORM_WIDTH_IN_PX
    FOCUSABLE_OBJECT_CONNECTIONS = {}

    def __init__(self, waveform_length = None, *a, **k):
        raise waveform_length is not None or AssertionError
        raise waveform_length > 0 or AssertionError
        super(WaveformNavigation, self).__init__(*a, **k)
        self._length = waveform_length
        self._focused_object = None
        self._focus_marker = FocusMarker('', 0)
        self._touched_objects = set()
        self._has_tasks = False
        self.set_visible_region(0, self._length)

    def disconnect(self):
        super(WaveformNavigation, self).disconnect()
        if self._has_tasks:
            self._tasks.kill()
            self._tasks.clear()

    def get_object_identifier(self, obj):
        raise NotImplementedError

    def get_object_provider(self):
        raise NotImplementedError

    def get_zoom_object(self):
        raise NotImplementedError

    @property
    def visible_length(self):
        """ Returns the length of the visible area """
        return self.visible_end - self.visible_start

    @property
    def visible_proportion(self):
        """ Returns the proportion between the visible length and the sample length """
        return self.visible_length / float(self._length)

    def set_visible_region(self, start, end, animate = False):
        self.animate_visible_region = animate
        self.visible_start = clamp(start, 0, self._length)
        self.visible_end = clamp(end, 0, self._length)

    def zoom(self, value):
        """ Zooms in or out of the waveform start
            value should be between -1.0 and 1.0, where 1.0 will zoom in as much as
            possible and -1.0 will zoom out completely.
        """
        zoom_factor = 1.0 + abs(value * self.ZOOM_SENSITIVITY)
        if value > 0:
            visible_length = self._length * self.visible_proportion / zoom_factor
        else:
            visible_length = self._length * self.visible_proportion * zoom_factor
        visible_length = clamp(visible_length, min(self._length, self.MIN_VISIBLE_LENGTH), self._length)
        self.focus_object(self._focused_object, visible_length=visible_length)
        self.show_focus = True
        self.try_hide_focus_delayed()

    def focus_position(self, position, align_right = False, animate = False, focus_name = '', visible_length = None):
        """ Focuses the position in the waveform and brings it into the visible range.
            The visible length is preserved, if visible_length is None. The position is
            aligned to the left or right of the visible range, with a certain margin
            defined by RELATIVE_FOCUS_MARGIN
            :position: the position in absolute sample time
            :align_right: focuses the position on the left or right side of the
            :animate: should be set to True if, if it should animate to the new position
            :visible_length: the amount of samples, that should be shown
        """
        visible_length = self.visible_length if visible_length is None else visible_length
        visible_margin = visible_length * self.RELATIVE_FOCUS_MARGIN
        length = self._length
        if align_right:
            right = position + visible_margin
            self.set_visible_region(clamp(right - visible_length, 0, length - visible_length), clamp(right, visible_length, length), animate)
        else:
            left = position - visible_margin
            self.set_visible_region(clamp(left, 0, length - visible_length), clamp(left + visible_length, visible_length, length), animate)
        self._focus_marker = FocusMarker(focus_name, position)
        self.notify_focus_marker()

    def focus_object(self, obj, visible_length = None):
        if obj != self.get_zoom_object():
            identifier = self.get_object_identifier(obj)
            if identifier in self.FOCUSABLE_OBJECT_CONNECTIONS:
                connection = self.FOCUSABLE_OBJECT_CONNECTIONS[identifier]
                self.focus_position(connection.getter(self.get_object_provider()), align_right=connection.align_right, animate=liveobj_changed(self._focused_object, obj), focus_name=connection.focus_name, visible_length=visible_length)
            self._focused_object = obj

    @listenable_property
    def focus_marker(self):
        return self._focus_marker

    def touch_object(self, obj):
        self._touched_objects.add(obj)
        self.focus_object(obj)
        self.show_focus = True

    def release_object(self, obj):
        if obj in self._touched_objects:
            self._touched_objects.remove(obj)
            self.try_hide_focus()

    def change_object(self, obj):
        self.focus_object(obj)
        self.show_focus = True
        self.try_hide_focus_delayed()

    def try_hide_focus(self):
        """ Hides the focus, if the focused object is not longer touched """
        if self._should_hide_focus():
            self.show_focus = False

    def try_hide_focus_delayed(self):
        """ Hides the focus after some time, if the focused object is not
            longer touched
        """
        if self._hide_focus_task and self._should_hide_focus():
            self._hide_focus_task.restart()

    def _should_hide_focus(self):
        return self.get_zoom_object() not in self._touched_objects and self._focused_object not in self._touched_objects

    def reset_focus_and_animation(self):
        self.show_focus = False
        self.animate_visible_region = False
        self._touched_objects = set()

    @lazy_attribute
    @depends(parent_task_group=const(None))
    def _tasks(self, parent_task_group = None):
        if parent_task_group is not None:
            tasks = parent_task_group.add(task.TaskGroup())
            self._has_tasks = True
            return tasks

    @lazy_attribute
    def _hide_focus_task(self):
        tasks = self._tasks
        if tasks is not None:
            return tasks.add(task.sequence(task.wait(EncoderControl.TOUCH_TIME), task.run(self.try_hide_focus)))


ObjectConnection = namedtuple('ObjectConnection', ['getter', 'align_right', 'focus_name'])

class SimplerWaveformNavigation(WaveformNavigation):
    """ Extends the WaveformNavigation class by the concept of focusing parameters
        and slices.
    """
    selected_slice_focus = object()
    FOCUSABLE_OBJECT_CONNECTIONS = {'Start': ObjectConnection(lambda simpler: simpler.sample.start_marker, False, 'start_marker'),
     'End': ObjectConnection(lambda simpler: simpler.sample.end_marker, True, 'end_marker'),
     'S Start': ObjectConnection(lambda simpler: simpler.view.sample_start, False, 'position'),
     'S Length': ObjectConnection(lambda simpler: simpler.view.sample_end, True, 'position'),
     'S Loop Length': ObjectConnection(lambda simpler: simpler.view.sample_loop_start, False, 'position'),
     selected_slice_focus: ObjectConnection(lambda simpler: simpler.view.selected_slice, False, '')}

    def __init__(self, simpler = None, *a, **k):
        super(SimplerWaveformNavigation, self).__init__(*a, **k)
        self._simpler = simpler
        focusable_parameters = [ self._simpler.get_parameter_by_name(n) for n in self.FOCUSABLE_OBJECT_CONNECTIONS ]
        self.__on_selected_slice_changed.subject = simpler.view
        self.__on_parameter_value_changed.replace_subjects(focusable_parameters)

    def get_object_identifier(self, obj):
        if hasattr(obj, 'name'):
            return obj.name
        return self.selected_slice_focus

    def get_object_provider(self):
        return self._simpler

    def get_zoom_object(self):
        return self._simpler.zoom

    @listens_group('value')
    def __on_parameter_value_changed(self, parameter):
        self.change_object(parameter)

    @listens('selected_slice')
    def __on_selected_slice_changed(self):
        slice_index = self._get_selected_slice_index()
        if slice_index != -1:
            self.focus_object(slice_index)

    def _get_selected_slice_index(self):
        try:
            return self._simpler.sample.slices.index(self._simpler.view.selected_slice)
        except ValueError:
            pass

        return -1


class AudioClipWaveformNavigation(WaveformNavigation):
    """ WaveformNavigation that adds the concept of focus for audio clips to the. """
    zoom_focus = object()
    start_marker_focus = object()
    loop_start_focus = object()
    loop_end_focus = object()
    FOCUSABLE_OBJECT_CONNECTIONS = {start_marker_focus: ObjectConnection(lambda clip: clip.view.sample_start_marker, False, 'start_marker'),
     loop_start_focus: ObjectConnection(lambda clip: clip.view.sample_loop_start, False, 'position'),
     loop_end_focus: ObjectConnection(lambda clip: clip.view.sample_loop_end, True, 'end_marker')}

    def __init__(self, clip = None, *a, **k):
        super(AudioClipWaveformNavigation, self).__init__(*a, **k)
        self._clip = clip
        self.__on_is_recording_changed.subject = clip

    def get_object_identifier(self, obj):
        return obj

    def get_object_provider(self):
        return self._clip

    def get_zoom_object(self):
        return self.zoom_focus

    @listens('is_recording')
    def __on_is_recording_changed(self):
        self._length = self._clip.view.sample_length
        self.set_visible_region(0, self._length)