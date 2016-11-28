import argparse
import time
import io
import os
import sys
import collections
import repository
import model
import json
import files
import commits
import functions
import features
import ast

def parse_arguments():
    try:
        parser = argparse.ArgumentParser(
            description="Build architecture warehouse for a software project",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument(
            'path', help="path to repository")
        parser.add_argument(
            '-rev', help="build for revision REV", default='HEAD')
        # parser.add_argument(
        #     '-rev_from', help="build from revision REV_FROM", default='HEAD~8')
        # parser.add_argument(
        #     '-rev_to', help="build to revision REV_TO", default='HEAD')
        return parser.parse_args()
    except SystemExit:
        sys.exit("SOVA: Error parsing arguments, aborting")

def run():
    args = parse_arguments()
    # repo = repository.Repository(args.path, args.rev, args.rev_from, args.rev_to)
    repo = repository.Repository(args.path, args.rev)
    repo.connect()

    files.output(repo, './data/files/'+repo.name+'#'+repo.commit)
    #commits.output(repo, './data/commits')
    #functions.output(repo, './data/functions')
    #features.output(repo, './data/features')

    #archive = model.Archive(None, None, None, None)
    #archive.project = model.Project(repo.origin, repo.commit, repo.owner, repo.name)
    #archive.commits = commits.retrieve(repo)
    #archive.files = files.retrieve(repo)
    #archive.functions = features.retrieve(repo)
    #with open('./data/'+repo.name+'@'+repo.owner+'#'+repo.commit+'.json', 'wb+') as out_json:
    #    json.dump(archive, out_json, default=model.default, indent=2)

    sys.exit("SOVA: Software warehouse successfully generated")

if __name__ == '__main__':
    run()
