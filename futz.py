#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.


import os, sys
from getopt import getopt, GetoptError

import pygit2
from tst import TST
from tst.suffix import SuffixTree

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

@command
def merges(repo):
  head = repo.lookup_reference('HEAD').resolve()
  total_merges = 0
  merger = dict()
  merge_from = dict()
  for commit in repo.walk(head.oid, pygit2.GIT_SORT_REVERSE):
    if len(commit.parents) < 2: continue
    total_merges += 1
    email = commit.author.name.encode('utf8')
    merger[email] = merger.get(email, 0) + 1
    mfrom = [p.author.name.encode('utf8') for p in commit.parents if email !=
        p.author.name.encode('utf8')]
    for pe in mfrom:
      merge_from[email] = merge_from.get(email, dict())
      merge_from[email][pe] = merge_from[email].get(pe, 0) + 1
    output(
      commit.hex, email, mfrom
    )
  output()
  for email, count in merger.iteritems():
    output(email, count, float(count)/float(total_merges))
  output()
  output()
  outs = list()
  for email, froms in merge_from.iteritems():
    for pe, count in froms.iteritems():
      outs.append((email, pe, count, float(count)/float(total_merges)))
  outs = sorted(outs, key=lambda x:x[3])
  output('\n'.join(' '.join(str(col) for col in line) for line in outs))

@command
def index(repo, args):

  def cmd_usage():
    log("index all commits with extensions given by -x")
    usage()

  short_opts =  'hx:'
  long_opts = [
    'help', 'extension=', 'exclude='
  ]

  try:
    opts, args = getopt(args, short_opts, long_opts)
  except GetoptError, err:
    log(err)
    usage(error_codes['option'])

  exts = set()
  excludes = set()
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      cmd_usage()
    elif opt in ('-x', '--extension'):
      exts.add(arg)
    elif opt in ('--exclude',):
      excludes.add(arg)
  log(exts)
 
  index = SuffixTree()
  def add(name, obj, commitid, objid):
    if os.path.splitext(name)[1][1:] not in exts: return
    if name in excludes: return
    log('------->', name)
    data = obj.data.replace('\r', '')
    for line in obj.data.split('\n'):
      objs = index.get(line, set())
      notin = not bool(objs)
      objs.add((commitid, objid))
      if notin: index[line] = objs

  def walk(tree, i=2):
    for entry in tree:
      log(' '*i, entry.name.encode('utf8'))
      eobj = entry.to_object()
      if isinstance(eobj, pygit2.Tree): walk(eobj, i+2)
      else: add(entry.name.encode('utf8'), eobj, commit.hex, entry.hex)

  head = repo.lookup_reference('HEAD').resolve()
  for commit in repo.walk(head.oid, pygit2.GIT_SORT_REVERSE):
    log(commit.hex, commit.tree)
    walk(commit.tree)

  while True:
    query = raw_input('> ')
    if not query: break
    for key, objs in index.find(query):
      output(key)
      for commitid, objid in objs:
        output(' '*4, commitid, objid)


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

