#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import os, sys

def log(*msgs):
  '''Log a message to the user
  @varargs *msgs : a sequence of object to print'''
  for msg in msgs:
    print >>sys.stderr, str(msg),
  print >>sys.stderr
  sys.stderr.flush()

def output(*msgs):
  '''Output a piece of data (suitable for piping to others).
  @varargs *msgs : a sequence of object to print'''
  for msg in msgs:
    print >>sys.stdout, str(msg),
  print >>sys.stdout
  sys.stdout.flush()

