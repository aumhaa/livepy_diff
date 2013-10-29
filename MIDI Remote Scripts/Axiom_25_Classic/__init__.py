#Embedded file name: /Volumes/Jenkins2045_2/versonator2/Hudson/live/Projects/AppLive/Resources/MIDI Remote Scripts/Axiom_25_Classic/__init__.py
from Axiom import Axiom

def create_instance(c_instance):
    return Axiom(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[408], model_name='USB Axiom 25'),
     PORTS_KEY: [inport(props=[NOTES_CC, SCRIPT]), inport(props=[PLAIN_OLD_MIDI]), outport(props=[SCRIPT])]}