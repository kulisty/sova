import repository
import model
import json
import csv
import os
import itertools

def retrieve(repository):
    functions = repository.retrieve_functions()
    names = {
        (n,repository.address_functions(f,n,l))
        for (n,f,l) in functions
    }
    files = {
        (f,repository.address_files(f))
        for (n,f,l) in functions
    }
    ni = list(a for (n,a) in names)
    nf = list(a for (f,a) in files)
    idx = ni+nf+['.']
    #print(idx)
    #
    graph = model.Graph(
        model.Project(repository.origin, repository.commit, repository.owner, repository.name),
        [],[]
    )
    #
    for (n,a) in names:
        graph.nodes.append(model.Node(n, 'Function', idx.index(a), a))
    for (f,a) in files:
        graph.nodes.append(model.Node(f, 'File', idx.index(a), a))
    graph.nodes.append(model.Node('.', 'File', idx.index('.'), repository.origin))
    for (n,f,l) in functions:
        graph.links.append(model.Link( idx.index(repository.address_files(f)), idx.index(repository.address_functions(f,n,l)), 1 ))
    for (f,a) in files:
        graph.links.append(model.Link( idx.index(a), idx.index('.'), 1 ))
    #for (c, p) in parents:
    #    graph.links.append(model.Link( idx.index(c), idx.index(p), 2))
    return graph

def output(repository, file):
    graph = retrieve(repository)
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
    #
