import argparse
import time
import io
import os
import sys
import repository
import model
import files
import commits
import functions
import features

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
    files.output(repo, './data/files')
    commits.output(repo, './data/commits')
    functions.output(repo, './data/functions')
    features.output(repo, './data/features')
    sys.exit("SOVA: Software warehouse successfully generated")

if __name__ == '__main__':
    run()
