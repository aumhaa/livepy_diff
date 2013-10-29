#Embedded file name: /Applications/Ableton Live 9.05 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Livid_Base/__init__.py
from Base import Base

def create_instance(c_instance):
    """ Creates and returns the Base script """
    return Base(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[115], model_name='Livid Instruments Base'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}