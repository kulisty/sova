import argparse
import time
import io
import os
import sys
import repository
import model
import files

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Build architecture warehouse for a software project",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'path', help="path to repository")
    parser.add_argument(
        '-rev_from', help="build from revision REV_FROM", default='HEAD~32')
    parser.add_argument(
        '-rev_to', help="build to revision REV_TO", default='HEAD')
    return parser.parse_args()

def run():
    args = parse_arguments()
    repo = repository.Repository(args.path, args.rev_from, args.rev_to)
    repo.connect()
    files.output(repo, 'files')
    sys.exit("SOVA: Software warehouse successfully generated")
 
if __name__ == '__main__':
    run()
