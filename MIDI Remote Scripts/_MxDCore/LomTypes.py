
import ast
from collections import namedtuple
import json
import types
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ControlElement import ControlElement
from _Framework.Util import is_iterable

class MFLPropertyFormats:
    Default, JSON = range(2)


_MFLProperty = namedtuple('MFLProperty', 'name format to_json from_json min_epii_version')

def MFLProperty(name, format = MFLPropertyFormats.Default, to_json = None, from_json = None, min_epii_version = (-1, -1)):
    return _MFLProperty(name, format, to_json, from_json, min_epii_version)


def data_dict_to_json(property_name, data_dict):
    return json.dumps({property_name: data_dict})


def json_to_data_dict(property_name, json_dict):
    data_dict = ast.literal_eval(json_dict)
    return data_dict.get(property_name, data_dict)


def verify_routings_available_for_track(track, prop_name):
    error_format = "'%s' not available on %s"
    song = track.canonical_parent
    if track == song.master_track:
        raise RuntimeError(error_format % (prop_name, 'master track'))
    elif 'input' in prop_name:
        if track.is_foldable:
            raise RuntimeError(error_format % (prop_name, 'group tracks'))
        elif track in song.return_tracks:
            raise RuntimeError(error_format % (prop_name, 'return tracks'))


def routing_object_to_dict(routing_type):
    return {'display_name': routing_type.display_name,
     'identifier': hash(routing_type)}


def available_routing_objects_to_json(track, property_name):
    verify_routings_available_for_track(track, property_name)
    property_value = getattr(track, property_name)
    return data_dict_to_json(property_name, tuple([ routing_object_to_dict(t) for t in property_value ]))


def available_routing_input_types_to_json(track):
    return available_routing_objects_to_json(track, 'available_input_routing_types')


def available_routing_output_types_to_json(track):
    return available_routing_objects_to_json(track, 'available_output_routing_types')


def available_routing_input_channels_to_json(track):
    return available_routing_objects_to_json(track, 'available_input_routing_channels')


def available_routing_output_channels_to_json(track):
    return available_routing_objects_to_json(track, 'available_output_routing_channels')


def routing_object_to_json(track, property_name):
    verify_routings_available_for_track(track, property_name)
    property_value = getattr(track, property_name)
    return data_dict_to_json(property_name, routing_object_to_dict(property_value))


def routing_input_type_to_json(track):
    return routing_object_to_json(track, 'input_routing_type')


def routing_output_type_to_json(track):
    return routing_object_to_json(track, 'output_routing_type')


def routing_input_channel_to_json(track):
    return routing_object_to_json(track, 'input_routing_channel')


def routing_output_channel_to_json(track):
    return routing_object_to_json(track, 'output_routing_channel')


def json_to_routing_object(track, property_name, json_dict):
    verify_routings_available_for_track(track, property_name)
    objects = getattr(track, 'available_%ss' % property_name, [])
    identifier = json_to_data_dict(property_name, json_dict)['identifier']
    for routing_object in objects:
        if hash(routing_object) == identifier:
            return routing_object


def json_to_input_routing_type(track, json_dict):
    return json_to_routing_object(track, 'input_routing_type', json_dict)


def json_to_output_routing_type(track, json_dict):
    return json_to_routing_object(track, 'output_routing_type', json_dict)


def json_to_input_routing_channel(track, json_dict):
    return json_to_routing_object(track, 'input_routing_channel', json_dict)


def json_to_output_routing_channel(track, json_dict):
    return json_to_routing_object(track, 'output_routing_channel', json_dict)


_DEVICE_BASE_PROPS = [MFLProperty('canonical_parent'),
 MFLProperty('parameters'),
 MFLProperty('view'),
 MFLProperty('can_have_chains'),
 MFLProperty('can_have_drum_pads'),
 MFLProperty('class_display_name'),
 MFLProperty('class_name'),
 MFLProperty('is_active'),
 MFLProperty('name'),
 MFLProperty('type'),
 MFLProperty('store_chosen_bank')]
_DEVICE_VIEW_BASE_PROPS = [MFLProperty('canonical_parent'), MFLProperty('is_collapsed')]
_CHAIN_BASE_PROPS = [MFLProperty('canonical_parent'),
 MFLProperty('name'),
 MFLProperty('devices'),
 MFLProperty('delete_device'),
 MFLProperty('mute'),
 MFLProperty('solo'),
 MFLProperty('muted_via_solo'),
 MFLProperty('mixer_device'),
 MFLProperty('color'),
 MFLProperty('color_index'),
 MFLProperty('is_auto_colored'),
 MFLProperty('has_audio_input'),
 MFLProperty('has_audio_output'),
 MFLProperty('has_midi_input'),
 MFLProperty('has_midi_output')]
EXPOSED_TYPE_PROPERTIES = {Live.Application.Application: (MFLProperty('view'),
                                MFLProperty('current_dialog_button_count'),
                                MFLProperty('current_dialog_message'),
                                MFLProperty('open_dialog_count'),
                                MFLProperty('get_bugfix_version'),
                                MFLProperty('get_document'),
                                MFLProperty('get_major_version'),
                                MFLProperty('get_minor_version'),
                                MFLProperty('press_current_dialog_button')),
 Live.Application.Application.View: (MFLProperty('canonical_parent'),
                                     MFLProperty('browse_mode'),
                                     MFLProperty('available_main_views'),
                                     MFLProperty('focus_view'),
                                     MFLProperty('hide_view'),
                                     MFLProperty('is_view_visible'),
                                     MFLProperty('scroll_view'),
                                     MFLProperty('show_view'),
                                     MFLProperty('toggle_browse'),
                                     MFLProperty('zoom_view')),
 Live.Chain.Chain: tuple(_CHAIN_BASE_PROPS),
 Live.ChainMixerDevice.ChainMixerDevice: (MFLProperty('canonical_parent'),
                                          MFLProperty('volume'),
                                          MFLProperty('panning'),
                                          MFLProperty('sends'),
                                          MFLProperty('chain_activator')),
 Live.Clip.Clip: (MFLProperty('canonical_parent'),
                  MFLProperty('view'),
                  MFLProperty('color'),
                  MFLProperty('color_index'),
                  MFLProperty('end_marker'),
                  MFLProperty('has_envelopes'),
                  MFLProperty('is_arrangement_clip'),
                  MFLProperty('is_audio_clip'),
                  MFLProperty('is_midi_clip'),
                  MFLProperty('is_overdubbing'),
                  MFLProperty('is_playing'),
                  MFLProperty('is_recording'),
                  MFLProperty('is_triggered'),
                  MFLProperty('length'),
                  MFLProperty('loop_end'),
                  MFLProperty('loop_start'),
                  MFLProperty('looping'),
                  MFLProperty('muted'),
                  MFLProperty('name'),
                  MFLProperty('playing_position'),
                  MFLProperty('position'),
                  MFLProperty('signature_denominator'),
                  MFLProperty('signature_numerator'),
                  MFLProperty('start_marker'),
                  MFLProperty('start_time'),
                  MFLProperty('will_record_on_start'),
                  MFLProperty('clear_all_envelopes'),
                  MFLProperty('clear_envelope'),
                  MFLProperty('deselect_all_notes'),
                  MFLProperty('duplicate_loop'),
                  MFLProperty('fire'),
                  MFLProperty('get_notes'),
                  MFLProperty('get_selected_notes'),
                  MFLProperty('move_playing_pos'),
                  MFLProperty('quantize'),
                  MFLProperty('quantize_pitch'),
                  MFLProperty('remove_notes'),
                  MFLProperty('replace_selected_notes'),
                  MFLProperty('scrub'),
                  MFLProperty('select_all_notes'),
                  MFLProperty('set_fire_button_state'),
                  MFLProperty('set_notes'),
                  MFLProperty('stop'),
                  MFLProperty('stop_scrub'),
                  MFLProperty('available_warp_modes'),
                  MFLProperty('file_path'),
                  MFLProperty('gain'),
                  MFLProperty('gain_display_string'),
                  MFLProperty('pitch_coarse'),
                  MFLProperty('pitch_fine'),
                  MFLProperty('ram_mode'),
                  MFLProperty('warp_mode'),
                  MFLProperty('warping')),
 Live.Clip.Clip.View: (MFLProperty('canonical_parent'),
                       MFLProperty('grid_is_triplet'),
                       MFLProperty('grid_quantization'),
                       MFLProperty('hide_envelope'),
                       MFLProperty('select_envelope_parameter'),
                       MFLProperty('show_envelope'),
                       MFLProperty('show_loop')),
 Live.ClipSlot.ClipSlot: (MFLProperty('canonical_parent'),
                          MFLProperty('clip'),
                          MFLProperty('color'),
                          MFLProperty('color_index'),
                          MFLProperty('controls_other_clips'),
                          MFLProperty('duplicate_clip_to'),
                          MFLProperty('has_clip'),
                          MFLProperty('has_stop_button'),
                          MFLProperty('is_group_slot'),
                          MFLProperty('is_playing'),
                          MFLProperty('is_recording'),
                          MFLProperty('is_triggered'),
                          MFLProperty('playing_status'),
                          MFLProperty('will_record_on_start'),
                          MFLProperty('create_clip'),
                          MFLProperty('delete_clip'),
                          MFLProperty('fire'),
                          MFLProperty('set_fire_button_state'),
                          MFLProperty('stop')),
 Live.Device.Device: tuple(_DEVICE_BASE_PROPS),
 Live.Device.Device.View: tuple(_DEVICE_VIEW_BASE_PROPS),
 Live.DeviceParameter.DeviceParameter: (MFLProperty('canonical_parent'),
                                        MFLProperty('automation_state'),
                                        MFLProperty('is_enabled'),
                                        MFLProperty('is_quantized'),
                                        MFLProperty('max'),
                                        MFLProperty('min'),
                                        MFLProperty('name'),
                                        MFLProperty('original_name'),
                                        MFLProperty('state'),
                                        MFLProperty('value'),
                                        MFLProperty('value_items'),
                                        MFLProperty('re_enable_automation'),
                                        MFLProperty('str_for_value'),
                                        MFLProperty('__str__')),
 Live.DrumChain.DrumChain: tuple(_CHAIN_BASE_PROPS + [MFLProperty('out_note'), MFLProperty('choke_group')]),
 Live.DrumPad.DrumPad: (MFLProperty('canonical_parent'),
                        MFLProperty('chains'),
                        MFLProperty('mute'),
                        MFLProperty('name'),
                        MFLProperty('note'),
                        MFLProperty('solo'),
                        MFLProperty('delete_all_chains')),
 Live.MaxDevice.MaxDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty('get_bank_count'), MFLProperty('get_bank_name'), MFLProperty('get_bank_parameters')]),
 Live.MixerDevice.MixerDevice: (MFLProperty('canonical_parent'),
                                MFLProperty('sends'),
                                MFLProperty('panning'),
                                MFLProperty('track_activator'),
                                MFLProperty('volume'),
                                MFLProperty('crossfade_assign')),
 Live.PluginDevice.PluginDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty('presets'), MFLProperty('selected_preset_index')]),
 Live.RackDevice.RackDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty('chains'),
                              MFLProperty('drum_pads'),
                              MFLProperty('return_chains'),
                              MFLProperty('visible_drum_pads'),
                              MFLProperty('has_macro_mappings'),
                              MFLProperty('copy_pad'),
                              MFLProperty('has_drum_pads')]),
 Live.RackDevice.RackDevice.View: tuple(_DEVICE_VIEW_BASE_PROPS + [MFLProperty('selected_chain'),
                                   MFLProperty('is_showing_chain_devices'),
                                   MFLProperty('selected_drum_pad'),
                                   MFLProperty('drum_pads_scroll_position')]),
 Live.Sample.Sample: (MFLProperty('canonical_parent'),
                      MFLProperty('beats_granulation_resolution'),
                      MFLProperty('beats_transient_envelope'),
                      MFLProperty('beats_transient_loop_mode'),
                      MFLProperty('complex_pro_envelope'),
                      MFLProperty('complex_pro_formants'),
                      MFLProperty('end_marker'),
                      MFLProperty('file_path'),
                      MFLProperty('gain'),
                      MFLProperty('length'),
                      MFLProperty('slicing_sensitivity'),
                      MFLProperty('start_marker'),
                      MFLProperty('texture_flux'),
                      MFLProperty('texture_grain_size'),
                      MFLProperty('tones_grain_size'),
                      MFLProperty('warp_mode'),
                      MFLProperty('warping'),
                      MFLProperty('gain_display_string'),
                      MFLProperty('insert_slice'),
                      MFLProperty('move_slice'),
                      MFLProperty('remove_slice'),
                      MFLProperty('clear_slices'),
                      MFLProperty('reset_slices'),
                      MFLProperty('slicing_style'),
                      MFLProperty('slicing_beat_division'),
                      MFLProperty('slicing_region_count')),
 Live.Scene.Scene: (MFLProperty('canonical_parent'),
                    MFLProperty('clip_slots'),
                    MFLProperty('color'),
                    MFLProperty('color_index'),
                    MFLProperty('is_empty'),
                    MFLProperty('is_triggered'),
                    MFLProperty('name'),
                    MFLProperty('tempo'),
                    MFLProperty('fire'),
                    MFLProperty('fire_as_selected'),
                    MFLProperty('set_fire_button_state')),
 Live.SimplerDevice.SimplerDevice: tuple(_DEVICE_BASE_PROPS + [MFLProperty('sample'),
                                    MFLProperty('can_warp_as'),
                                    MFLProperty('can_warp_double'),
                                    MFLProperty('can_warp_half'),
                                    MFLProperty('multi_sample_mode'),
                                    MFLProperty('pad_slicing'),
                                    MFLProperty('playback_mode'),
                                    MFLProperty('playing_position'),
                                    MFLProperty('playing_position_enabled'),
                                    MFLProperty('retrigger'),
                                    MFLProperty('slicing_playback_mode'),
                                    MFLProperty('voices'),
                                    MFLProperty('crop'),
                                    MFLProperty('guess_playback_length'),
                                    MFLProperty('reverse'),
                                    MFLProperty('warp_as'),
                                    MFLProperty('warp_double'),
                                    MFLProperty('warp_half')]),
 Live.SimplerDevice.SimplerDevice.View: tuple(_DEVICE_VIEW_BASE_PROPS + [MFLProperty('selected_slice')]),
 Live.Song.Song: (MFLProperty('cue_points'),
                  MFLProperty('return_tracks'),
                  MFLProperty('scenes'),
                  MFLProperty('tracks'),
                  MFLProperty('visible_tracks'),
                  MFLProperty('master_track'),
                  MFLProperty('view'),
                  MFLProperty('appointed_device'),
                  MFLProperty('arrangement_overdub'),
                  MFLProperty('back_to_arranger'),
                  MFLProperty('can_jump_to_next_cue'),
                  MFLProperty('can_jump_to_prev_cue'),
                  MFLProperty('can_redo'),
                  MFLProperty('can_undo'),
                  MFLProperty('clip_trigger_quantization'),
                  MFLProperty('current_song_time'),
                  MFLProperty('exclusive_arm'),
                  MFLProperty('exclusive_solo'),
                  MFLProperty('groove_amount'),
                  MFLProperty('is_playing'),
                  MFLProperty('last_event_time'),
                  MFLProperty('loop'),
                  MFLProperty('loop_length'),
                  MFLProperty('loop_start'),
                  MFLProperty('metronome'),
                  MFLProperty('midi_recording_quantization'),
                  MFLProperty('nudge_down'),
                  MFLProperty('overdub'),
                  MFLProperty('punch_in'),
                  MFLProperty('punch_out'),
                  MFLProperty('nudge_up'),
                  MFLProperty('re_enable_automation_enabled'),
                  MFLProperty('record_mode'),
                  MFLProperty('root_note'),
                  MFLProperty('scale_name'),
                  MFLProperty('select_on_launch'),
                  MFLProperty('session_automation_record'),
                  MFLProperty('session_record'),
                  MFLProperty('session_record_status'),
                  MFLProperty('signature_denominator'),
                  MFLProperty('signature_numerator'),
                  MFLProperty('song_length'),
                  MFLProperty('swing_amount'),
                  MFLProperty('tempo'),
                  MFLProperty('capture_and_insert_scene'),
                  MFLProperty('continue_playing'),
                  MFLProperty('create_audio_track'),
                  MFLProperty('create_midi_track'),
                  MFLProperty('create_return_track'),
                  MFLProperty('create_scene'),
                  MFLProperty('delete_scene'),
                  MFLProperty('delete_track'),
                  MFLProperty('delete_return_track'),
                  MFLProperty('duplicate_scene'),
                  MFLProperty('duplicate_track'),
                  MFLProperty('find_device_position'),
                  MFLProperty('get_beats_loop_length'),
                  MFLProperty('get_beats_loop_start'),
                  MFLProperty('get_current_beats_song_time'),
                  MFLProperty('get_current_smpte_song_time'),
                  MFLProperty('is_cue_point_selected'),
                  MFLProperty('jump_by'),
                  MFLProperty('jump_to_next_cue'),
                  MFLProperty('jump_to_prev_cue'),
                  MFLProperty('move_device'),
                  MFLProperty('play_selection'),
                  MFLProperty('re_enable_automation'),
                  MFLProperty('redo'),
                  MFLProperty('scrub_by'),
                  MFLProperty('set_or_delete_cue'),
                  MFLProperty('start_playing'),
                  MFLProperty('stop_all_clips'),
                  MFLProperty('stop_playing'),
                  MFLProperty('tap_tempo'),
                  MFLProperty('force_link_beat_time'),
                  MFLProperty('trigger_session_record'),
                  MFLProperty('undo')),
 Live.Song.Song.View: (MFLProperty('canonical_parent'),
                       MFLProperty('detail_clip'),
                       MFLProperty('highlighted_clip_slot'),
                       MFLProperty('selected_chain'),
                       MFLProperty('selected_parameter'),
                       MFLProperty('selected_scene'),
                       MFLProperty('selected_track'),
                       MFLProperty('draw_mode'),
                       MFLProperty('follow_song'),
                       MFLProperty('select_device')),
 Live.Song.CuePoint: (MFLProperty('canonical_parent'),
                      MFLProperty('name'),
                      MFLProperty('time'),
                      MFLProperty('jump')),
 Live.Track.Track: (MFLProperty('available_input_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_input_types_to_json, min_epii_version=(4, 3)),
                    MFLProperty('available_output_routing_types', format=MFLPropertyFormats.JSON, to_json=available_routing_output_types_to_json, min_epii_version=(4, 3)),
                    MFLProperty('input_routing_type', format=MFLPropertyFormats.JSON, to_json=routing_input_type_to_json, from_json=json_to_input_routing_type, min_epii_version=(4, 3)),
                    MFLProperty('output_routing_type', format=MFLPropertyFormats.JSON, to_json=routing_output_type_to_json, from_json=json_to_output_routing_type, min_epii_version=(4, 3)),
                    MFLProperty('available_input_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_input_channels_to_json, min_epii_version=(4, 3)),
                    MFLProperty('available_output_routing_channels', format=MFLPropertyFormats.JSON, to_json=available_routing_output_channels_to_json, min_epii_version=(4, 3)),
                    MFLProperty('input_routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_input_channel_to_json, from_json=json_to_input_routing_channel, min_epii_version=(4, 3)),
                    MFLProperty('output_routing_channel', format=MFLPropertyFormats.JSON, to_json=routing_output_channel_to_json, from_json=json_to_output_routing_channel, min_epii_version=(4, 3)),
                    MFLProperty('clip_slots'),
                    MFLProperty('devices'),
                    MFLProperty('canonical_parent'),
                    MFLProperty('mixer_device'),
                    MFLProperty('view'),
                    MFLProperty('arm'),
                    MFLProperty('can_be_armed'),
                    MFLProperty('can_be_frozen'),
                    MFLProperty('can_show_chains'),
                    MFLProperty('color'),
                    MFLProperty('color_index'),
                    MFLProperty('current_input_routing'),
                    MFLProperty('current_input_sub_routing'),
                    MFLProperty('current_monitoring_state'),
                    MFLProperty('current_output_routing'),
                    MFLProperty('current_output_sub_routing'),
                    MFLProperty('fired_slot_index'),
                    MFLProperty('fold_state'),
                    MFLProperty('has_audio_input'),
                    MFLProperty('has_audio_output'),
                    MFLProperty('has_midi_input'),
                    MFLProperty('has_midi_output'),
                    MFLProperty('implicit_arm'),
                    MFLProperty('input_meter_level'),
                    MFLProperty('input_routings'),
                    MFLProperty('input_sub_routings'),
                    MFLProperty('input_meter_left'),
                    MFLProperty('input_meter_right'),
                    MFLProperty('is_foldable'),
                    MFLProperty('is_frozen'),
                    MFLProperty('is_grouped'),
                    MFLProperty('is_part_of_selection'),
                    MFLProperty('is_showing_chains'),
                    MFLProperty('is_visible'),
                    MFLProperty('mute'),
                    MFLProperty('muted_via_solo'),
                    MFLProperty('name'),
                    MFLProperty('output_meter_left'),
                    MFLProperty('output_meter_level'),
                    MFLProperty('output_meter_right'),
                    MFLProperty('output_routings'),
                    MFLProperty('output_sub_routings'),
                    MFLProperty('playing_slot_index'),
                    MFLProperty('solo'),
                    MFLProperty('delete_device'),
                    MFLProperty('duplicate_clip_slot'),
                    MFLProperty('jump_in_running_session_clip'),
                    MFLProperty('stop_all_clips')),
 Live.Track.Track.View: (MFLProperty('canonical_parent'),
                         MFLProperty('selected_device'),
                         MFLProperty('device_insert_mode'),
                         MFLProperty('is_collapsed'),
                         MFLProperty('select_instrument'))}
HIDDEN_TYPE_PROPERTIES = {Live.Sample.Sample: ('slices',)}
ENUM_TYPES = (Live.Song.Quantization,
 Live.Song.RecordingQuantization,
 Live.Song.CaptureMode,
 Live.Clip.GridQuantization,
 Live.DeviceParameter.AutomationState,
 Live.Sample.SlicingStyle,
 Live.Sample.SlicingBeatDivision)
TUPLE_TYPES = {'tracks': Live.Track.Track,
 'visible_tracks': Live.Track.Track,
 'return_tracks': Live.Track.Track,
 'clip_slots': Live.ClipSlot.ClipSlot,
 'scenes': Live.Scene.Scene,
 'parameters': Live.DeviceParameter.DeviceParameter,
 'sends': Live.DeviceParameter.DeviceParameter,
 'devices': Live.Device.Device,
 'cue_points': Live.Song.CuePoint,
 'chains': Live.Chain.Chain,
 'return_chains': Live.Chain.Chain,
 'drum_pads': Live.DrumPad.DrumPad,
 'visible_drum_pads': Live.DrumPad.DrumPad,
 'control_surfaces': ControlSurface,
 'components': ControlSurfaceComponent,
 'controls': ControlElement}
PROPERTY_TYPES = {'master_track': Live.Track.Track,
 'selected_track': Live.Track.Track,
 'selected_scene': Live.Scene.Scene,
 'volume': Live.DeviceParameter.DeviceParameter,
 'panning': Live.DeviceParameter.DeviceParameter,
 'crossfader': Live.DeviceParameter.DeviceParameter,
 'song_tempo': Live.DeviceParameter.DeviceParameter,
 'cue_volume': Live.DeviceParameter.DeviceParameter,
 'track_activator': Live.DeviceParameter.DeviceParameter,
 'chain_activator': Live.DeviceParameter.DeviceParameter,
 'clip': Live.Clip.Clip,
 'detail_clip': Live.Clip.Clip,
 'highlighted_clip_slot': Live.ClipSlot.ClipSlot,
 'selected_device': Live.Device.Device,
 'selected_parameter': Live.DeviceParameter.DeviceParameter,
 'selected_chain': Live.Chain.Chain,
 'selected_drum_pad': Live.DrumPad.DrumPad,
 'sample': Live.Sample.Sample,
 'mixer_device': (Live.MixerDevice.MixerDevice, Live.ChainMixerDevice.ChainMixerDevice),
 'view': (Live.Application.Application.View,
          Live.Song.Song.View,
          Live.Track.Track.View,
          Live.Device.Device.View,
          Live.RackDevice.RackDevice.View,
          Live.Clip.Clip.View)}
LIVE_APP = 'live_app'
LIVE_SET = 'live_set'
CONTROL_SURFACES = 'control_surfaces'
THIS_DEVICE = 'this_device'
ROOT_KEYS = (THIS_DEVICE,
 CONTROL_SURFACES,
 LIVE_APP,
 LIVE_SET)

class LomAttributeError(AttributeError):
    pass


class LomObjectError(AttributeError):
    pass


class LomNoteOperationWarning(Exception):
    pass


class LomNoteOperationError(AttributeError):
    pass


def get_exposed_lom_types():
    return EXPOSED_TYPE_PROPERTIES.keys()


def get_exposed_properties_for_type(lom_type, epii_version):
    return [ prop for prop in EXPOSED_TYPE_PROPERTIES.get(lom_type, []) if epii_version >= prop.min_epii_version ]


def get_exposed_property_names_for_type(lom_type, epii_version):
    return [ prop.name for prop in get_exposed_properties_for_type(lom_type, epii_version) ]


def is_property_exposed_for_type(property_name, lom_type, epii_version):
    return property_name in get_exposed_property_names_for_type(lom_type, epii_version)


def get_exposed_property_info(lom_type, property_name, epii_version):
    properties = get_exposed_properties_for_type(lom_type, epii_version)
    prop = filter(lambda p: p.name == property_name, properties)
    if not prop:
        return None
    return prop[0]


def is_class(class_object):
    return isinstance(class_object, types.ClassType) or hasattr(class_object, '__bases__')


def get_control_surfaces():
    result = []
    cs_list_key = 'control_surfaces'
    if isinstance(__builtins__, dict):
        if cs_list_key in __builtins__.keys():
            result = __builtins__[cs_list_key]
    elif hasattr(__builtins__, cs_list_key):
        result = getattr(__builtins__, cs_list_key)
    return tuple(result)


def get_root_prop(external_device, prop_key):
    root_properties = {LIVE_APP: Live.Application.get_application,
     LIVE_SET: lambda : Live.Application.get_application().get_document(),
     CONTROL_SURFACES: get_control_surfaces}
    if not prop_key in ROOT_KEYS:
        raise AssertionError
        return prop_key == THIS_DEVICE and external_device
    return root_properties[prop_key]()


def cs_base_classes():
    from _Framework.ControlSurface import ControlSurface
    from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
    from _Framework.ControlElement import ControlElement
    from ableton.v2.control_surface import ControlElement as ControlElement2
    from ableton.v2.control_surface import ControlSurface as ControlSurface2
    from ableton.v2.control_surface import Component as ControlSurfaceComponent2
    return (ControlSurface,
     ControlSurfaceComponent,
     ControlElement,
     ControlSurface2,
     ControlSurfaceComponent2,
     ControlElement2)


def is_lom_object(lom_object, lom_classes):
    return isinstance(lom_object, tuple(lom_classes) + (type(None),)) or isinstance(lom_object, cs_base_classes()) or isinstance(lom_object, Live.Base.Vector)


def is_cplusplus_lom_object(lom_object):
    return isinstance(lom_object, Live.LomObject.LomObject)


def is_object_iterable(obj):
    return not isinstance(obj, basestring) and is_iterable(obj) and not isinstance(obj, cs_base_classes())


def is_property_hidden(lom_object, property_name):
    return property_name in HIDDEN_TYPE_PROPERTIES.get(type(lom_object), [])


def verify_object_property(lom_object, property_name, epii_version):
    raise_error = False
    if isinstance(lom_object, cs_base_classes()):
        if not hasattr(lom_object, property_name):
            raise_error = True
    elif not is_property_exposed_for_type(property_name, type(lom_object), epii_version):
        raise_error = True
    if raise_error:
        raise LomAttributeError("'%s' object has no attribute '%s'" % (lom_object.__class__.__name__, property_name))