from collections import defaultdict, deque
import math


class Node(object):
    def __init__(self, identifier: str, production: float, dependecies: dict = None):
        self.dependecies = dependecies
        self.production = production
        self.id = identifier
        self.distance = 0
        self.parent = None


class Source(Node):
    def __init__(self, identifier):
        super().__init__(identifier, math.inf)


class Sink(Node):
    def __init__(self, identifier):
        super().__init__(identifier, 0)


class Edge(object):
    def __init__(self, node_1: Node, node_2: Node, capacity=0, flow=0, delay=0):
        self._node_1 = node_1
        self._node_2 = node_2
        self._capacity = capacity
        self.flow = flow
        self.delay = delay

    def __str__(self):
        return "Edge {0} -> {1}" .format(self.node_1.id, self.node_2.id)

    @property
    def node_1(self):
        return self._node_1

    @property
    def node_2(self):
        return self._node_2

    @property
    def capacity(self):
        return self._capacity

    def reverse(self):
        return Edge(self._node_2, self._node_1, self._capacity, self.flow, self.delay)


class Graph(object):
    def __init__(self, edges, directed=True):
        self._source = Source('s')
        self.nodes = {'s': self._source}
        self.graph = defaultdict(dict)
        self.is_directed = directed
        self._add_connections(edges)

    def __getitem__(self, item):
        return self.graph[item]

    def _add_connections(self, edges):
        for edge in edges:
            self.add_edge(edge)

    def _add_initial_nodes(self, node):
        self.add_edge(Edge(self._source, node, capacity=math.inf))

    def add_edge(self, edge):
        # connect sources of elements to the source node
        if edge.node_1.dependecies is None and not isinstance(edge.node_1, Source):
            self._add_initial_nodes(edge.node_1)

        # add nodes references to the dict of nodes
        self.nodes[edge.node_1.id] = edge.node_1
        self.nodes[edge.node_2.id] = edge.node_2
        # add the edges
        self.graph[edge.node_1.id][edge.node_2.id] = edge
        if not self.is_directed:
            self.graph[edge.node_2.id][edge.node_1.id] = edge.reverse()

    def neighbours(self, node):
        return [self.nodes[identifier] for identifier in list(self.graph[node.id].keys())]

    def shortest_path(self, start_node, end_node):
        for node in list(self.nodes.values()):
            node.distance = math.inf

        start_node.distance = 0
        queue = deque(start_node)

        while queue.count != 0:
            current_node = queue.popleft()
            for neighbour in self.neighbours(current_node):
                if neighbour.distance == math.inf:
                    neighbour.distance = current_node.distance + 1
                    neighbour.parent = current_node
                    deque.append(neighbour)

        def get_path(node):
            if node.id == self._source.id:
                return node
            else:
                return [node].extend(get_path(node.parent))

        path = None
        if end_node.distance != math.inf:
            path = get_path(end_node)

        return path













