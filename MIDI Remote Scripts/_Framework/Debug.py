
enable_debug_output = True

def debug_print(*a):
    """ Special function for debug output """
    if enable_debug_output:
        print ' '.join(map(str, a))