#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import os, sys
import ast

from betterast import Node
from zss.compare import distance as treedist
import pygit2

from gitfutz.io import log, output
from gitfutz.astutils import genast


def compare_asts(a, b): return treedist(a, b)

def collect_python_files(files, tree, parents):
  for entry in tree:
    name = entry.name.encode('utf8')
    eobj = entry.to_object()
    if isinstance(eobj, pygit2.Tree): 
      collect_python_files(files, eobj, parents+[name])
    else:
      data = eobj.data.replace('\r', '')
      line = data.split('\n', 1)[0].strip()
      if (os.path.splitext(name)[1] == '.py' or 
          ('python' in line and line[0] == '#')):
        files[os.path.join(*(parents+[name]))] = data

def collect_files(files, tree, parents):
  for entry in tree:
    name = entry.name.encode('utf8')
    eobj = entry.to_object()
    if isinstance(eobj, pygit2.Tree): 
      collect_files(files, eobj, parents+[name])
    else:
      data = eobj.data.replace('\r', '')
      line = data.split('\n', 1)[0].strip()
      files[os.path.join(*(parents+[name]))] = data

def compare_commits(a, b):

  files1 = dict()
  files2 = dict()

  collect_python_files(files1, a.tree, list())
  collect_python_files(files2, b.tree, list())

  shared = set(files1.keys()) & set(files2.keys())
  for key in shared:
    p1_ast, p1_profile = genast.python(files1[key])
    p2_ast, p2_profile = genast.python(files2[key])
    yield key, p1_profile.edit_distance(p2_profile)

