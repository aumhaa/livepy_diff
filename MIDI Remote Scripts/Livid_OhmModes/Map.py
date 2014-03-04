
"""
Ohm64_Map.py

Created by amounra on 2010-10-05.
Copyright (c) 2010 __artisia__. All rights reserved.

This file allows the reassignment of the controls from their default arrangement.  The order is from left to right; 
Buttons are Note #'s and Faders/Rotaries are Controller #'s

"""
CHANNEL = 0
FORCE_TYPE = False
FORCE_COLOR_TYPE = 1
OHM_BUTTONS = [65,
 73,
 66,
 74,
 67,
 75,
 68,
 76]
OHM_FADERS = [23,
 22,
 15,
 14,
 5,
 7,
 6,
 4]
OHM_DIALS = [17,
 16,
 9,
 8,
 19,
 18,
 11,
 10,
 21,
 20,
 13,
 12,
 3,
 1,
 0,
 2]
OHM_MENU = [69,
 70,
 71,
 77,
 78,
 79]
CROSSFADER = 24
SHIFT_L = 64
SHIFT_R = 72
LIVID = 87
PAGE1_DRUM_CHANNEL = 9
PAGE1_DRUM_MAP = [[0,
  1,
  2,
  3],
 [4,
  5,
  6,
  7],
 [8,
  9,
  10,
  11],
 [12,
  13,
  14,
  15]]
PAGE1_BASS_CHANNEL = 10
PAGE1_BASS_MAP = [[24,
  28,
  32,
  36],
 [25,
  29,
  33,
  37],
 [26,
  30,
  34,
  38],
 [27,
  31,
  35,
  39]]
PAGE1_KEYS_CHANNEL = 11
PAGE1_KEYS_MAP = [[24, 12, 0],
 [26, 14, 2],
 [28, 16, 4],
 [29, 17, 5],
 [31, 19, 7],
 [33, 21, 9],
 [35, 23, 11],
 [36, 24, 12]]
PAGE1_MODES_MAP = [[0,
  0,
  0,
  0,
  0,
  0,
  0,
  0],
 [0,
  0,
  -1,
  0,
  0,
  0,
  -1,
  0],
 [0,
  -1,
  -1,
  0,
  0,
  -1,
  -1,
  0],
 [0,
  0,
  0,
  1,
  0,
  0,
  0,
  0],
 [0,
  0,
  0,
  0,
  0,
  0,
  -1,
  0],
 [0,
  0,
  -1,
  0,
  0,
  -1,
  -1,
  0],
 [0,
  -1,
  -1,
  0,
  -1,
  -1,
  -1,
  0],
 [0,
  0,
  0,
  0,
  0,
  0,
  0,
  0]]
BACKLIGHT_TYPE = ['static',
 'pulse',
 'up',
 'down']
BACKLIGHT_VALUE = [127,
 96,
 64,
 32]
OHM_TYPE = ['static',
 'pulse',
 'up',
 'down']
OHM_VALUE = [127,
 96,
 64,
 32]
PAD_TRANSLATION = ((0, 0, 0, 9),
 (0, 1, 1, 9),
 (0, 2, 2, 9),
 (0, 3, 3, 9),
 (1, 0, 4, 9),
 (1, 1, 5, 9),
 (1, 2, 6, 9),
 (1, 3, 7, 9),
 (2, 0, 8, 9),
 (2, 1, 9, 9),
 (2, 2, 10, 9),
 (2, 3, 11, 9),
 (3, 0, 12, 9),
 (3, 1, 13, 9),
 (3, 2, 14, 9),
 (3, 3, 15, 9))
FOLLOW = True
COLOR_MAP = [2,
 64,
 4,
 8,
 16,
 127,
 32]
STOP_CLIP_COLOR = [127, 1]
CLIP_TRIGD_TO_PLAY_COLOR = [13, 1]
CLIP_TRIGD_TO_RECORD_COLOR = [12, 1]
CLIP_STOPPED_COLOR = [1, 1]
CLIP_STARTED_COLOR = [6, 13]
CLIP_RECORDING_COLOR = [5, 19]
ZOOM_STOPPED_COLOR = [1, 1]
ZOOM_PLAYING_COLOR = [6, 13]
ZOOM_SELECTED_COLOR = [9, 7]
ARM_COLOR = [5, 14]
STOP_COLOR = [127, 1]
PLAY_COLOR = [6, 1]
MUTE_COLOR = [2, 1]
CROSSFADE_ASSIGN_COLOR = [4, 1]
SCENE_LAUNCH_COLOR = [1, 7]
NAV_BUTTON_COLOR = [3, 1]
DRUM_COLOR = [6, 20]
KEYS_COLOR = [2, 1]
BASS_COLOR = [5, 32]
DEVICE_NAV_COLOR = [2, 1]
SOLO_COLOR = [3, 7]
TAP_COLOR = [1, 1]
SELECT_COLOR = [1, 127]