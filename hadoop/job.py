#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import sys, os, difflib, random, re
import logging
log = logging.getLogger("job")

import pygit2
from mrjob.job import MRJob
from mrjob.util import bash_wrap, log_to_stream
from editdist import distance as strdist
from sklearn import cluster

from gitfutz.astutils import tools

SUBJECTS_DIR = '/home/tah35/subjects'
log_to_stream("job", debug=True)

def quick_strdist(a,b):
    return difflib.SequenceMatcher(None, a, b).real_quick_ratio()

def collect_files(files, tree, parents):
    for entry in tree:
        name = entry.name.encode('utf8')
        try: eobj = entry.to_object()
        except:
            continue
        if isinstance(eobj, pygit2.Tree): 
            collect_files(files, eobj, parents+[name])
        else:
            files[os.path.join(*(parents+[name]))] = eobj.oid.encode('hex')

class Sequence(MRJob):

    def steps(self):
        return [
          self.mr(mapper=self.commits),
          self.mr(
            mapper=self.commit_stats, 
            reducer=self.sum_stats,
            combiner=self.sum_stats),
          self.mr(
            mapper=self.normalize_stats_mapper, 
            reducer=self.normalize_stats_reducer),
          self.mr(
            reducer=self.cluster_authors),
        ]

    def configure_options(self):
        super(Sequence, self).configure_options()
        self.add_passthrough_option('--sample', default=False,
            action='store_true',
            help='Should sampling occur?')
        self.add_passthrough_option('--sample-threshold', type='float',
            default=.4, help='What percentage of commits should be sampled?')

    def commits(self, _, url):
        self.increment_counter('job', 'commits calls', 1)
        name = re.sub(r'\.git$', r'', os.path.basename(url).strip())
        path = os.path.join(SUBJECTS_DIR, name)
        repo = pygit2.Repository(path)
        head = repo.lookup_reference('HEAD').resolve()
        for commit in repo.walk(head.oid, pygit2.GIT_SORT_REVERSE):
            if not self.options.sample: 
                self.increment_counter('job', 'commits to process', 1)
                yield path, commit.hex
            else:
                if random.random() < self.options.sample_threshold:
                    self.increment_counter('job', 'commits to process', 1)
                    yield path, commit.hex
                else:
                    print 'skipped', path, commit.hex

    def commit_stats(self, path, chex):
        self.increment_counter('job', 'commit_stats calls', 1)
        repo = pygit2.Repository(path)
        try:
            commit = repo[chex.decode('hex')]
        except:
            return
        log.debug(chex)
        merge = 1 if len(commit.parents) > 1 else 0
        yield (path, commit.author.email), (1, merge, 0.0)
        files1 = dict()
        collect_files(files1, commit.tree, list())
        for parent in commit.parents:
            files2 = dict()
            collect_files(files2, parent.tree, list())
            shared = set(files1.keys()) & set(files2.keys())
            for key in shared:
                if files1[key] == files2[key]: continue
                try:
                    f1 = repo[files1[key].decode('hex')].data.replace('\r', '')
                    f2 = repo[files2[key].decode('hex')].data.replace('\r', '')
                except:
                    continue
                try:
                    ## "binary" file check
                    f1 = f1.decode('utf8').encode('utf8')
                    f2 = f1.decode('utf8').encode('utf8')
                except UnicodeDecodeError:
                    continue
                log.debug(' '*4 + key)
                yield (path, commit.author.email), (0, 0, quick_strdist(f1,f2))
        self.increment_counter('job', 'commits processed', 1)

    def sum_stats(self, pa, cms):
        self.increment_counter('job', 'sum_stats calls', 1)
        path, author = pa
        t_commits = 0.0
        t_merges = 0.0
        t_sdist = 0.0
        for commits, merges, sdist in cms:
            t_commits += commits
            t_merges += merges
            t_sdist += sdist
        yield (path, author), (float(t_commits), float(t_merges),
            float(t_sdist))

    def normalize_stats_mapper(self, pa, cms):
        self.increment_counter('job', 'normalize_stats_mapper calls', 1)
        path, author = pa
        yield path, (author, cms[0], cms[1], cms[2])

    def normalize_stats_reducer(self, path, acms):
        self.increment_counter('job', 'normalize_stats_reducer calls', 1)
        def div(q, d): return q/d if d != 0.0 else 0.0
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
            yield path, (author, (
              (div(commits, t_commits), div(merges, t_merges), div(sdist, t_sdist)), 
              (commits, merges, sdist)
            ))
    
    def cluster_authors(self, path, acms):
        self.increment_counter('job', 'cluster_authors calls', 1)
        acms = tuple(i for i in acms)
        try:
            est = cluster.KMeans(k=min(max(len(acms)/2, 2), 4))
            est.fit([cms[0] for author, cms in acms])
            groups = tuple((author, est.predict(cms[0]).tolist()[0], cms)
                        for author, cms in acms)
        except:
            groups = tuple((author, -1, cms) for author, cms in acms)
        groups = sorted(groups, key=lambda x: x[1])
        for author, group, cms in groups:
            yield (path, author), {
              'group': group,
              'raw': {
                'commits':cms[1][0],
                'merges':cms[1][1],
                'sdist':cms[1][2],
              },
              'normalized': {
                'commits':cms[0][0],
                'merges':cms[0][1],
                'sdist':cms[0][2],
              },
            }

if __name__ == '__main__':
    Sequence.run()

