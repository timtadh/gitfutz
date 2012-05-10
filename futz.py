#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.


import os, sys
from getopt import getopt, GetoptError

import pygit2

VERSION = 'git master'

error_codes = {
    'usage':1,
    'file_not_found':2,
    'option':3,
    'args':4,
    'version':5,
    'bad_bool':6,
    'no_args':7,
    'bad_module':9,
    'file_instead_of_dir':11,
}

usage_message = \
'''usage: gitfutz -r <repo> [sub command]'''

extended_message = \
'''
Options

    -h, help                            print this message
    -v, version                         print the version
    -r, repo=<repo>                     the repository to operate on

Sub Commands

    Here sub commands will be documented

Specs
    <file> = a path to a file
    <module> = "a.x.b" a fully qualified import path of a module. Must be on the
               PYTHONPATH. Can be relative to the current working directory
    <repo> = a path to the git repository as loadable by pygit2
'''


def log(*msgs):
  for msg in msgs:
      print >>sys.stderr, msg,
  print >>sys.stderr
  sys.stderr.flush()

def output(*msgs):
  for msg in msgs:
      print >>sys.stdout, msg,
  print >>sys.stdout
  sys.stdout.flush()

def version():
  '''Print version and exits'''
  log('fuzzbuzz version :', VERSION)
  sys.exit(error_codes['version'])

def main(args):

  short_opts =  'hvr:'
  long_opts = [
    'help', 'version', 'repo='
  ]

  try:
    opts, args = getopt(args, short_opts, long_opts)
  except GetoptError, err:
    log(err)
    usage(error_codes['option'])

  for opt, arg in opts:
    if opt in ('-h', '--help'):
      usage()
    elif opt in ('-v', '--version'):
      version()
  pass


if __name__ == '__main__':
  main(sys.argv[1:])

