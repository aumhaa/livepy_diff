#Embedded file name: /Volumes/Jenkins2045_2/versonator2/Hudson/live/Projects/AppLive/Resources/MIDI Remote Scripts/VCM600/__init__.py
from VCM600 import VCM600

def create_instance(c_instance):
    """ Creates and returns the ADA1 script """
    return VCM600(c_instance)