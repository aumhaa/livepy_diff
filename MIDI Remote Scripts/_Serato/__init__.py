
from __future__ import absolute_import, print_function, unicode_literals
from .Serato import Serato
HIDE_SCRIPT = True

def create_instance(c_instance):
    u""" Creates and returns the Serato script """
    return Serato(c_instance)