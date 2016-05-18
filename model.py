class Node(object):

    def __init__(self, name='', group='', id='', url=''):
        self.name = name
        self.group = group
        self.id = id
        self.url = url
        # on-screen display - circle
        self.cx = 0.0
        self.cy = 0.0
        self.r = 0.0
        self.style = ""

    def _asdict(self):
        return self.__dict__

    def __dir__(self):
            return ['name', 'group', 'id', 'url']

class Link(object):

    def __init__(self, source='', target='', value=''):
        self.source = source
        self.target = target
        self.value = value
        # on-screen display - line
        self.x1 = 0.0
        self.y1 = 0.0
        self.x2 = 0.0
        self.y2 = 0.0
        self.style = ""

    def _asdict(self):
        return self.__dict__

    def __dir__(self):
            return ['source', 'target', 'value']

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
