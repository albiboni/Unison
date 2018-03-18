from collections import defaultdict, deque
import math
import copy

class Node(object):
    def __init__(self, identifier: str, production: float, dependencies: dict):
        self.dependencies = dependencies
        self.production = production
        self.id = identifier
        self.distance = 0
        self.parent = None

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return ord(self.id)


class Source(Node):
    def __init__(self, identifier):
        super().__init__(identifier, math.inf, {})


class Sink(Node):
    def __init__(self, identifier, dependency):
        super().__init__(identifier, 0, dependency)


class Edge(object):
    def __init__(self, node_1: Node, node_2: Node, capacity=0, flow=0, delay=0):
        self._node_1 = node_1
        self._node_2 = node_2
        self._capacity = capacity
        self._flow = flow
        self.delay = delay

    def __str__(self):
        return "Edge {0} -> {1}" .format(self.node_1.id, self.node_2.id)

    def __eq__(self, other):
        return self.node_1.id == other.node_1.id and self.node_2.id == other.node_2.id

    def __hash__(self):
        return ord(self.node_1.id) + ord(self.node_2.id)

    @property
    def flow(self):
        return self._flow

    @flow.setter
    def flow(self, value):
        #if not isinstance(self.node_1, Source):
        #    self._flow = value*list(self.node_1.dependencies.values())[0]
        #else:
        self._flow = value


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
    def __init__(self, edges, directed=True, subgraph=False):
        self.nodes = {}
        self._sources = {}
        self._sink = None
        self.graph = defaultdict(dict)
        self.is_directed = directed
        self.capacity = [edge.capacity for edge in edges ]
        self._add_connections(edges)
        if not subgraph:
            self.update_dependencies()
        if subgraph:
            self.init_edges_capacity()

    def get_parent_nodes(self, node_id):
        if node_id in [node.id for node in self.sources]:
            return None

        parent_node_ids = []
        for node_1_id, inner_dict in list(self.graph.items()):
            for node_2_id, edge in list(inner_dict.items()):
                if node_2_id == node_id:
                    parent_node_ids.append(node_1_id)
        return parent_node_ids

    def update_dependencies(self):
        def find_dependency_const(node):
            if self.is_source(node):
                return {node: 1}
            else:
                dependencies = list(self.nodes[node].dependencies.keys())
                for parent in dependencies:
                    factor_parent = self.nodes[node].dependencies[parent]
                    updated_dict = find_dependency_const(parent)
                    for key in updated_dict:
                        self.nodes[node].dependencies[key] = factor_parent * updated_dict[key]

                    if not self.is_source(parent):
                        del self.nodes[node].dependencies[parent]

                return self.nodes[node].dependencies
        find_dependency_const(self.sink.id)

    def init_edges_capacity(self):

        for node_1_id, inner_dict in list(self.graph.items()):
            if not self.is_source(node_1_id) and not self.is_sink(node_1_id):
                for node_2_id, edge in list(inner_dict.items()):
                    edge = self.graph[node_1_id][node_2_id]
                    try:
                        edge._capacity = self.nodes[node_1_id].production / list(self.nodes[
                            node_1_id].dependencies.values())[0]

                    except AttributeError as e:
                        raise AttributeError("Trying to set capacity of source edge, they are set to infinity")

    def is_source(self, node_id):
        return node_id in [node.id for node in self.sources]

    def is_sink(self, node_id):
        return node_id in [node.id for node in filter(lambda x: isinstance(x, Sink), self.nodes)]

    def edges(self):
        edges = []
        for node_1_id, inner_dict in list(self.graph.items()):
            for node_2_id, edge in list(inner_dict.items()):
                edges.append(edge)
        return edges

    def flow(self):
        flow = []
        for node_1_id, inner_dict in list(self.graph.items()):
            for node_2_id, edge in list(inner_dict.items()):
                flow.append(edge.flow)
        return flow

    @property
    def sources(self):
        self._sources = list(filter(lambda x: isinstance(x, Source), self.nodes.values()))
        return self._sources

    @property
    def sink(self):
        self._sink = list(filter(lambda x: isinstance(x, Sink), self.nodes.values()))[0]
        return self._sink

    def __getitem__(self, item):
        return self.graph[item]

    def _add_connections(self, edges):
        for edge in edges:
            self.add_edge(edge)

    def add_edge(self, edge):
        # connect sources of elements to the source node
        if isinstance(edge.node_1, Source):
            edge._capacity = math.inf

        # add nodes references to the dict of nodes
        self.nodes[edge.node_1.id] = edge.node_1
        self.nodes[edge.node_2.id] = edge.node_2
        # add the edges
        self.graph[edge.node_1.id][edge.node_2.id] = edge
        if not self.is_directed:
            self.graph[edge.node_2.id][edge.node_1.id] = edge.reverse()

    def neighbours(self, node):
        return [self.nodes[identifier] for identifier in list(self.graph[node.id].keys())]

    def bfs(self, start_node):
        for node in list(self.nodes.values()):
            node.distance = math.inf

        start_node.distance = 0
        queue = deque()
        queue.append(start_node)

        while len(queue) != 0:
            current_node = queue.popleft()
            for neighbour in self.neighbours(current_node):
                if neighbour.distance == math.inf:
                    neighbour.distance = current_node.distance + 1
                    neighbour.parent = current_node
                    queue.append(neighbour)

    def shortest_path(self, start_node, end_node):
        self.bfs(start_node)

        def get_path(node, acc):
            if node.id == start_node.id:
                return acc[::-1]
            else:
                return get_path(node.parent, acc + [self.graph[node.parent.id][node.id]])

        path = []
        if end_node.distance != math.inf:
            path = get_path(end_node, path)
        return path

    def residual_graph(self):
        edges = []
        for node_1, inner_dict in list(self.graph.items()):
            for node_2, edge in list(inner_dict.items()):
                if edge.capacity - edge.flow > 0:
                    edges.append(Edge(self.nodes[node_1], self.nodes[node_2],
                                      capacity=edge.capacity - edge.flow))
                elif edge.capacity == edge.flow:
                    edges.append(Edge(self.nodes[node_2], self.nodes[node_1], capacity=edge.flow))
        return Graph(edges, directed=True, subgraph=True)

    def get_subgraphs(self):
        graphs = []
        for source in self.sources:
            self.bfs(source)
            nodes_subgraph = copy.deepcopy(list(filter(lambda x: x.distance < math.inf,
                                               self.nodes.values())))
            edges_subgraph = copy.deepcopy(list(filter(lambda x: x.node_1 in nodes_subgraph and
                                                   x.node_2 in nodes_subgraph,
                                self.edges())))
            self.remove_unwanted_dependencies(edges_subgraph,
                                              list(map(lambda x: x.id, nodes_subgraph)))
            graphs.append(Graph(edges_subgraph, subgraph=True))

        return graphs

    def remove_unwanted_dependencies(self, edges, nodes):
        for edge in edges:
            dependencies_node_1 = copy.copy(edge.node_1.dependencies)
            for dependency in dependencies_node_1:
                if dependency not in nodes:
                    del edge.node_1.dependencies[dependency]

            dependencies_node_2 = copy.copy(edge.node_1.dependencies)
            for dependency in dependencies_node_2:
                if dependency not in nodes:
                    del edge.node_2.dependencies[dependency]



