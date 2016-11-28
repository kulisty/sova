import repository
import model
import json
import csv
import os
import itertools

# Given two lists of strings a, b
# determine if a is a prefix of b,
# treating each string a consecutive (atomic) token
def isprefix(a, b):
    return all(itertools.imap(lambda x,y: x==y, a, b)) and len(a) < len(b)

# Given a list of strings s and a list of lists (of strings)
# determine the longest string on the list being the strict prefix of the given one
def findlongest(s, strings, empty = [os.curdir]):
    longest = []
    for i in range(len(strings)):
        l = strings[i]
        if isprefix(l, s) and (len(l) > len(longest)):
            longest = l
    if longest == []:
        longest = empty
    return longest

# Convert a list of strings into a normalized os path
def topath(strings):
    result = os.curdir + os.sep
    for i in range(len(strings)):
        p = strings[i]
        result = result + os.sep + p
    result = os.path.normpath(result)
    return result

def emptypath(s):
    if s == u'':
        return os.curdir
    else:
        return os.path.normpath(s)

def recurse_setdefault(res, array):
    if len(array) == 0:
        return
    elif len(array) == 1:
        res.append(array[0])
    else:
        recurse_setdefault(res.setdefault(array[0], [] if len(array) == 2 else {}), array[1:])

def another_approach():
    files = ["foo/bar/Bla", "foo/bar/Foo", "foo/foo/Bsdf", "xsd/sdafd/saasf"]
    dict_add = lambda x, y={}: dict_add(x[:-1], y).setdefault(x[-1], {}) if(x) else y
    base_dict = {}
    map(lambda x: dict_add(x, base_dict), [path.split("/") for path in files])

def retrieve(repository):
    files = repository.retrieve_files()
    files.sort()
    paths = [
        (f, os.path.basename(f), emptypath(os.path.dirname(f)))
        for f in files
    ]
    modules = list({
        dirname
        for (filename, basename, dirname) in paths
    })
    modules.sort()
    splits = [
        m.split(os.sep)
        for m in modules
    ]
    parents = []
    while splits:
        z = splits.pop()
        s = findlongest(z, splits)
        parents.append((topath(z), topath(s)))
    children = [
        c
        for (c,p) in parents
    ]
    idx = files+children
    #
    graph = model.Graph([],[])
    #
    for f in files:
        graph.nodes.append(model.Node(f, 'File', idx.index(f), repository.address_files(f), 2))
    for m in children:
        graph.nodes.append(model.Node(m, 'Directory', idx.index(m), repository.address_files(m), 1))
    for (f, b, m) in paths:
        graph.links.append(model.Link( idx.index(f), idx.index(m), 1, 2))
    for (c, p) in parents:
        graph.links.append(model.Link( idx.index(c), idx.index(p), 2, 1))
    return graph

def output(repository, file):
    graph = retrieve(repository)
    #
    files = repository.retrieve_files()
    dirs = {}
    recurse_setdefault(dirs, files)
    #
    graph.project = model.Project(repository.origin, repository.commit, repository.owner, repository.name)
    graph.tree = dirs
    #
    # write json
    with open(file+'.json', 'wb+') as out_json:
        json.dump(graph, out_json, default=model.default, indent=2)
    #
    # write csv
    out_csv = csv.writer(open(file+'.csv', 'wb+'), delimiter=';')
    out_csv.writerow(['name', 'group', 'id', 'url'])
    for i in range(len(graph.nodes)):
        out_csv.writerow([graph.nodes[i].name, graph.nodes[i].group, graph.nodes[i].id, graph.nodes[i].url])
