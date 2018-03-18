import unittest
import math
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
        self.node_sink = Sink('t', dependency={'h': 1})

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

        self.node2_a = Source("a")
        self.node2_b = Source("b")
        self.node2_c = Node("c", 28, dependencies={"a": 4})
        self.node2_d = Node("d", 16, dependencies={"b": 2})
        self.node2_e = Node("e", 12, dependencies={"c": 3})
        self.node2_f = Node("f", 8, dependencies={"d": 0.5})
        self.node2_g = Node("g", 4, dependencies={"e": 1.5, "f": 2})
        self.sink2 = Sink("t", dependency={'g': 1})

        self.edge2_ac = Edge(self.node2_a, self.node2_c)
        self.edge2_bd = Edge(self.node2_b, self.node2_d)
        self.edge2_ce = Edge(self.node2_c, self.node2_e)
        self.edge2_df = Edge(self.node2_d, self.node2_f)
        self.edge2_eg = Edge(self.node2_e, self.node2_g)
        self.edge2_fg = Edge(self.node2_f, self.node2_g)
        self.edge2_gt = Edge(self.node2_g, self.sink2)

        self.graph2 = Graph([self.edge2_ac, self.edge2_bd, self.edge2_df, self.edge2_ce,
                          self.edge2_fg, self.edge2_eg, self.edge2_gt])
        self.graph2.update_dependencies()


    def test_edges(self):
        self.assertEqual(self.graph['d']['e'], self.edge_de)
        self.assertEqual(self.graph['b']['d'], self.edge_bd)

    def test_initial_edges(self):
        self.assertEqual(self.graph['a']['c'].node_2, self.node_c)
        self.assertEqual(self.graph['b']['d'].node_2, self.node_d)

    def test_neighbours(self):
        self.assertEqual(self.graph.neighbours(self.node_b)[0].id, self.node_d.id)
        self.assertEqual(self.graph.neighbours(self.node_b)[1].id, self.node_f.id)

    def test_shortest_path(self):
        shortest_path = [self.edge_ac, self.edge_ce, self.sink_edge]
        for i, edge in enumerate(self.graph.shortest_path(self.graph.nodes['a'], self.node_sink)):
            self.assertEqual(edge, shortest_path[i])

    def test_subgraphs(self):
        subgraphs = self.graph.get_subgraphs()
        subgraph_0 = set(map(lambda x: x.id, {self.node_a, self.node_c, self.node_e,
                                              self.node_sink}))
        subgraph_1 = set(map(lambda x: x.id, {self.node_b, self.node_d, self.node_f, self.node_e,
                                     self.node_g,
                      self.node_h, self.node_sink}))
        self.assertEqual(set(subgraphs[0].nodes), subgraph_0)
        self.assertEqual(set(subgraphs[1].nodes), subgraph_1)

    def test_dependencies(self):
        expected_dependency = {'a': 4}
        self.assertEqual(self.graph2.nodes['c'].dependencies, expected_dependency)
        expected_dependency_g = {'a': 18, 'b': 2}
        expected_dependency_e = {'a': 12}
        self.assertEqual(self.graph2.nodes['g'].dependencies, expected_dependency_g)
        self.assertEqual(self.graph2.nodes['e'].dependencies, expected_dependency_e)

    def test_dependencies_subgraph(self):
        subgraph_0, subgraph_1 = self.graph2.get_subgraphs()
        expected_dependency_g0 = {'a': 18}
        expected_dependency_g1 = {'b': 2}
        self.assertEqual(subgraph_0.nodes['g'].dependencies, expected_dependency_g0)
        self.assertEqual(subgraph_1.nodes['g'].dependencies, expected_dependency_g1)

    # def test_capacities(self):
    #     subgraph_0, subgraph_1 = self.graph2.get_subgraphs()
    #     subgraph_0.init_edges_capacity()
    #     subgraph_1.init_edges_capacity()
    #     self.assertEqual(subgraph_0['a']['c'].capacity, math.inf)
    #     self.assertEqual(subgraph_1['b']['d'].capacity, math.inf)
    #     self.assertEqual(subgraph_0['c']['e'].capacity, 7)
    #     self.assertEqual(subgraph_1['d']['f'].capacity, 8)
    #     self.assertEqual(subgraph_0['e']['g'].capacity, 1)
    #     self.assertEqual(subgraph_1['f']['g'].capacity, 8)

if __name__ == '__main__':
    unittest.main()
