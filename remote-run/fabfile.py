#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import os, sys

from fabric import api
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

HOME_DIR = '/home/tah35'
DEPLOY_DIR = os.path.join(HOME_DIR, 'deploy')
FUTZ_DIR = os.path.join(DEPLOY_DIR, 'gitfutz')
SUBJECT_DIR = os.path.join(HOME_DIR, 'subject')
ENV_DIR = os.path.join(DEPLOY_DIR, 'env')
SRCS_DIR = os.path.join(HOME_DIR, 'srcs')
DEPS_DIR = os.path.join(HOME_DIR, 'deps')

env.hosts = ['tah35@o405-u01.case.edu', 'tah35@o405-u02.case.edu',
             'tah35@o405-u04.case.edu']
#env.shell = 'PYTHONPATH=/home/tah35/lib/python ' + env.shell

def assert_dir_exists(path):
  '''checks if a directory exists. if not it creates it. if something exists
  and it is not a directory it exits with an error.
  '''

  with settings(warn_only=True):
    if run('test -d %s' % path).failed:
      run('mkdir %s' % path)
  return path

def _dir_exists(path):
  with settings(warn_only=True):
    not_exists = run('test -d %s' % path).failed
  return not not_exists

def deploy():
  with cd(assert_dir_exists(DEPLOY_DIR)):
    if not _dir_exists(FUTZ_DIR):
      run('git clone https://github.com/timtadh/gitfutz.git %s' % FUTZ_DIR)
  with cd(FUTZ_DIR):
    run('git clean -fdx')
    run('git pull')
    if not _dir_exists(ENV_DIR):
      mkenv()

def mkenv():
  run('/home/tah35/bin/virtualenv --no-site-packages %s' % ENV_DIR)

def install_cdeps():
  pass

def install_virtualenv():
  virdir = os.path.join(SRCS_DIR, 'virtualenv')
  if not _dir_exists(SRCS_DIR): run('mkdir %s' % SRCS_DIR)
  if not _dir_exists(DEPS_DIR): run('mkdir %s' % DEPS_DIR)
  if not _dir_exists(virdir):
    with cd(SRCS_DIR): run('git clone https://github.com/pypa/virtualenv.git')
  with cd(virdir):
    run('python setup.py install --home %s' % DEPS_DIR)
  load_rcs()

def install_cmake():
  url = 'http://www.cmake.org/files/v2.8/cmake-2.8.8.tar.gz'
  tarfile = os.path.join(SRCS_DIR, 'cmake-2.8.8.tar.gz')
  cmakedir = os.path.join(SRCS_DIR, 'cmake-2.8.8')
  archives = os.path.join(SRCS_DIR, 'archives')
  if not _dir_exists(SRCS_DIR): run('mkdir %s' % SRCS_DIR)
  if not _dir_exists(DEPS_DIR): run('mkdir %s' % DEPS_DIR)
  if not _dir_exists(archives): run('mkdir %s' % archives)
  if not _dir_exists(cmakedir):
    with cd(SRCS_DIR):
      run('wget %s' % url)
      run('tar xzf %s' % tarfile)
      run('mv %s %s' % (tarfile, archives))
  with cd(cmakedir):
    run('./configure --prefix=%s' % (DEPS_DIR))
    run('make')
    run('make install')
  load_rcs()

def load_rcs():
  api.put('./remote-bashrc', '~/.bashrc')
  api.put('./remote-profile', '~/.profile')

def getsubject():
  if _dir_exists(SUBJECT_DIR):
    run('rm -rf %s' % SUBJECT_DIR)
  run('git clone %s %s' % (raw_input('subject? '), SUBJECT_DIR))

