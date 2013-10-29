#Embedded file name: /Applications/Ableton Live 9.05 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Livid_OhmModes/__init__.py
from OhmModes import OhmModes

def create_instance(c_instance):
    """ Creates and returns the OhmModes script """
    return OhmModes(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[115], model_name='Livid OhmRGB'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}