"""
Created by Alejandro Daniel Noel
"""
from core.plant_graph.ExternalSupplier import ExternalSupplier
from core.plant_graph.machine import Machine
from core.plant_graph.product import Product
from core.optimizer.graph import Node, Sink, Source, Graph, Edge
from core.plant_graph.json_parser import make_json_dict
import math


def to_graph_obj(output_machine):
    machine_names = [key for key in output_machine.to_dict().keys()]
    ext_supplier_names = [key for key in ExternalSupplier.to_dict().keys()]
    all_names = machine_names + ext_supplier_names
    nodes = []
    edges = []
    for name in machine_names:
        a_machine = output_machine.search_machine_by_name(name)
        provided_product_quantities = {}
        for supplier in a_machine.suppliers:
            provided_product_quantities[supplier.name] = a_machine.output_product.sub_products_quantities[supplier.output_product] / a_machine.count_suppliers_of_product(supplier.output_product)
        nodes.append(Node(name, a_machine.output_rate, provided_product_quantities))
    for name in ext_supplier_names:
        nodes.append(Source(name))
    for i, node in enumerate(nodes):
        suppliers = output_machine.search_machine_by_name(all_names[i]).suppliers
        if suppliers is None:
            continue
        for j, supplier in enumerate(suppliers):
            up_node = nodes[all_names.index(supplier.name)]
            edges.append(Edge(up_node, node, delay=output_machine.search_machine_by_name(node.id).delays[j]))
    edges.append(Edge(nodes[[n.id for n in nodes].index(output_machine.name)], Sink('Sink',
                                                                                    {
                                                                                        output_machine.name: math.inf})))
    print([str(edge) for edge in edges])
    return Graph(edges, subgraph=False)


def update_output_machine(_output_machine, _graph_obj):
    for edge in _graph_obj.edges:
        _output_machine.search_machine_by_name(edge.node_1.id).set_output_rate = edge.local_flow


if __name__ == "__main__":
    ExternalSupplier.reset_instance_tracker()
    flour = Product(name="flour", units='kg')
    water = Product(name="water", units='liter')
    cream = Product(name="cream", units='kg')
    dough = Product(name="dough", units='kg', sub_products_quantities={flour: 0.4, water: 0.6})
    filling = Product(name="filling", units='liter', sub_products_quantities={cream: 0.7, flour: 0.3})
    pie = Product(name="pie", units='unit', sub_products_quantities={dough: 0.5, filling: 0.2})
    dough_maker1 = Machine(name="Dough maker 1", min_batch_time=200, max_batch_time=1000, batch_time=500, batch_size=50,
                           output_product=dough)
    dough_maker2 = Machine(name="Dough maker 2", min_batch_time=200, max_batch_time=1000, batch_time=500, batch_size=50,
                           output_product=dough)
    filling_maker1 = Machine(name="Filling maker 1", min_batch_time=100, max_batch_time=500.0, batch_time=150, batch_size=20,
                             output_product=filling)
    filling_maker2 = Machine(name="Filling maker 2", min_batch_time=100, max_batch_time=500.0, batch_time=150, batch_size=20,
                             output_product=filling)
    filling_maker3 = Machine(name="Filling maker 3", min_batch_time=100, max_batch_time=500.0, batch_time=150, batch_size=20,
                             output_product=filling)
    output_machine = Machine(name="Pie maker", min_batch_time=10, max_batch_time=300, batch_time=50, batch_size=30,
                             output_product=pie,
                             suppliers=[dough_maker1, dough_maker2, filling_maker1, filling_maker2, filling_maker3],
                             delays=[22.3, 20.1, 13.2, 11.1, 15.3])


    def dicts_are_equal(dict1, dict2):
        def ordered_recursive(obj):
            if isinstance(obj, dict):
                return sorted((k, ordered_recursive(v)) for k, v in obj.items())
            if isinstance(obj, list):
                return sorted(ordered_recursive(x) for x in obj)
            else:
                return str(obj)

        return ordered_recursive(dict1) == ordered_recursive(dict2)

    dict1 = make_json_dict(output_machine)
    graph_obj = to_graph_obj(output_machine)
    update_output_machine(output_machine, graph_obj)
    dict2 = make_json_dict(output_machine)
    print(dicts_are_equal(dict1, dict2))
