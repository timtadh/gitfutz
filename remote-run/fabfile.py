#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import os, sys, time

from fabric import api
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm

HOME_DIR = '/home/tah35'
OUTPUT_DIR = os.path.join(HOME_DIR, 'output')
DEPLOY_DIR = os.path.join(HOME_DIR, 'deploy')
FUTZ_DIR = os.path.join(DEPLOY_DIR, 'gitfutz')
SUBJECT_DIR = os.path.join(HOME_DIR, 'subject')
ENV_DIR = os.path.join(DEPLOY_DIR, 'env')
SRCS_DIR = os.path.join(HOME_DIR, 'srcs')
DEPS_DIR = os.path.join(HOME_DIR, 'deps')

subjects = {
'tah35@o405-u01.case.edu':'https://github.com/pypa/virtualenv.git', 
'tah35@o405-u02.case.edu':'https://github.com/pypa/pip.git', 
'tah35@o405-u04.case.edu':'http://git.gnome.org/browse/gegl', 
'tah35@o405-u05.case.edu':'https://github.com/django/django.git', 
'tah35@o405-u06.case.edu':'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git', 
'tah35@o405-u07.case.edu':'https://github.com/facebook/tornado.git',
'tah35@o405-u08.case.edu':'https://github.com/joyent/node.git', 
'tah35@o405-u10.case.edu':'https://github.com/jquery/jquery.git',
'tah35@o405-u11.case.edu':'https://github.com/nathanmarz/storm.git', 
'tah35@o405-u12.case.edu':'https://github.com/tenderlove/nokogiri.git',
'tah35@o405-u13.case.edu':'https://github.com/antirez/redis.git', 
'tah35@o405-u14.case.edu':'https://github.com/mongodb/mongo.git',
}

def assert_local_dir_exists(path, nocreate=False):
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

def assert_local_file_exists(path):
  '''checks if the file exists. If it doesn't causes the program to exit.
  @param path : path to file
  @returns : the path to the file (an echo) [only on success]
  '''
  path = os.path.abspath(os.path.expanduser(path))
  if not os.path.exists(path):
    log('No file found. "%(path)s"' % locals())
    usage(error_codes['file_not_found'])
  return path


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

def _load_env_prefix():
  swork = '.swork.activate'
  activate = os.path.join(ENV_DIR, 'bin', 'activate')
  futz_env = os.path.join(FUTZ_DIR, 'env')
  
  with settings(warn_only=True):
    not_exists = run('test -L %s' % futz_env).failed
  if not_exists:
    run('ln -s %s %s' % (FUTZ_DIR, futz_env))

  s = 'cd %s && source %s && source %s' % (FUTZ_DIR, swork, activate)
  return s

def add_public_key(keyfile, name):
  rfile = os.path.join(HOME_DIR, '.ssh', name)
  authorized_keys = os.path.join(HOME_DIR, '.ssh', 'authorized_keys')
  api.put(assert_local_file_exists(keyfile), rfile)
  run('cat %s >> %s' % (rfile, authorized_keys))

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
  run('virtualenv --no-site-packages %s' % ENV_DIR)

def install_cdeps():
  cdeps_dir = os.path.join(FUTZ_DIR, 'cdeps')
  srcs_dir = os.path.join(cdeps_dir, 'srcs')
  libgit2 = os.path.join(srcs_dir, 'libgit2')
  libgit2_build = os.path.join(libgit2, 'build')
  if _dir_exists(cdeps_dir): 
    run('rm -rf %s' % cdeps_dir)
  run('mkdir -p %s' % srcs_dir)
  with cd(srcs_dir):
    run('git clone https://github.com/libgit2/libgit2.git')
  with cd(libgit2):
    run('git checkout master')
    run('mkdir build')
  with cd(libgit2_build):
    run('cmake .. -DCMAKE_INSTALL_PREFIX=%s' % cdeps_dir)
    run('cmake --build . --target install')

def install_pydeps():
  pyreqs = os.path.join(FUTZ_DIR, 'python_requirements.txt')

  with api.prefix(_load_env_prefix()):
    run('pip install numpy')
    run('pip install scipy')
    run('pip install matplotlib')
    run('cat %s | xargs pip install' % pyreqs)

def install_virtualenv():
  virdir = os.path.join(SRCS_DIR, 'virtualenv')
  if not _dir_exists(SRCS_DIR): run('mkdir %s' % SRCS_DIR)
  if not _dir_exists(DEPS_DIR): run('mkdir %s' % DEPS_DIR)
  if not _dir_exists(virdir):
    with cd(SRCS_DIR): run('git clone https://github.com/pypa/virtualenv.git')
  with cd(virdir):
    run('python setup.py install --home %s' % DEPS_DIR)

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

def install_subjects():
  host = env.host_string
  url = subjects[host]
  if _dir_exists(SUBJECT_DIR):
    run('rm -rf %s' % SUBJECT_DIR)
  run('git clone %s %s' % (url, SUBJECT_DIR))

def install():
  load_rcs()
  install_virtualenv()
  deploy()
  install_cmake()
  install_cdeps()
  install_pydeps()
  install_subjects()
  test_futz()

def test_cmake():
  run('cmake')

def test_pygit2():
  with api.prefix(_load_env_prefix()):
    run("python -c 'import pygit2; print pygit2'")

def test_futz():
  with settings(warn_only=True):
    with api.prefix(_load_env_prefix()):
      o = run("futz --help")
      assert o.return_code == 1

def load_rcs():
  api.put('./remote-bashrc', '~/.bashrc')
  api.put('./remote-profile', '~/.profile')

def getsubject():
  if _dir_exists(SUBJECT_DIR):
    run('rm -rf %s' % SUBJECT_DIR)
  run('git clone %s %s' % (raw_input('subject? '), SUBJECT_DIR))

def clean_output():
  if _dir_exists(OUTPUT_DIR): run('rm -rf %s' % OUTPUT_DIR)

def check_processes():
  run('ps -u')

def sequence():
  host = env.host_string
  url = subjects[host]
  subject = os.path.splitext(os.path.basename(url))[0]
  starttime = time.strftime('%Y-%m-%d_%H-%M-%S')
  outputname = 'sequence_%s_%s' % (subject, starttime)
  output = os.path.join(OUTPUT_DIR, outputname)
  localoutput = os.path.join('.', 'output')
  localhostout = os.path.join(localoutput, env.host_string)
  assert_dir_exists(OUTPUT_DIR)
  assert_local_dir_exists(localoutput)
  assert_local_dir_exists(localhostout)
  with settings(warn_only=True):
    with api.prefix(_load_env_prefix()):
      o = run('futz -r %s sequence > %s' % (SUBJECT_DIR, output))
      print 'the return code =', o.return_code
  print 'FINISHED SEQUENCING'
  api.get(output, os.path.join(localhostout, outputname))

def merges():
  with api.prefix(_load_env_prefix()):
    run('futz -r %s merges' % SUBJECT_DIR)

