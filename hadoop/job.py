import re

from mrjob.job import MRJob
from mrjob.util import bash_wrap

import pygit2

class MRWordFreqCount(MRJob):

    def mapper(self, _, path):
        repo = pygit2.Repository(path)
        head = repo.lookup_reference('HEAD').resolve()
        for commit in repo.walk(head.oid, pygit2.GIT_SORT_REVERSE):
            yield commit.author.email, 1

    def combiner(self, author, counts):
        yield author, sum(counts)

    def reducer(self, author, counts):
        yield author, sum(counts)


if __name__ == '__main__':
    MRWordFreqCount.run()
