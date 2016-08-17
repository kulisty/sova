import repository
import model
import json
import csv
import os
import itertools

def retrieve(repository):
    (commits, family) = repository.retrieve_commits()
    # commits = {c for (c,p) in family} | {p for (c,p) in family}
    idx = list(commits)
    #
    graph = model.Graph(
        model.Project(repository.origin, repository.commit, repository.owner, repository.name),
        [],[]
    )
    #
    for c in commits:
        graph.nodes.append(model.Node(c, 'Commit', idx.index(c), repository.address_commits(c)))
    for (c, p) in family:
        graph.links.append(model.Link( idx.index(c), idx.index(p), 1))
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
