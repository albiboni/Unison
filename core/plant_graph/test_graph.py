"""
Created by Alejandro Daniel Noel
"""

import unittest
import json

from core.plant_graph.Machine import Machine
from core.plant_graph.Product import Product
from core.plant_graph.ExternalSupplier import ExternalSupplier
from core.plant_graph.json_parser import write_json, read_json


def dicts_are_equal(dict1, dict2):
    def ordered_recursive(obj):
        if isinstance(obj, dict):
            return sorted((k, ordered_recursive(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(ordered_recursive(x) for x in obj)
        else:
            return obj
    return ordered_recursive(dict1) == ordered_recursive(dict2)


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.flour = Product(name="flour", units='kg')
        self.water = Product(name="water", units='liter')
        self.cream = Product(name="cream", units='kg')
        self.dough = Product(name="dough", units='kg', sub_products_quantities={self.flour: 0.3, self.water: 0.5})
        self.filling = Product(name="filling", units='liter', sub_products_quantities={self.cream: 0.5, self.flour: 0.1})
        self.pie = Product(name="pie", units='unit', sub_products_quantities={self.dough: 0.4, self.filling: 0.6})
        self.dough_maker = Machine(name="Dough maker", min_output_rate=0.1, max_output_rate=3.0,
                                   output_product=self.dough)
        self.filling_maker = Machine(name="Filling maker", min_output_rate=0.1, max_output_rate=4.0,
                                     output_product=self.filling)
        self.output_machine = Machine(name="Pie maker", min_output_rate=1, max_output_rate=3,
                                      output_product=self.pie, suppliers=[self.dough_maker, self.filling_maker])

    def test_auto_assigns_suppliers(self):
        flour_supplier = None
        water_supplier = None
        cream_supplier = None
        for supplier in ExternalSupplier.instances:
            if supplier.name == 'Supplier_of_flour':
                flour_supplier = supplier
            elif supplier.name == 'Supplier_of_water':
                water_supplier = supplier
            elif supplier.name == 'Supplier_of_cream':
                cream_supplier = supplier
        self.assertTrue(flour_supplier in self.dough_maker.suppliers)
        self.assertTrue(flour_supplier in self.filling_maker.suppliers)
        self.assertTrue(water_supplier in self.dough_maker.suppliers)
        self.assertTrue(cream_supplier in self.filling_maker.suppliers)

    def test_save_load_json(self):
        write_json(self.output_machine, "sample_graph.json")
        parsed_machine = read_json("sample_graph.json")
        dict1 = json.load(open("sample_graph.json", 'r'))
        dict2 = write_json(parsed_machine, "sample_graph.json")
        self.assertTrue(dicts_are_equal(dict1, dict2))
