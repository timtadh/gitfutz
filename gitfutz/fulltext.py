#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import os, sys
from getopt import getopt, GetoptError

import pygit2
from tst.suffix import SuffixTree

from gitfutz.io import output, log


def index(repo, exts, excludes):
  '''Construct a fulltext (in-memory) index of the repository'''
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
      eobj = entry.to_object()
      if isinstance(eobj, pygit2.Tree): walk(eobj, i+2)
      else: add(entry.name.encode('utf8'), eobj, commit.hex, entry.hex)

  head = repo.lookup_reference('HEAD').resolve()
  for commit in repo.walk(head.oid, pygit2.GIT_SORT_REVERSE):
    log(commit.hex, commit.tree)
    walk(commit.tree)
  return index

def query_index(index, query):
  '''Perform a query on the index.'''
  for key, objs in index.find(query):
    yield key, (co for co in objs)


