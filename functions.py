import repository
import model
import json
import csv
import os
import itertools

def retrieve(repository):
    f = repository.retrieve_functions()
    return f

def output(repository, file):
    functions = repository.retrieve_functions()
    #
    graph = model.Graph(
        model.Project(repository.path, repository.origin, repository.revision),
        [],[]
    )
    #
    for (f,n,l) in functions:
        graph.nodes.append(model.Node(n, 'Functions', 1, repository.address_functions(f,l)))
    #for c in classes:
    #    graph.nodes.append(model.Node(m, 'Classes', idx.index(m), repository.address_files(m)))
    #for (f, c) in paths:
    #    graph.links.append(model.Link( idx.index(f), idx.index(m), 1 ))
    #for (c, p) in parents:
    #    graph.links.append(model.Link( idx.index(c), idx.index(p), 2))
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
