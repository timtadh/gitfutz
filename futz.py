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
    'bad_file_read':10,
    'file_instead_of_dir':11,
}

short_usage_message = \
'''usage: gitfutz -r <repo> [sub command]'''

usage_message = \
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

extended_message = ''

def log(*msgs):
  '''Log a message to the user'''
  for msg in msgs:
    print >>sys.stderr, str(msg),
  print >>sys.stderr
  sys.stderr.flush()

def output(*msgs):
  '''Output a piece of data (suitable for piping to others).'''
  for msg in msgs:
    print >>sys.stdout, str(msg),
  print >>sys.stdout
  sys.stdout.flush()

def version():
  '''Print version and exits'''
  log('fuzzbuzz version :', VERSION)
  sys.exit(error_codes['version'])

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

def command(f):
  '''A decorator to mark a function as shell sub-command.'''
  setattr(f, 'command', True)
  return f

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

@command
def commits(repo):
  head = repo.lookup_reference('HEAD').resolve()
  for commit in repo.walk(head.oid, pygit2.GIT_SORT_REVERSE):
    output(commit.hex, commit.author.email, [p.hex for p in commit.parents])

commands = dict((name, attr)
  for name, attr in locals().iteritems()
  if hasattr(attr, 'command') and attr.command == True
)

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

  repo = None
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      usage()
    elif opt in ('-v', '--version'):
      version()
    elif opt in ('-r', '--repo'):
      repo = pygit2.Repository(assert_dir_exists(arg, nocreate=True))

  if len(args) == 0:
    log('must supply a subcommand')
    usage(error_codes['option'])
  
  sub_cmd = args[0]
  if sub_cmd not in commands:
    log('command %s is not available' % sub_cmd)
    usage(error_codes['option'])

  if repo is None:
    log('must supply a repository to operate on')
    usage(error_codes['option'])

  cmd = commands[sub_cmd]
  if cmd.func_code.co_argcount == 2:
    cmd(repo, args[1:])
  else:
    cmd(repo)

if __name__ == '__main__':
  main(sys.argv[1:])

