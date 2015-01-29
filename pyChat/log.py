#!/usr/bin/env python
#-------------------------------------------------------------------------------
'''
.. module:: pyChat.log.py
'''

import sys
import logging

loghandler1 = logging.StreamHandler(sys.stderr)
loghandler1.setFormatter(logging.Formatter('%(asctime)s : %(name)s %(levelname)s : %(filename)s %(funcName)s %(lineno)d - %(message)s'))

log = logging.getLogger('pyChat')
log.propagate = False
log.setLevel(logging.DEBUG)
log.addHandler(loghandler1)
