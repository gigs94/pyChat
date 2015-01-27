#!/usr/bin/env python
#-------------------------------------------------------------------------------
'''
.. module:: pyChat_log.py
'''

import sys
import logging

pyChat_handler1 = logging.StreamHandler(sys.stderr)
pyChat_handler1.setFormatter(logging.Formatter('%(asctime)s : %(name)s %(levelname)s : %(filename)s %(funcName)s %(lineno)d - %(message)s'))

log = logging.getLogger('pyChat')
log.propagate = False
log.setLevel(logging.DEBUG)
log.addHandler(pyChat_handler1)
