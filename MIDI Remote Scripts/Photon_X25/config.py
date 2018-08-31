from __future__ import absolute_import, print_function, unicode_literals
from .consts import *
TRANSPORT_CONTROLS = {u'STOP': GENERIC_STOP,
 u'PLAY': GENERIC_PLAY,
 u'REC': GENERIC_REC,
 u'LOOP': GENERIC_LOOP,
 u'RWD': GENERIC_RWD,
 u'FFWD': GENERIC_FFWD}
DEVICE_CONTROLS = ((GENERIC_ENC1, 0),
 (GENERIC_ENC2, 1),
 (GENERIC_ENC3, 2),
 (GENERIC_ENC4, 3),
 (GENERIC_ENC5, 0),
 (GENERIC_ENC6, 1),
 (GENERIC_ENC7, 2),
 (GENERIC_ENC8, 3))
VOLUME_CONTROLS = ((GENERIC_SLI1, -1),
 (GENERIC_SLI2, -1),
 (GENERIC_SLI3, -1),
 (GENERIC_SLI4, -1),
 (GENERIC_SLI5, -1),
 (GENERIC_SLI6, -1),
 (GENERIC_SLI7, -1),
 (GENERIC_SLI8, -1))
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
CONTROLLER_DESCRIPTIONS = {u'INPUTPORT': u'PhotonX25',
 u'OUTPUTPORT': u'PhotonX25',
 u'CHANNEL': 0}
MIXER_OPTIONS = {u'NUMSENDS': 2,
 u'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1),
 u'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1),
 u'MASTERVOLUME': -1}
