
"""
Alias_Map.py

Created by amounra on 2012-12-30.
Copyright (c) 2010 __artisia__. All rights reserved.

This file allows the reassignment of the controls from their default arrangement.  The order is from left to right; 
Buttons are Note #'s and Faders/Rotaries are Controller #'s
"""
DISABLE_MASTER_VOLUME = False
CHANNEL = 0
ALIAS_BUTTONS = [ index for index in range(16) ]
ALIAS_FADERS = [ index + 17 for index in range(9) ]
ALIAS_DIALS = [ index + 1 for index in range(16) ]
ALIAS_ENCODER = 42
FOLLOW = True
COLOR_MAP = [2,
 64,
 4,
 8,
 16,
 127,
 32]
MUTE_TOG = 2
REC_TOG = 5