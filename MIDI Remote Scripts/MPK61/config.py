
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {u'STOP': GENERIC_STOP,
 u'PLAY': GENERIC_PLAY,
 u'REC': GENERIC_REC,
 u'LOOP': GENERIC_LOOP,
 u'RWD': GENERIC_RWD,
 u'FFWD': GENERIC_FFWD,
 u'NORELEASE': 0}
DEVICE_CONTROLS = ((GENERIC_ENC1, 0),
 (GENERIC_ENC2, 0),
 (GENERIC_ENC3, 0),
 (GENERIC_ENC4, 0),
 (GENERIC_ENC5, 0),
 (GENERIC_ENC6, 0),
 (GENERIC_ENC7, 0),
 (GENERIC_ENC8, 0))
VOLUME_CONTROLS = ((GENERIC_SLI1, 0),
 (GENERIC_SLI2, 0),
 (GENERIC_SLI3, 0),
 (GENERIC_SLI4, 0),
 (GENERIC_SLI5, 0),
 (GENERIC_SLI6, 0),
 (GENERIC_SLI7, 0),
 (GENERIC_SLI8, 0))
TRACKARM_CONTROLS = (GENERIC_BUT1,
 GENERIC_BUT2,
 GENERIC_BUT3,
 GENERIC_BUT4,
 GENERIC_BUT5,
 GENERIC_BUT6,
 GENERIC_BUT7,
 GENERIC_BUT8)
BANK_CONTROLS = {u'TOGGLELOCK': GENERIC_BUT9,
 u'BANKDIAL': -1,
 u'NEXTBANK': GENERIC_PAD5,
 u'PREVBANK': GENERIC_PAD1,
 u'BANK1': -1,
 u'BANK2': -1,
 u'BANK3': -1,
 u'BANK4': -1,
 u'BANK5': -1,
 u'BANK6': -1,
 u'BANK7': -1,
 u'BANK8': -1}
PAD_TRANSLATION = ((0, 0, 81, 1),
 (1, 0, 83, 1),
 (2, 0, 84, 1),
 (3, 0, 86, 1),
 (0, 1, 74, 1),
 (1, 1, 76, 1),
 (2, 1, 77, 1),
 (3, 1, 79, 1),
 (0, 2, 67, 1),
 (1, 2, 69, 1),
 (2, 2, 71, 1),
 (3, 2, 72, 1),
 (0, 3, 60, 1),
 (1, 3, 62, 1),
 (2, 3, 64, 1),
 (3, 3, 65, 1))
CONTROLLER_DESCRIPTION = {u'INPUTPORT': u'Akai MPK61',
 u'OUTPUTPORT': u'Akai MPK61',
 u'CHANNEL': 0,
 u'PAD_TRANSLATION': PAD_TRANSLATION}
MIXER_OPTIONS = {u'NUMSENDS': 2,
 u'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1),
 u'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1),
 u'MASTERVOLUME': -1}