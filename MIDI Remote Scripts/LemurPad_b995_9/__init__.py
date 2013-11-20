#Embedded file name: /Applications/Ableton Live 9 Standard.app/Contents/App-Resources/MIDI Remote Scripts/LemurPad_b995_9/__init__.py
from LemurPad import LemurPad

def create_instance(c_instance):
    """ Creates and returns the LemaurPad script """
    return LemurPad(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=2536, product_ids=[115], model_name='Lemur'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT, REMOTE]), outport(props=[SCRIPT, REMOTE])]}