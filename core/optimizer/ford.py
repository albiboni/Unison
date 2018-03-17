from core.optimizer.graph import Source, Graph, Edge, Node, Sink
node_source = Source('s')
node_a = Node("a", 10, {"a": 4})
node_b = Node("b", 15, {"b": 4})
node_c = Node("c", 20, {"a": 4})
node_d = Node("d", 30, {"c": 1/3})
#node_e = Node("e", 10, {"b": 2, "d": 6})
node_sink = Sink('t')

edge_sa = Edge(node_source, node_a)
edge_sb = Edge(node_source,node_b)
edge_ac = Edge(node_a, node_c)
edge_bd = Edge(node_b, node_d)
#edge_de = Edge(node_d, node_e)
#edge_ce = Edge(node_c, node_e)
edge_ct = Edge(node_c, node_sink)
edge_dt = Edge(node_d, node_sink)



#print([str(edge) for edge in shortest_path])

def get_value(shortest_path):
    values = []
    for i in range(len(shortest_path)):
        values.append(shortest_path[i].capacity)
    minimum = min(values)
    idx_min = values.index(min(values))
    return values, idx_min, minimum


graph = Graph([edge_sa, edge_sb, edge_ac, edge_bd, edge_dt, edge_ct])

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
    print(graph.flow())
    res_graph = graph.residual_graph()
    shortest_path = res_graph.shortest_path(node_source, node_sink)

print(max_flow)
'''
print(values)
print([str(edge) for edge in shortest_path])
values = get_value(shortest_path)
#update flow
for i in range(len(shortest_path)):

    shortest_path[i].flow = values[2]
'''



