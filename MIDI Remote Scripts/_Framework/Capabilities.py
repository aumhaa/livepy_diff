from __future__ import absolute_import, print_function
PORTS_KEY = 'ports'
CONTROLLER_ID_KEY = 'controller_id'
TYPE_KEY = 'surface_type'
FIRMWARE_KEY = 'firmware_version'
AUTO_LOAD_KEY = 'auto_load'
VENDORID = 'vendor_id'
PRODUCTIDS = 'product_ids'
MODEL_NAMES = 'model_names'
DIRECTIONKEY = 'direction'
PORTNAMEKEY = 'name'
MACNAMEKEY = 'mac_name'
PROPSKEY = 'props'
HIDDEN = 'hidden'
SYNC = 'sync'
SCRIPT = 'script'
NOTES_CC = 'notes_cc'
REMOTE = 'remote'
PLAIN_OLD_MIDI = 'plain_old_midi'

def __create_port_dict(direction, port_name, mac_name, props):
    assert type(direction) is str
    assert type(port_name) is str
    assert props == None or type(props) is list
    if props:
        for prop in props:
            assert type(prop) is str

    assert mac_name == None or type(mac_name) is str
    capabilities = {DIRECTIONKEY: direction,
     PORTNAMEKEY: port_name,
     PROPSKEY: props}
    if mac_name:
        capabilities[MACNAMEKEY] = mac_name
    return capabilities


def inport(port_name = '', props = [], mac_name = None):
    """ Generate a ..."""
    return __create_port_dict('in', port_name, mac_name, props)


def outport(port_name = '', props = [], mac_name = None):
    """ Generate a ..."""
    return __create_port_dict('out', port_name, mac_name, props)


def controller_id(vendor_id, product_ids, model_name):
    """ Generate a hardwareId dict"""
    assert type(vendor_id) is int
    assert type(product_ids) is list
    for product_id in product_ids:
        assert type(product_id) is int

    assert type(model_name) is str or type(model_name) is list
    if type(model_name) is str:
        model_names = [model_name]
    else:
        model_names = model_name
    return {VENDORID: vendor_id,
     PRODUCTIDS: product_ids,
     MODEL_NAMES: model_names}
