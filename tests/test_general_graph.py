import unittest
from core.optimizer.graph import Graph, Edge, Node, Sink, Source


class TestGraph(unittest.TestCase):
    def setUp(self):
        # construct the graph
        self.node_a = Source("a")
        self.node_b = Source("b")
        self.node_c = Node("c", 20, {"a": 4})
        self.node_d = Node("d", 30, {"c": 1/3})
        self.node_e = Node("e", 10, {"b": 2, "d": 6})
        self.node_f = Node("f", 10, {"b": 3})
        self.node_g = Node("g", 10, {"f": 3})
        self.node_h = Node("h", 10, {"d": 2})
        self.node_sink = Sink('t')

        self.edge_ac = Edge(self.node_a, self.node_c)
        self.edge_bd = Edge(self.node_b, self.node_d)
        self.edge_ce = Edge(self.node_c, self.node_e)
        self.edge_de = Edge(self.node_d, self.node_e)
        self.edge_bf = Edge(self.node_b, self.node_f)
        self.edge_fe = Edge(self.node_f, self.node_e)
        self.edge_fg = Edge(self.node_f, self.node_g)
        self.edge_dh = Edge(self.node_d, self.node_h)
        self.edge_ge = Edge(self.node_g, self.node_e)
        self.edge_he = Edge(self.node_h, self.node_e)
        self.sink_edge = Edge(self.node_e, self.node_sink)
        self.graph = Graph([self.edge_ac, self.edge_bd, self.edge_ce, self.edge_de, self.edge_fe,
                            self.edge_bf, self.edge_fg, self.edge_ge, self.edge_dh,
                            self.edge_he, self.sink_edge])

    def test_edges(self):
        self.assertEqual(self.graph['d']['e'], self.edge_de)
        self.assertEqual(self.graph['b']['d'], self.edge_bd)

    def test_initial_edges(self):
        self.assertEqual(self.graph['s']['a'].node_2, self.node_a)
        self.assertEqual(self.graph['s']['b'].node_2, self.node_b)

    def test_neighbours(self):
        self.assertEqual(self.graph.neighbours(self.node_b)[0].id, self.node_d.id)
        self.assertEqual(self.graph.neighbours(self.node_b)[1].id, self.node_f.id)

    def test_shortest_path(self):
        shortest_path = [self.graph['s']['a'], self.edge_ac, self.edge_ce, self.sink_edge]
        for i, edge in enumerate(self.graph.shortest_path(self.graph._source, self.node_sink)):
            self.assertEqual(edge, shortest_path[i])





if __name__ == '__main__':
    unittest.main()
