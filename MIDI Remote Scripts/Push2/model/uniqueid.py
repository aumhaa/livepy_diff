
from __future__ import absolute_import, print_function
from itertools import count

class UniqueIdMixin(object):
    _idgen = count()

    def __init__(self, *a, **k):
        super(UniqueIdMixin, self).__init__(*a, **k)
        self.__id__ = self._idgen.next()