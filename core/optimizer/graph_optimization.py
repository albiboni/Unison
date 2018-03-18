def total_common_nodes(graph):
    graphs = graph.get_subgraphs()
    common_pts = [[0]*len(graphs) for j in range(len(graphs))]
    for i in range(len(graphs)-1):
        for j in range(i + 1, len(graphs)):
            common_pts[i][j] = graph.common_nodes(graphs[i], graphs[j])
    return common_pts


def get_subgraph_edge(subgraph, node):
    return list(filter(lambda edge: edge.node_1.id == node, subgraph.edges))[0]


def enforce_flow_constraints(graphs, common_nodes):
    for graph in graphs:
        ford_best(graph)

    for i in range(len(graphs)-1):
        for j in range(i + 1, len(graphs)):
            if common_nodes[i][j] != 0:
                for node in common_nodes[i][j]:
                    ratio = (list(graphs[i].nodes[node].dependencies.values())[0] /
                             list(graphs[j].nodes[node].dependencies.values())[0])
                    edge_i = get_subgraph_edge(graphs[i], node)
                    edge_j = get_subgraph_edge(graphs[j], node)
                    ratio_flows = edge_i.flow/edge_j.flow
                    if ratio > ratio_flows:
                        flow = graphs[i][edge_j.node_1.id][edge_j.node_2.id].flow / ratio
                        for edge in graphs[j].edges:
                            edge.flow = flow
                    else:
                        flow = graphs[j][edge_j.node_1.id][edge_j.node_2.id].flow * ratio
                        for edge in graphs[i].edges:
                            edge.flow = flow
    return graphs

def ford_best(graph):
    node_source = graph.sources[0]
    node_sink = graph.sink
    # print ([(str(edge), edge.capacity) for edge in graph.edges])
    res_graph = graph.residual_graph()
    max_flow = 0
    constraints = []
    shortest_path = res_graph.shortest_path(node_source, node_sink)
    while len(shortest_path) != 0:
        # print([str(edge) for edge in shortest_path])
        # print(res_graph.capacity)
        values = get_value(shortest_path)
        for i in range(len(shortest_path)):
            if shortest_path[i] in graph.edges:
                graph[shortest_path[i].node_1.id][shortest_path[i].node_2.id].flow += values[2]
            elif shortest_path[i] in res_graph.edges:
                graph[shortest_path[i].node_1.id][shortest_path[i].node_2.id].flow -= values[2]
        max_flow += values[2]
        constraints.append(str(shortest_path[values[1]]))
        # print([(str(edge), edge.flow) for edge in graph.edges])
        res_graph = graph.residual_graph()
        shortest_path = res_graph.shortest_path(node_source, node_sink)
    min_cut = get_min_cut(node_source, res_graph, graph)
    return min_cut, res_graph, max_flow


def get_min_cut(node_source, res_graph, graph):
    res_graph.bfs(node_source)
    set_S = []
    set_T = []
    for node in list(res_graph.nodes.values()):
        if node.distance == float('inf'):
            set_T.append(node)
        else:
            set_S.append(node)

    min_cut = []

    for edge in graph.edges:
        if edge.node_1 in set_S and edge.node_2 in set_T:
            min_cut.append(edge)
    # print([str(edge) for edge in min_cut])
    return min_cut


def get_value(shortest_path):
    values = []
    for i in range(len(shortest_path)):
        values.append(shortest_path[i].capacity)
    minimum = min(values)
    idx_min = values.index(min(values))
    return values, idx_min, minimum


def optimize(graph):
    common_nodes = total_common_nodes(graph)
    graphs = graph.get_subgraphs()
    updated_graphs = enforce_flow_constraints(graphs, common_nodes)
    for subgraph in updated_graphs:
        for edge in subgraph.edges:
            graph[edge.node_1.id][edge.node_2.id].flow += edge.flow
            graph[edge.node_1.id][edge.node_2.id].local_flow += edge.local_flow
