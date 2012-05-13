#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import os, sys

error_codes = {
    'usage':1,
    'file_not_found':2,
    'option':3,
    'args':4,
    'version':5,
    'bad_bool':6,
    'no_args':7,
    'bad_module':9,
    'bad_file_read':10,
    'file_instead_of_dir':11,
}

short_usage_message = None
usage_message = None
extended_message = None


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

def usage(code=None):
  '''Prints the usage and exits with an error code specified by code. If code
  is not given it exits with error_codes['usage']'''
  log(short_usage_message)
  if code is None or code < 2:
    log(usage_message)
  if code is None:
    log(extended_message)
    code = error_codes['usage']
  sys.exit(code)

def assert_file_exists(path):
  '''checks if the file exists. If it doesn't causes the program to exit.
  @param path : path to file
  @returns : the path to the file (an echo) [only on success]
  '''
  path = os.path.abspath(os.path.expanduser(path))
  if not os.path.exists(path):
    log('No file found. "%(path)s"' % locals())
    usage(error_codes['file_not_found'])
  return path

def assert_dir_exists(path, nocreate=False):
  '''checks if a directory exists. if not it creates it. if something exists
  and it is not a directory it exits with an error.
  '''
  path = os.path.abspath(path)
  if not os.path.exists(path) and nocreate:
    log('No directory exists at location "%(path)s"' % locals())
    usage(error_codes['file_not_found'])
  elif not os.path.exists(path):
    os.mkdir(path)
  elif not os.path.isdir(path):
    log('Expected a directory found a file. "%(path)s"' % locals())
    usage(error_codes['file_instead_of_dir'])
  return path

def read_file_or_die(path):
  '''Reads the file, if there is an error it kills the program.
  @param path : the path to the file
  @returns string : the contents of the file
  '''
  path = assert_file_exists(path)
  try:
    f = open(path, 'r')
    s = f.read()
    f.close()
  except Exception:
    log('Error reading file at "%s".' % path)
    usage(error_codes['bad_file_read'])
  return s

