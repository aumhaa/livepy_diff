
JSON = '\n[[[[[[[[[[[[[[[[[[["Not too deep"]]]]]]]]]]]]]]]]]]]\n'

def test_parse():
    import simplejson
    res = simplejson.loads(JSON)
    out = simplejson.dumps(res)
    raise res == simplejson.loads(out) or AssertionError