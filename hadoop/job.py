#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import sys, os, difflib

import pygit2
from mrjob.job import MRJob
from mrjob.util import bash_wrap
from editdist import distance as strdist

from gitfutz.astutils import tools

SUBJECTS_DIR = '/home/tah35/subjects'

def quick_strdist(a,b):
    return difflib.SequenceMatcher(None, a, b).real_quick_ratio()

def collect_files(files, tree, parents):
    for entry in tree:
        name = entry.name.encode('utf8')
        eobj = entry.to_object()
        if isinstance(eobj, pygit2.Tree): 
            collect_files(files, eobj, parents+[name])
        else:
            files[os.path.join(*(parents+[name]))] = eobj.oid.encode('hex')

class Sequence(MRJob):

    def steps(self):
        return [
          self.mr(mapper=self.commits),
          self.mr(mapper=self.commit_files),
          self.mr(
            mapper=self.commit_stats, 
            reducer=self.sum_stats,
            combiner=self.sum_stats),
          self.mr(
            mapper=self.normalize_stats_mapper, 
            reducer=self.normalize_stats_reducer),
        ]

    def get_commit(self, path, chex):
        repo = pygit2.Repository(path)
        commit = repo[chex.decode('hex')]
        return commit

    def commits(self, _, url):
        path = os.path.join(SUBJECTS_DIR, 
                            os.path.basename(url).replace('.git', ''))
        repo = pygit2.Repository(path)
        head = repo.lookup_reference('HEAD').resolve()
        for commit in repo.walk(head.oid, pygit2.GIT_SORT_REVERSE):
            yield path, commit.hex

    def commit_files(self, path, chex):
        commit = self.get_commit(path, chex)
        merge = 1 if len(commit.parents) > 1 else 0
        yield (path, chex), {
            'file_name': None,
            'parent_file': None,
            'commit_file': None,
            'merges': merge,
            'commits': 1
        }
        files1 = dict()
        collect_files(files1, commit.tree, list())
        for parent in commit.parents:
            files2 = dict()
            collect_files(files2, parent.tree, list())
            shared = set(files1.keys()) & set(files2.keys())
            for key in shared:
                if files1[key] == files2[key]: continue
                yield (path, chex), {
                    'file_name': key,
                    'parent_file': files1[key],
                    'commit_file': files2[key],
                    'merges': 0,
                    'commits': 0
                }

    def commit_stats(self, pc, d):
        path, chex = pc
        commit = self.get_commit(path, chex)
        if d['file_name'] is None: 
            yield (path, commit.author.email), (d['commits'], d['merges'], 0.0)
        else:
            repo = pygit2.Repository(path)
            f1 = repo[d['parent_file'].decode('hex')].data.replace('\r', '')
            f2 = repo[d['commit_file'].decode('hex')].data.replace('\r', '')
            yield (path, commit.author.email), (0, 0, quick_strdist(f1,f2))

    def sum_stats(self, pa, cms):
        path, author = pa
        cms = [cm for cm in cms]
        commits = map(lambda x: x[0], cms)
        merges = map(lambda x: x[1], cms)
        sdists = map(lambda x: x[2], cms)
        yield (path, author), (float(sum(commits)), float(sum(merges)),
            float(sum(sdists)))

    def normalize_stats_mapper(self, pa, cms):
        path, author = pa
        yield path, (author, cms[0], cms[1], cms[2])

    def normalize_stats_reducer(self, path, acms):
        t_commits = 0.0
        t_merges = 0.0
        t_sdist = 0.0
        c_acms = list()
        for author, commits, merges, sdist in acms:
            c_acms.append((author, commits, merges, sdist))
            t_commits += commits
            t_merges += merges
            t_sdist += sdist
        for author, commits, merges, sdist in c_acms:
            yield (path, author), ((commits/t_commits, merges/t_merges,
                sdist/t_sdist), (commits, merges, sdist))

if __name__ == '__main__':
    Sequence.run()

