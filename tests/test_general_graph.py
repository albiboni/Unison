import unittest
from core.optimizer.graph import Graph, Edge, Node, Sink


class TestGraph(unittest.TestCase):
    def setUp(self):
        # construct the graph
        self.node_a = Node("a", 10, None)
        self.node_b = Node("b", 15, None)
        self.node_c = Node("c", 20, {"a": 4})
        self.node_d = Node("d", 30, {"c": 1/3})
        self.node_e = Node("e", 10, {"b": 2, "d": 6})
        self.node_sink = Sink('t')
        self.edge_ab = Edge(self.node_a, self.node_b)
        self.edge_cd = Edge(self.node_c, self.node_d)
        self.edge_be = Edge(self.node_b, self.node_e)
        self.edge_de = Edge(self.node_d, self.node_e)
        self.sink_edge = Edge(self.node_e, self.node_sink)
        self.graph = Graph([self.edge_ab, self.edge_be, self.edge_cd, self.edge_de, self.sink_edge])

    def test_edges(self):
        self.assertEqual(self.graph['d']['e'], self.edge_de)
        self.assertEqual(self.graph['c']['d'], self.edge_cd)





