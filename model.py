class Node(object):

    def __init__(self, name='', group='', id=''):
        self.name = name
        self.group = group
        self.id = id

    def _asdict(self):
        return self.__dict__

class Link(object):

    def __init__(self, source='', target='', value=''):
        self.source = source
        self.target = target
        self.value = value

    def _asdict(self):
        return self.__dict__

class Graph(object):

    # Note: there were problems with nodes=[], links=[]
    # for some reason two consecutively created graphs
    # were allocated the same collections of nodes and links
    def __init__(self, nodes, links):
        self.nodes = nodes
        self.links = links

    def _asdict(self):
        return self.__dict__

# for json printing
def default(self):
    return self._asdict()
