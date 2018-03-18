from core.optimizer.graph import Source, Graph, Edge, Node, Sink

from core.optimizer.graph_optimization import find_final_flow, ford_best

'''
node_source = Source('s')
node_a = Node("a", 10, {'s':5})
node_b = Node("b", 15, {'s':5})
node_f = Node("f", 5, {'s':5})
node_c = Node("c", 20, {"a": 4})
node_d = Node("d", 30, {"c": 1/3})
node_e = Node("e", 10, {"b": 2})
node_h = Node("h", 10, {"d": 6})
node_sink = Sink('t', {"d": 6})

edge_sa = Edge(node_source, node_a)
edge_sb = Edge(node_source,node_b)
edge_sf = Edge(node_source, node_f)
edge_ac = Edge( node_a, node_c, capacity=1.)
edge_bd = Edge(node_b, node_d, capacity=1.)
edge_fe = Edge( node_f, node_e, capacity=1.)
edge_de = Edge(node_d, node_e, capacity=1.)
edge_dc = Edge(node_d, node_c, capacity=1.)
edge_ch = Edge(node_c, node_h, capacity=2.)
edge_ht = Edge(node_h, node_sink, capacity=2.)
edge_et = Edge(node_e, node_sink, capacity=1,)
'''
node2_a = Source("a")
node2_b = Source("b")
node2_c = Node("c", 28, dependencies={"a": 4})
node2_d = Node("d", 16, dependencies={"b": 2})
node2_e = Node("e", 12, dependencies={"c": 3})
node2_f = Node("f", 8, dependencies={"d": 0.5})
node2_g = Node("g", 4, dependencies={"e": 1.5, "f": 2})
sink2 = Sink("t", dependency={'g': 1})

edge2_ac = Edge(node2_a, node2_c)
edge2_bd = Edge(node2_b, node2_d)
edge2_ce = Edge(node2_c, node2_e)
edge2_df = Edge(node2_d, node2_f)
edge2_eg = Edge(node2_e, node2_g)
edge2_fg = Edge(node2_f, node2_g)
edge2_gt = Edge(node2_g, sink2)

graph2 = Graph([edge2_ac, edge2_bd, edge2_df, edge2_ce,
                  edge2_fg, edge2_eg, edge2_gt])
graph2.update_dependencies()

#graph = Graph([edge_sa, edge_sb, edge_sf, edge_ac, edge_bd, edge_fe, edge_de, edge_dc, edge_ch, edge_ht, edge_et])
#def ford_best(graph):
#shortest_path = graph.shortest_path(node_source, node_sink)


graphs = graph2.get_subgraphs()
for graph in graphs:
    print(ford_best(graph)[2])
print("common nodes: ", graph2.common_nodes(graphs[0], graphs[1]))

# common_nodes = total_common_nodes(graph2)
# graphs = graph2.get_subgraphs()
# graphs = enforce_flow_constraints(graphs, common_nodes)
# print([(str(edge), edge.flow) for edge in graphs[0].edges()])
# print([(str(edge), edge.flow) for edge in graphs[1].edges()])

find_final_flow(graph2)
print([(str(edge), edge.local_flow) for edge in graph2.edges()])



#     for i in range in graphs:
#         print(ford_best(graph)[2])
#min_cut, res_graph, max_flow = ford_best(graph)
#for i inraphs

#print(ford_best(graph))

'''
res_graph.bfs(node_source)
#set_S = list(filter(lambda x: x.distance < math.inf, res_graph.nodes))
#print([str(node) for node in set_S])
#set_T = list(filter(lambda x: x not in set_S, res_graph.nodes))
set_S = []
set_T = []
for node in list(res_graph.nodes.values()):
    if node.distance == float('inf'):
        set_T.append(node)
    else:
        set_S.append(node)

min_cut = []

for edge in graph.edges():
    if edge.node_1 in set_S and edge.node_2 in set_T:
        min_cut.append(edge)
print([str(edge) for edge in min_cut])
   # return max_flow


#print(ford_best(graph))
#return max_flow, constraints
#print(max_flow)
#print(constraints)
'''
