"""
Created by Alejandro Daniel Noel
"""
import json

from core.plant_graph.ExternalSupplier import ExternalSupplier
from core.plant_graph.Machine import Machine
from core.plant_graph.Product import Product
from core.plant_graph.time_schedule import create_time_schedule


def write_json(output_machine: Machine, filename):
    the_dict = {"products": output_machine.output_product.to_dict(),
                "machines": output_machine.to_dict(),
                "external_suppliers": ExternalSupplier.to_dict(),
                "graph": output_machine.get_graph(),
                "schedule": create_time_schedule(output_machine)}
    json.dump(the_dict, open(filename, 'w'), indent=4)
    return the_dict


def read_json(filename):
    the_dict = json.load(open(filename, 'r'))

    # First make list, then add connections
    products = {name: Product(name=name, units=value["units"], sub_products_quantities={}) for name, value in the_dict['products'].items()}
    for product in products.values():
        product.sub_products_quantities = {products[name]: quantity
                                           for name, quantity in the_dict['products'][product.name]['sub_products'].items()}

    ExternalSupplier.reset_instance_tracker()
    # First make list, then add connections
    suppliers = {name: Machine(name=name,
                               min_output_rate=val['min_output_rate'],
                               max_output_rate=val['max_output_rate'],
                               output_rate=val['output_rate'],
                               is_on=val['is_on'],
                               output_product=products[val['output_product']],
                               test_suppliers=False
                               ) for name, val in the_dict['machines'].items()}
    suppliers = {**suppliers, **{name: ExternalSupplier(output_product=products[val['output_product']],
                                                        min_output_rate=val['min_output_rate'],
                                                        max_output_rate=val['max_output_rate'],
                                                        output_rate=val['output_rate'],
                                                        ) for name, val in the_dict['external_suppliers'].items()}}
    for supplier_links in the_dict['graph']:
        base = supplier_links[0]
        supplier = supplier_links[1]
        delay = supplier_links[2]
        suppliers[base].add_supplier(suppliers[supplier], delay)

    # return the last machine in the chain (the graph was built backwards)
    return suppliers[the_dict['graph'][0][0]]
