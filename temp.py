    print("{")

    print("    "+"\"nodes\":[")

    for i in range(len(commits)):
        print("        " + "{ " +
            "\"name\":\"" + commits[i].hexsha + "\"" + " , " +
            "\"group\":" + str(i) + "" + " , " +
            "\"id\":\"" + str(nodes.index(commits[i].hexsha)) + "\"" +
            " },"
        )

    print("    "+"],")

    print("    "+"\"links\":[")

    for (child, parent) in parents:
        print(
            "        " + "{" +
            "\"source\":" + str(nodes.index(child.hexsha)) + "" +
            "," +
            "\"target\":" + str(nodes.index(parent.hexsha)) + "" +
            "," +
            "\"value\":" + str(1) +
            "},"
        )

    print("    "+"]")
    print("}")
    #print(parents)



    def retrieve_modules(self, commit='HEAD'):
        files = self.retrieve_files(commit)
        # modules = [
        #    (os.path.dirname(file), os.path.basename(file)) for file in files
        # ]
        modules = {
            dirname for (basename, dirname) in files
        }
        return modules



   def retrieve_parents(self, commit):
        parents = [
            (commit, parent)
            for parent in commit.parents
        ]
        return parents

    def retrieve_family(self):
        family = [
            (commit, parent)
            for (commit, parent) in self.iterate_family()
        ]
        return family

    def iterate_family(self):
        commits = self.retrieve_commits()
        for commit in commits:
            for parent in commit.parents:
                yield (commit, parent)


    commits = repository.retrieve_commits()
    index = [
        #(i, commits[i].hexsha) for i in range(len(commits))
        commits[i].hexsha for i in range(len(commits))
    ]
    # family = extractor.retrieve_family()
    # modules = extractor.retrieve_modules()
    # return (index, family, files, modules)


    # (vertices, edges, files, modules) = build(arguments.path, arguments.rev_from, arguments.rev_to)

    #graph4commits = model.Graph()
    #for i in range(len(vertices)):
    #    graph4commits.nodes.append(model.Node(vertices[i], i, i))
    #for (child, parent) in edges:
    #    graph4commits.links.append(model.Link(vertices.index(child.hexsha), vertices.index(parent.hexsha), "1"))

    #for module in modules:
    #    graph4files.links.append(model.Link(1, 1, "1"))

    #print(json.dumps(graph, default=model.default,  indent=2))

    #with open('commits.json', 'w') as file4commits:
    #    json.dump(graph4commits, file4commits, default=model.default,  indent=2)





def commonprefix2(args, sep='/'):
    return os.path.commonprefix(args).rpartition(sep)[0]

def allnamesequal(name):
    return all(n==name[0] for n in name[1:])
 
def commonprefix(paths, sep='/'):
    bydirectorylevels = zip(*[p.split(sep) for p in paths])
    return sep.join(x[0] for x in itertools.takewhile(allnamesequal, bydirectorylevels))
 
def split_path(p):
    a,b = os.path.split(p)
    return (split_path(a) if len(a) and len(b) else []) + [b]

    #commonprefix(modules)
    #print(modules[3:])
    #for i in itertools.takewhile(lambda x: os.path.commonprefix([x]+["lib"]), modules[3:]):
    #    print(i)
    #root = modules[0]
    #modules.remove(root)
    #parents = zip(modules, itertools.repeat(root,len(modules)))
    #print(parents)
    #print(['lib'] in ['lib','basia'])
    #it = itertools.takewhile(lambda x: ['lib'] < x, splits)
    #for d in it:
    #    print(d)
    #modules.sort()
    #print("Modules:", modules[:-3])
    #print("Modules:", modules[-1])
    #zz = [x for x in modules if x not in [y[:len(x)] for y in modules if y != x]]
    #zy = [x for x, y in zip(modules[:-1], modules[1:]) if x != y[:len(x)]] + [modules[-1]]
    #zx = [modules[i] for i in range(len(modules))[:-1] if modules[i] != modules[i+1][:len(modules[i])]] + [modules[-1]]
    #[v for i, v in enumerate(ls[:-1]) if not ls[i+1].startswith(v)]+[ls[-1]]
    #print(zz)
    #print(zy)
    #print(zx)
    #print("test: ", isprefix(['ala'], ['ala','ma']))
    #print("test: ", findlongest(['ala','ma','kota'], [['al'], ['al','ma']]))
    # print(isprefix(['ala','mam'], ['ala','ma','kota']))    
    #print(splits)

    #n = idx.index("")
    #for m in modules:
    #    graph.links.append(model.Link( idx.index(m), n, 2 ))
