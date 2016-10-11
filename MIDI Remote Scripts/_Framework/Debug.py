
from __future__ import absolute_import, print_function
enable_debug_output = True

def debug_print(*a):
    """ Special function for debug output """
    if enable_debug_output:
        print(' '.join(map(str, a)))