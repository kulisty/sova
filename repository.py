import os
import git
import model
import sys

class Repository:

    def __init__(self, path, revision_from, revision_to):
        self.path = path
        self.revision_from = revision_from
        self.revision_to = revision_to
        self.repository = None
        self.origin = None

    def connect(self):
        try:
            if self.repository == None:
                self.repository = git.Repo(self.path)
                self.origin = self.repository.remotes.origin.url.replace(".git","")
                print("SOVA: Connected to <" + self.path + "> originated from <" + self.origin + ">")
        except git.exc.NoSuchPathError:
            sys.exit("SOVA: Repository does not exist, aborting")

    def address_files(self, s):
        if s == ".":
            return self.origin.replace("/","\\")
        else:
            return (self.origin + "/blob/master/" + s).replace("/","\\")

    def address_commits(self, s):
        return (self.origin + "/commit/" + s).replace("/","\\")

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
            # for commit in self.repository.iter_commits('%s..%s' %(self.revision_from, self.revision_to))
            for commit in self.repository.iter_commits()
        ]
        #family = ((commit.hexsha, parent.hexsha) for commit in commits for parent in commit.parents)
        #family = {(commit.hexsha, parent.hexsha) for commit in commits for parent in commit.parents}
        family = [(commit.hexsha, parent.hexsha) for commit in commits for parent in commit.parents]
        return family
