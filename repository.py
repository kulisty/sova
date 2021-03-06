import os
import re
import git
import model
import sys
import collections
from radon import visitors
#from pygithub3 import Github

class FunctionsVisitor(visitors.CodeVisitor):
    def __init__(self, file=''):
        self.functions = []
        self.file = file

    def visit_FunctionDef(self, node):
        self.functions.append(Function(node.name, self.file, node.lineno))
        for child in node.body:
            self.visit(child)

class FeaturesVisitor(visitors.CodeVisitor):
    def __init__(self, file='', code_lines=[]):
        self.features = []
        self.file = file
        self.code_lines = code_lines

    def visit_FunctionDef(self, node):
        complexity_visitor = visitors.ComplexityVisitor.from_ast(node)
        start_line = node.lineno - 1
        end_line = complexity_visitor.functions[0].endline
        # vector of features, only complexity for the time being
        features = [
            #complexity_visitor.functions[0].complexity,
            complexity_visitor.functions[0].complexity,

        ]
        self.features.append(Feature(node.name, self.file, node.lineno, features))
        for child in node.body:
            self.visit(child)

File = collections.namedtuple('File', ['filename', 'file', 'path'])
Commit = collections.namedtuple('Commit', [])
Function = collections.namedtuple('Function', ['functionname', 'file', 'lineno'])
Feature = collections.namedtuple('Function', ['functionname', 'file', 'lineno', 'features'])

class Repository:

    def __init__(self, path, revision):
        self.path = path
        self.revision = revision
        # technical
        self.repository = None
        # model
        self.origin = None
        self.commit = None
        self.owner = None
        self.name = None

    def connect(self):
        try:
            if self.repository == None:
                self.repository = git.Repo(self.path)
                self.origin = self.repository.remotes.origin.url.replace(".git","")
                self.commit = self.repository.commit(self.revision).hexsha
                b = self.origin.rfind("/")
                a = self.origin.rfind("/", 0, b)
                self.owner = self.origin[a+1:b]
                self.name = self.origin[b+1:]
                print("SOVA: Connected to <" + self.path + "> originated from <" + self.origin + "> at <" + self.commit + ">")
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

    def address_functions(self, f, n, l):
        if f == ".":
            return (self.origin + "#L" + l).replace("/","\\")
        else:
            return (self.origin + "/blob/master/" + f  + "#L" + l).replace("/","\\")

    def retrieve_files(self):
        try:
            # listing = self.repository.git.ls_tree('-r', '--name-only', self.revision).split('\n')
            listing = self.repository.git.ls_tree('-r', '-l', self.revision).split('\n')
            #print(listing)
            files = []
            for l in listing:
                e = l.split()
                #print(e[0], e[1], e[2], e[3], e[4])
                files.append((os.path.normpath(e[4]), e[3]))
            #files = [
            #    os.path.normpath(file)
            #    for file in listing
            #]
            #print(files)
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

    def retrieve_functions(self):
        try:
            listing = self.repository.git.ls_tree('-r', '--name-only', self.revision).split('\n')
            functions = []
            for f in listing:
                if f.endswith('.py'):
                    code = self.repository.git.show('{}:{}'.format(self.revision, f))
                    visitor = FunctionsVisitor.from_code(code, file=f)
                    for v in visitor.functions:
                        #print(v.functionname, v.file, v.lineno)
                        functions.append((v.functionname, v.file, str(v.lineno)))
            return functions
        except git.exc.GitCommandError as e:
            sys.exit("SOVA: Failed to execute git command (error {0}), aborting".format(e.status))
        except:
            sys.exit("SOVA: Failed to retrieve functions, aborting")

    def retrieve_features(self):
        try:
            listing = self.repository.git.ls_tree('-r', '--name-only', self.revision).split('\n')
            features = []
            for f in listing:
                if f.endswith('.py'):
                    code = self.repository.git.show('{}:{}'.format(self.revision, f))
                    code_lines = code.split('\n')
                    #print(code)
                    visitor = FeaturesVisitor.from_code(code, file=f, code_lines=code_lines)
                    for v in visitor.features:
                        #print(v.functionname, v.file, v.lineno, v.features)
                        features.append((v.functionname, v.file, str(v.lineno), v.features))
            return features
        except git.exc.GitCommandError as e:
            sys.exit("SOVA: Failed to execute git command (error {0}), aborting".format(e.status))
        except:
            sys.exit("SOVA: Failed to retrieve functions, aborting")
