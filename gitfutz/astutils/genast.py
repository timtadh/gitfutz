#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import os, sys
import ast

from betterast import Node
from pygram import Profile

from gitfutz.io import log, output

def python(text):

  def construct(pynode):
    name = pynode.__class__.__name__
    node = Node(name)
    for attr_name, attrs in ast.iter_fields(pynode):
      if attrs is None: continue
      if hasattr(attrs, '__len__') and len(attrs) == 0: continue
      attr_node = Node(attr_name)
      node.addkid(attr_node)
      if hasattr(attrs, '__iter__'):
        for attr in attrs:
          if issubclass(attr.__class__, ast.AST):
            attr_node.addkid(construct(attr))
          else:
            attr_node.addkid(Node(str(attr)))
      elif issubclass(attrs.__class__, ast.AST):
        attr_node.addkid(construct(attrs))
      else:
        if isinstance(attrs, unicode):
          attrs = attrs.encode('utf8')
        attr_node.addkid(Node(str(attrs)))
    return node

  try:
    pyast = ast.parse(text)
  except SyntaxError:
    return None, None
  newast = construct(pyast)
  return newast, Profile(newast)

