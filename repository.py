import os
import git
import model
import sys

class Repository:

    def __init__(self, path, revision):
        self.path = path
        self.revision = revision
        # to be calculated
        self.repository = None
        self.origin = None

    def connect(self):
        try:
            if self.repository == None:
                self.repository = git.Repo(self.path)
                self.origin = self.repository.remotes.origin.url.replace(".git","")
                print("SOVA: Connected to <" + self.path + "> originated from <" + self.origin + ">")
        except git.exc.NoSuchPathError:
            sys.exit("SOVA: Path does not exist, aborting")
        except:
            sys.exit("SOVA: Could not connect to repository, aborting")

    def address_files(self, s):
        if s == ".":
            return self.origin.replace("/","\\")
        else:
            return (self.origin + "/blob/master/" + s).replace("/","\\")

    def address_commits(self, s):
        return (self.origin + "/commit/" + s).replace("/","\\")

    def retrieve_files(self):
        try:
            listing = self.repository.git.ls_tree('-r', '--name-only', self.revision).split('\n')
            files = [
                os.path.normpath(file)
                for file in listing
            ]
            return files
        except git.exc.GitCommandError as e:
            sys.exit("SOVA: Failed to execute git command (error {0}), aborting".format(e.status))
        except:
            sys.exit("SOVA: Failed to retrieve files, aborting")

    def retrieve_commits(self):
        try:
            commits = [
                # commit.hexsha
                # commit.author.email
                # commit.parents
                commit
                # for commit in self.repository.iter_commits('%s..%s' %(self.revision_from, self.revision_to))
                for commit in self.repository.iter_commits(self.revision)
            ]
            #family = ((commit.hexsha, parent.hexsha) for commit in commits for parent in commit.parents)
            #family = {(commit.hexsha, parent.hexsha) for commit in commits for parent in commit.parents}
            family = [(commit.hexsha, parent.hexsha) for commit in commits for parent in commit.parents]
            members = [(commit.hexsha) for commit in commits]
            return (members, family)
        except git.exc.GitCommandError as e:
            sys.exit("SOVA: Failed to execute git command (error {0}), aborting".format(e.status))
        except:
            sys.exit("SOVA: Failed to retrieve commits, aborting")
