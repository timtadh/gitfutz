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

#subjects = {
#'tah35@o405-u01.case.edu':'https://github.com/pypa/virtualenv.git',
#'tah35@o405-u02.case.edu':'https://github.com/pypa/pip.git',
#'tah35@o405-u04.case.edu':'http://git.gnome.org/browse/gegl',
#'tah35@o405-u05.case.edu':'https://github.com/django/django.git',
#'tah35@o405-u06.case.edu':'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git',
#'tah35@o405-u07.case.edu':'https://github.com/facebook/tornado.git',
#'tah35@o405-u08.case.edu':'https://github.com/erlang/otp.git',
#'tah35@o405-u10.case.edu':'https://github.com/jquery/jquery.git',
#'tah35@o405-u11.case.edu':'https://github.com/nathanmarz/storm.git',
#'tah35@o405-u12.case.edu':'https://github.com/tenderlove/nokogiri.git',
#'tah35@o405-u13.case.edu':'https://github.com/antirez/redis.git',
#'tah35@o405-u14.case.edu':'https://github.com/mongodb/mongo.git',
#}
#subjects = {
#'tah35@o405-u01.case.edu':'https://github.com/twitter/bootstrap.git',
#'tah35@o405-u02.case.edu':'https://github.com/twitter/scalding.git',
#'tah35@o405-u04.case.edu':'https://github.com/twitter/scala_school.git',
#'tah35@o405-u05.case.edu':'https://github.com/twitter/util.git',
#'tah35@o405-u06.case.edu':'https://github.com/twitter/cassovary.git',
#'tah35@o405-u07.case.edu':'https://github.com/twitter/zipkin.git',
#'tah35@o405-u08.case.edu':'https://github.com/twitter/cassandra.git',
#'tah35@o405-u10.case.edu':'https://github.com/twitter/commons.git',
#'tah35@o405-u11.case.edu':'https://github.com/twitter/finagle.git',
#'tah35@o405-u12.case.edu':'https://github.com/twitter/activerecord-reputation-system.git',
#'tah35@o405-u13.case.edu':'https://github.com/twitter/twitter-cldr-rb.git',
#'tah35@o405-u14.case.edu':'https://github.com/twitter/twitter-text-rb.git',
#}
#subjects = {
#'tah35@o405-u01.case.edu':
#    'https://github.com/twitter/algebird',
#'tah35@o405-u02.case.edu':
#    'https://github.com/twitter/hdfs-du',
#'tah35@o405-u04.case.edu':
#    'https://github.com/twitter/ostrich',
#'tah35@o405-u05.case.edu':
#    'https://github.com/twitter/twitter-cldr-js',
#'tah35@o405-u06.case.edu':
#    'https://github.com/twitter/twemproxy',
#'tah35@o405-u07.case.edu':
#    'https://github.com/twitter/twitter-text-objc',
#'tah35@o405-u08.case.edu':
#    'https://github.com/twitter/twitter-text-java',
#'tah35@o405-u10.case.edu':
#    'https://github.com/twitter/pycascading',
#'tah35@o405-u11.case.edu':
#    'https://github.com/twitter/twitter-text-conformance',
#'tah35@o405-u12.case.edu':
#    'https://github.com/twitter/twitter-text-js',
#'tah35@o405-u13.case.edu':
#    'https://github.com/twitter/iago',
#'tah35@o405-u14.case.edu':
#    'https://github.com/twitter/recess',
#}

#subjects = {
#'tah35@o405-u01.case.edu':
#    'https://github.com/twitter/twitter.github.com',
#'tah35@o405-u02.case.edu':
#    'https://github.com/twitter/effectivescala',
#'tah35@o405-u04.case.edu':
#    'https://github.com/twitter/ambrose',
#'tah35@o405-u05.case.edu':
#    'https://github.com/twitter/hadoop-lzo',
#'tah35@o405-u06.case.edu':
#    'https://github.com/twitter/twemcache',
#'tah35@o405-u07.case.edu':
#    'https://github.com/twitter/snowflake',
#'tah35@o405-u08.case.edu':
#    'https://github.com/twitter/scrooge',
#'tah35@o405-u10.case.edu':
#    'https://github.com/twitter/hogan.js',
#'tah35@o405-u11.case.edu':
#    'https://github.com/twitter/elephant-twin-lzo',
#'tah35@o405-u12.case.edu':
#    'https://github.com/twitter/elephant-twin',
#'tah35@o405-u13.case.edu':
#    'https://github.com/twitter/cassie',
#'tah35@o405-u14.case.edu':
#    'https://github.com/twitter/twitter4j',
#}

#subjects = {
#'tah35@o405-u01.case.edu':
#    'https://github.com/twitter/bootstrap-server',
#'tah35@o405-u02.case.edu':
#    'https://github.com/twitter/twui',
#'tah35@o405-u04.case.edu':
#    'https://github.com/twitter/sbt-scrooge',
#'tah35@o405-u05.case.edu':
#    'https://github.com/twitter/naggati2',
#'tah35@o405-u06.case.edu':
#    'https://github.com/twitter/sbt-package-dist',
#'tah35@o405-u07.case.edu':
#    'https://github.com/twitter/gizzmo',
#'tah35@o405-u08.case.edu':
#    'https://github.com/twitter/flockdb',
#'tah35@o405-u10.case.edu':
#    'https://github.com/twitter/mahout',
#'tah35@o405-u11.case.edu':
#    'https://github.com/twitter/scala-bootstrapper',
#'tah35@o405-u12.case.edu':
#    'https://github.com/twitter/innovators-patent-agreement',
#'tah35@o405-u13.case.edu':
#    'https://github.com/twitter/twemperf',
#'tah35@o405-u14.case.edu':
#    'https://github.com/twitter/gizzard',
#}

#subjects = {
#'tah35@o405-u01.case.edu':
#    'https://github.com/twitter/ospriet',
#'tah35@o405-u02.case.edu':
#    'https://github.com/twitter/querulous',
#'tah35@o405-u04.case.edu':
#    'https://github.com/twitter/kestrel-client',
#'tah35@o405-u05.case.edu':
#    'https://github.com/twitter/standard-project',
#'tah35@o405-u06.case.edu':
#    'https://github.com/twitter/scrooge-runtime',
#'tah35@o405-u07.case.edu':
#    'https://github.com/twitter/jvmgcprof',
#'tah35@o405-u08.case.edu':
#    'https://github.com/twitter/cloudhopper-smpp',
#'tah35@o405-u10.case.edu':
#    'https://github.com/twitter/cloudhopper-commons-charset',
#'tah35@o405-u11.case.edu':
#    'https://github.com/twitter/scala-json',
#'tah35@o405-u12.case.edu':
#    'https://github.com/twitter/twitterActors',
#'tah35@o405-u13.case.edu':
#    'https://github.com/twitter/sbt-thrift',
#'tah35@o405-u14.case.edu':
#    'https://github.com/twitter/thrift_client',
#}

subjects = {
'tah35@o405-u01.case.edu':
    'https://github.com/twitter/streamyj',
'tah35@o405-u02.case.edu':
    'https://github.com/twitter/scala-zookeeper-client',
'tah35@o405-u04.case.edu':
    'https://github.com/twitter/joauth',
'tah35@o405-u05.case.edu':
    'https://github.com/twitter/haplocheirus',
'tah35@o405-u06.case.edu':
    'https://github.com/twitter/cloudhopper-commons-gsm',
'tah35@o405-u07.case.edu':
    'https://github.com/twitter/cloudhopper-commons-util',
'tah35@o405-u08.case.edu':
    'https://github.com/twitter/grabby-hands',
'tah35@o405-u10.case.edu':
    'https://github.com/twitter/webrat',
'tah35@o405-u11.case.edu':
    'https://github.com/twitter/mustache.js',
'tah35@o405-u12.case.edu':
    'https://github.com/twitter/rubyenterpriseedition187-248',
'tah35@o405-u13.case.edu':
    'https://github.com/twitter/flockdb-client',
'tah35@o405-u14.case.edu':
    'https://github.com/twitter/twitcher',
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
  install_cdeps()
  install_pydeps()
  test_futz()

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
  install_cmake()
  install_virtualenv()
  deploy()
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
  run('ps u -utah35')

def sequence():
  host = env.host_string
  url = subjects[host]
  subject = os.path.splitext(os.path.basename(url))[0]
  starttime = time.strftime('%Y-%m-%d_%H-%M-%S')
  outputname = 'sequence_%s_%s' % (subject, starttime)
  logname = 'log_sequence_%s_%s' % (subject, starttime)
  output = os.path.join(OUTPUT_DIR, outputname)
  logpath = os.path.join(OUTPUT_DIR, logname)
  localoutput = os.path.join('.', 'output')
  localhostout = os.path.join(localoutput, env.host_string)
  assert_dir_exists(OUTPUT_DIR)
  assert_local_dir_exists(localoutput)
  assert_local_dir_exists(localhostout)
  with settings(warn_only=True):
    with api.prefix(_load_env_prefix()):
      o = run('futz -r %s sequence 1> %s 2> %s' % (SUBJECT_DIR, output, logpath))
      print 'the return code =', o.return_code
  print 'FINISHED SEQUENCING'
  api.get(output, os.path.join(localhostout, outputname))
  api.get(logpath, os.path.join(localhostout, logname))

def merges():
  with settings(warn_only=True):
    with api.prefix(_load_env_prefix()):
      run('futz -r %s merges' % SUBJECT_DIR)

