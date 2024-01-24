"""
## CTGP-7 Tools
"""

VERBOSE = False

def vprint(*s, **kwd):
    if VERBOSE: print(*s, **kwd)

from . import mystuff, misc