#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import os, sys
import ast

from betterast import Node
from zss.compare import distance as treedist

from gitfutz.io import log, output


def compare_asts(a, b): return treedist(a, b)

