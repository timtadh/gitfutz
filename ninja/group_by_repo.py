
import os, sys, json

import mrjob
from mrjob.job import MRJob
from optutils import output, log, error_codes, add_code

def parse_json(fin):
    def decode(line):
        try:
            #log(line)
            return True, json.loads(line), None
        except ValueError, e:
            if e.message.startswith('Extra data:'):
                log('doubled lines')
                split =  int(e.message.split('(', 1)[1].
                                       split('-', 1)[0].
                                       replace('char ', ''))
                r = line[:split].encode('utf8')
                l = line[split:].encode('utf8')
                return False, None, (r, l)
            log(e)
            #log('skipped', "'%s'" % line)
            if e.message == 'No JSON object could be decoded':
                return False, None, None
            raise
        except Exception, e:
            log(e)
            log('skipped', line)
            raise

    def proc(lines):
        for line in lines:
            if not line: continue
            line = line.decode('utf8', 'ignore')
            ok, data, retry = decode(line)
            if ok:
                yield data
            elif retry:
                for data in proc(retry):
                    yield data

    for i, data in enumerate(proc(fin)):
        #if i % 10000 == 0: log(i, data)
        yield data

def get_repo(data):
    repo = data.get('repo', None)
    if repo is None:
        repo = data.get('repository', dict())
    if repo.get('name', '/') == '/':
        #print data.get('payload'), data.get('type')
        repo = data.get('payload', dict()).get('repo')
        #print data, repo, data.get('type')
        if repo is None and data.get('type') == 'CreateEvent':
            obj = data.get('payload', dict()).get('object')
            user_name = data.get('actor', dict()).get('login', '')
            #print obj
            if obj in ('repository', 'branch', 'tag'):
                #print data
                repo_name = data.get('payload', dict()).get('name', '')
                return '/'.join((repo_name, user_name))
            return None
        return repo
    else:
        return repo.get('name')

class Job(MRJob):

    INPUT_PROTOCOL = mrjob.protocol.RawValueProtocol
    INTERNAL_PROTOCOL = mrjob.protocol.JSONProtocol
    OUTPUT_PROTOCOL = mrjob.protocol.JSONProtocol

    def format_output(self, key, value):
        return json.dumps({'repo':key, 'events':value})

    def mapper(self, _, line):
        for line in parse_json([line]):
            if line['type'] == 'GistEvent': continue
            if line['type'] == 'FollowEvent': continue
            if line['type'] == 'DownloadEvent': continue
            if line['type'] == 'DeleteEvent': continue
            repo = get_repo(line)
            if repo is None: raise Exception
            if line['type'] != 'PullRequestEvent': continue
            if repo == '/':
                print get_repo(line), line['type'], line['payload']
                raise Exception
            else:
                yield repo, line

    def reducer(self, repo, events):
        yield repo, list(events)

if __name__ == '__main__':
    Job.run()

