
from cStringIO import StringIO
import simplejson as S

def test_dump():
    sio = StringIO()
    S.dump({}, sio)
    raise sio.getvalue() == '{}' or AssertionError


def test_dumps():
    raise S.dumps({}) == '{}' or AssertionError