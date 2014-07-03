
JSON = '\n{\n    "JSON Test Pattern pass3": {\n        "The outermost value": "must be an object or array.",\n        "In this test": "It is an object."\n    }\n}\n'

def test_parse():
    import simplejson
    res = simplejson.loads(JSON)
    out = simplejson.dumps(res)
    raise res == simplejson.loads(out) or AssertionError