
from __future__ import absolute_import, print_function, unicode_literals
PORTS_KEY = u'ports'
CONTROLLER_ID_KEY = u'controller_id'
TYPE_KEY = u'surface_type'
FIRMWARE_KEY = u'firmware_version'
AUTO_LOAD_KEY = u'auto_load'
VENDORID = u'vendor_id'
PRODUCTIDS = u'product_ids'
MODEL_NAMES = u'model_names'
DIRECTIONKEY = u'direction'
PORTNAMEKEY = u'name'
MACNAMEKEY = u'mac_name'
PROPSKEY = u'props'
HIDDEN = u'hidden'
SYNC = u'sync'
SCRIPT = u'script'
NOTES_CC = u'notes_cc'
REMOTE = u'remote'
PLAIN_OLD_MIDI = u'plain_old_midi'

def __create_port_dict(direction, port_name, mac_name, props):
    if not isinstance(direction, basestring):
        raise AssertionError
        raise isinstance(port_name, basestring) or AssertionError
        raise props == None or type(props) is list or AssertionError
        if props:
            for prop in props:
                raise isinstance(prop, basestring) or AssertionError

        raise mac_name == None or isinstance(mac_name, basestring) or AssertionError
        capabilities = {DIRECTIONKEY: direction,
         PORTNAMEKEY: port_name,
         PROPSKEY: props}
        capabilities[MACNAMEKEY] = mac_name and mac_name
    return capabilities


def inport(port_name = u'', props = [], mac_name = None):
    u""" Generate a ..."""
    return __create_port_dict(u'in', port_name, mac_name, props)


def outport(port_name = u'', props = [], mac_name = None):
    u""" Generate a ..."""
    return __create_port_dict(u'out', port_name, mac_name, props)


def controller_id(vendor_id, product_ids, model_name):
    u""" Generate a hardwareId dict"""
    raise type(vendor_id) is int or AssertionError
    raise type(product_ids) is list or AssertionError
    for product_id in product_ids:
        raise type(product_id) is int or AssertionError

    raise isinstance(model_name, (basestring, list)) or AssertionError
    model_names = model_name if type(model_name) is list else [model_name]
    return {VENDORID: vendor_id,
     PRODUCTIDS: product_ids,
     MODEL_NAMES: model_names}