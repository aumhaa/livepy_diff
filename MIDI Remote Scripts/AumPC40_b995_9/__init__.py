#Embedded file name: /Applications/Ableton Live 9 Standard.app/Contents/App-Resources/MIDI Remote Scripts/AumPC40_b995_9/__init__.py
from AumPC40 import AumPC40

def create_instance(c_instance):
    """ Creates and returns the AumPC40 script """
    return AumPC40(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[115], model_name='Akai APC40'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}