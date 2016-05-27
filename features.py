import repository
import model
import json
import csv
import os
import itertools

def retrieve(repository):
    f = repository.retrieve_features()
    return f

def output(repository, file):
    features = repository.retrieve_features()
    names = {
        (n,repository.address_functions(f,n,l),ff[0])
        for (n,f,l,ff) in features
    }
    files = {
        (f,repository.address_files(f))
        for (n,f,l,ff) in features
    }
    ni = list(a for (n,a,c) in names)
    nf = list(a for (f,a) in files)
    idx = ni+nf+['.']
    #print(idx)
    #
    graph = model.Graph(
        model.Project(repository.path, repository.origin, repository.revision),
        [],[]
    )
    #
    for (n,a,c) in names:
        graph.nodes.append( model.Node(name = n, group = 'Functions', id = idx.index(a), url = a, complexity = 5+float(c)/3) )
    for (f,a) in files:
        graph.nodes.append( model.Node(name = f, group = 'Files', id = idx.index(a), url = a, complexity = 4.0))
    #
    graph.nodes.append( model.Node(name = '.', group = 'Files', id = idx.index('.'), url = repository.origin, complexity = 6.0) )
    #
    for (n,f,l,ff) in features:
        graph.links.append(model.Link( idx.index(repository.address_files(f)), idx.index(repository.address_functions(f,n,l)), 1 ))
    for (f,a) in files:
        graph.links.append(model.Link( idx.index(a), idx.index('.'), 1 ))
    #for (c, p) in parents:
    #    graph.links.append(model.Link( idx.index(c), idx.index(p), 2))
    #
    # write json
    with open(file+'.json', 'wb+') as out_json:
        json.dump(graph, out_json, default=model.default, indent=2)
    #
    # write csv
    out_csv = csv.writer(open(file+'.csv', 'wb+'), delimiter=';')
    out_csv.writerow(['name', 'group', 'id', 'url', 'complexity', 'quality'])
    for i in range(len(graph.nodes)):
        out_csv.writerow([graph.nodes[i].name, graph.nodes[i].group, graph.nodes[i].id, graph.nodes[i].url, graph.nodes[i].complexity, graph.nodes[i].quality])
    #
