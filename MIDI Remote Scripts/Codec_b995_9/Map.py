#Embedded file name: /Applications/Ableton Live 9.05 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Codec_b995_9/Map.py
"""
Codec_Map.py

Created by amounra on 2010-10-05.
Copyright (c) 2010 __artisia__. All rights reserved.

This file allows the reassignment of the controls from their default arrangement.  The order is from left to right; 
Buttons are Note #'s and Faders/Rotaries are Controller #'s
There will eventually be a way to reassign the functions accessed by the different shift modes from this file as well....
Hold tight ;)
"""
CHANNEL = 0
CODE_BUTTONS = [[1,
  5,
  9,
  13,
  17,
  21,
  25,
  29],
 [2,
  6,
  10,
  14,
  18,
  22,
  26,
  30],
 [3,
  7,
  11,
  15,
  19,
  23,
  27,
  31],
 [4,
  8,
  12,
  16,
  20,
  24,
  28,
  32]]
CODE_DIALS = [[1,
  5,
  9,
  13,
  17,
  21,
  25,
  29],
 [2,
  6,
  10,
  14,
  18,
  22,
  26,
  30],
 [3,
  7,
  11,
  15,
  19,
  23,
  27,
  31],
 [4,
  8,
  12,
  16,
  20,
  24,
  28,
  32]]
CODE_COLUMN_BUTTONS = [38,
 39,
 40,
 41,
 42,
 43,
 44,
 45]
CODE_ROW_BUTTONS = [33,
 34,
 35,
 36]
LIVID = 37
BACKLIGHT_TYPE = ['static',
 'pulse',
 'up',
 'down']
BACKLIGHT_VALUE = [127,
 96,
 64,
 32]
FOLLOW = True
SHIFT_THRESH = 3
LINK_MIXER = True
LINK_OFFSET = [0, 0]
COLOR_MAP = [127,
 127,
 127,
 127,
 127,
 127,
 127]
USE_DEVICE_SELECTOR = True