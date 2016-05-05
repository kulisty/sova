import os
import git
import model

class Repository:

    def __init__(self, path, revision_from, revision_to):
        self.path = path
        self.revision_from = revision_from
        self.revision_to = revision_to
        self.repository = None

    def connect(self):
        try:
            if self.repository == None:
                self.repository = git.Repo(self.path)
        except git.exc.NoSuchPathError:
            self.repository = None

    def retrieve_files(self, commit='HEAD'):
        listing = self.repository.git.ls_tree('-r', '--name-only', commit).split('\n')
        files = [
            os.path.normpath(file)
            for file in listing
        ]
        return files

    def retrieve_commits(self):
        commits = [
            # commit.hexsha
            # commit.author.email
            # commit.parents
            commit
            for commit in self.repository.iter_commits()
        ]
        return commits
