from core.optimizer.graph import Source, Graph, Edge, Node, Sink
from core.optimizer.test import get_value, get_min_cut, ford_best
#node_source = Source('s')
#node_a = Node("a", 10, {"a": 4})
#node_b = Node("b", 15, {"b": 4})
node_a = Source("a")
node_b = Source("b")
node_c = Node("c", 20, {"a": 4})
node_d = Node("d", 30, {"c": 1/3})
#node_e = Node("e", 10, {"b": 2, "d": 6})
node_sink = Sink('t', dependency={'d': 1})

#edge_sa = Edge(node_source, node_a)
#edge_sb = Edge(node_source,node_b)
edge_ac = Edge(node_a, node_c,capacity=2.)
edge_bd = Edge(node_b, node_d,capacity=3.)
#edge_de = Edge(node_d, node_e)
#edge_ce = Edge(node_c, node_e)
edge_ct = Edge(node_c, node_sink, capacity=1.)
edge_dt = Edge(node_d, node_sink, capacity=2.)



#print([str(edge) for edge in shortest_path])





graph = Graph([edge_ac, edge_bd, edge_dt, edge_ct])

graphs = graph.get_subgraphs()
for graph in graphs:
    print(ford_best(graph)[2])
'''
res_graph = graph.residual_graph()
max_flow = 0
shortest_path = res_graph.shortest_path(node_source, node_sink)
while len(shortest_path) != 0:
    print([str(edge) for edge in shortest_path])
    print(res_graph.capacity)
    values = get_value(shortest_path)
    for i in range(len(shortest_path)):
        if shortest_path[i] in graph.edges():
            graph[shortest_path[i].node_1.id][shortest_path[i].node_2.id].flow += values[2]
        elif shortest_path[i] in res_graph.edges():
            graph[shortest_path[i].node_1.id][shortest_path[i].node_2.id].flow -= values[2]
    max_flow += values[2]
    print([(str(edge), edge.flow) for edge in graph.edges()])
    res_graph = graph.residual_graph()
    shortest_path = res_graph.shortest_path(node_source, node_sink)
min_cut = res_graph.bfs(node_source)
for node in list(res_graph.nodes.values()):
    print(node.distance)
print(max_flow)


print(values)
print([str(edge) for edge in shortest_path])
values = get_value(shortest_path)
#update flow
for i in range(len(shortest_path)):

    shortest_path[i].flow = values[2]
'''


