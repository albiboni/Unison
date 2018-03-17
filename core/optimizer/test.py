from core.optimizer.graph import Source, Graph, Edge, Node, Sink
node_source = Source('s')
node_a = Node("a", 10, {'s':5})
node_b = Node("b", 15, {'s':5})
node_f = Node("f", 5, {'s':5})
node_c = Node("c", 20, {"a": 4})
node_d = Node("d", 30, {"c": 1/3})
node_e = Node("e", 10, {"b": 2})
node_h = Node("h", 10, {"d": 6})
node_sink = Sink('t')

edge_sa = Edge(node_source, node_a)
edge_sb = Edge(node_source,node_b)
edge_sf = Edge(node_source, node_f)
edge_ac = Edge( node_a, node_c)
edge_db = Edge( node_d, node_b)
edge_fe = Edge( node_f, node_e)
edge_ed = Edge(node_e, node_d)
edge_dc = Edge(node_d, node_c)
edge_ch = Edge(node_c, node_h)
edge_ht = Edge(node_h, node_sink)
edge_td = Edge(node_sink, node_d)

def get_value(shortest_path):
    values = []
    for i in range(len(shortest_path)):
        values.append(shortest_path[i].capacity)
    minimum = min(values)
    idx_min = values.index(min(values))
    return values, idx_min, minimum

graph = Graph([edge_sa, edge_sb, edge_sf, edge_ac, edge_db, edge_fe, edge_ed, edge_dc, edge_ch, edge_ht, edge_td], residual=True)
#shortest_path = graph.shortest_path(node_source, node_sink)
res_graph = graph.residual_graph()
max_flow = 0
shortest_path = res_graph.shortest_path(node_source, node_sink)
while shortest_path !=0:
    shortest_path = res_graph.shortest_path(node_source, node_sink)
    print([str(edge) for edge in shortest_path])
    print(res_graph.capacity)
    values = get_value(shortest_path)
    for i in range(len(shortest_path)):
        if shortest_path[i] in graph.edges():
            shortest_path[i].flow += values[2]
        elif shortest_path[i] in res_graph.edges():
            shortest_path[i].flow -= values[2]

    res_graph = graph.residual_graph()