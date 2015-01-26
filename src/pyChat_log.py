#!/usr/bin/env python
#-------------------------------------------------------------------------------
'''
.. module:: pyChat_log.py
'''

import logging

pyChat_handler1 = logging.StreamHandler(sys.stderr)
pyChat_handler1.setFormatter(logging.Formatter('%(asctime)s : %(name)s %(levelname)s : %(filename)s %(funcName)s %(lineno)d - %(message)s'))

pyChat_log = logging.getLogger('pyChat')
pyChat_log.propagate = False
pyChat_log.setLevel(logging.NOTSET)
pyChat_log.addHandler(pyChat_handler1)

del pyChat_handler1
