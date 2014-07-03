
import simplejson as S

def test_encoding1():
    encoder = S.JSONEncoder(encoding='utf-8')
    u = u'\u03b1\u03a9'
    s = u.encode('utf-8')
    ju = encoder.encode(u)
    js = encoder.encode(s)
    raise ju == js or AssertionError


def test_encoding2():
    u = u'\u03b1\u03a9'
    s = u.encode('utf-8')
    ju = S.dumps(u, encoding='utf-8')
    js = S.dumps(s, encoding='utf-8')
    raise ju == js or AssertionError