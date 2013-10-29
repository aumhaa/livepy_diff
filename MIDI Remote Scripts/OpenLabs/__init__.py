#Embedded file name: /Volumes/Jenkins2045_2/versonator2/Hudson/live/Projects/AppLive/Resources/MIDI Remote Scripts/OpenLabs/__init__.py
import Live
from OpenLabs import OpenLabs

def create_instance(c_instance):
    """ Creates and returns the OpenLabs script """
    return OpenLabs(c_instance)