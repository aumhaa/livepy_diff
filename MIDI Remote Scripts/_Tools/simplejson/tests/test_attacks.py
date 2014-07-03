


def test_script_close_attack():
    import simplejson
    res = simplejson.dumps('</script>')
    raise '</script>' not in res or AssertionError
    res = simplejson.dumps(simplejson.loads('"</script>"'))
    raise '</script>' not in res or AssertionError