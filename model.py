# Container for information about the project
class Project(object):

    def __init__(self, origin='', commit='', owner='', name=''):
        self.origin = origin
        self.commit = commit
        self.owner = owner
        self.name = name

    def _asdict(self):
        return self.__dict__

    def __dir__(self):
            return ['origin', 'commit', 'owner', 'name']

# Container for information about the project's nodes
class Node(object):

    def __init__(self, name='', group='', id='', url='', complexity=1.0, quality=1.0):
        self.name = name
        self.group = group
        self.id = id
        self.url = url
        self.complexity = complexity
        self.quality = quality
        # on-screen display - circle
        self.cx = 0.0
        self.cy = 0.0
        self.r = 0.0
        self.style = ""
        self.index = 0
        self.x = 0.0
        self.y = 0.0
        self.px = 0.0
        self.py = 0.0
        self.fixed = False

    def _asdict(self):
        return self.__dict__

    def __dir__(self):
            return ['name', 'group', 'id', 'url', 'complexity', 'quality']

# Container for information about the project's links (between nodes)
class Link(object):

    def __init__(self, source='', target='', value='', complexity=1.0, quality=1.0):
        self.source = source
        self.target = target
        self.value = value
        self.complexity = complexity
        self.quality = quality
        # on-screen display - line
        self.x1 = 0.0
        self.y1 = 0.0
        self.x2 = 0.0
        self.y2 = 0.0
        self.style = ""

    def _asdict(self):
        return self.__dict__

    def __dir__(self):
            return ['source', 'target', 'value', 'complexity', 'quality']

# Container for information about the project and its nodes and links
class Graph(object):

    # Note: there were problems with nodes=[], links=[]
    # for some reason two consecutively created graphs
    # were allocated the same collections of nodes and links
    def __init__(self, project, nodes, links):
        self.project = project
        self.nodes = nodes
        self.links = links

    def _asdict(self):
        return self.__dict__

# For json printing
def default(self):
    return self._asdict()
