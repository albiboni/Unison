"""
Created by Alejandro Daniel Noel 
"""
from typing import List

from core.plant_graph.ExternalSupplier import ExternalSupplier
from core.plant_graph.Product import Product


class Machine:
    def __init__(self, name,
                 min_output_rate: float, max_output_rate: float,
                 output_product: Product,
                 suppliers: List['Machine'] = None, is_on=True, output_rate: float = None,
                 test_suppliers=True):
        """
        
        :param name: the name for the machine 
        :param min_output_rate: minimum performance or throttle point [units/second]
        :param max_output_rate: maximum performance or throttle point [units/second]
        :param output_product: the output that is outputted
        :param suppliers: list of machines that supply to this one
        :param next_machines: list of machines that this one supplies to
        :param is_on: whether the machine is working or not
        """
        self.name = name
        self._min_output_rate = min_output_rate
        self._max_output_rate = max_output_rate
        self._output_rate = output_rate or (max_output_rate + min_output_rate) / 2
        self.output_product = output_product
        self.suppliers = []
        self.add_suppliers(suppliers or [])
        self.next_machines = []
        self.is_on = is_on

        if test_suppliers:
            # Check if a subproduct is not being provided
            # If a provider is missing, add  a generic one
            _new_suppliers = []
            for sub_product in output_product.sub_products_list:
                sub_product_has_provider = False
                for prev_machine in self.suppliers:
                    if prev_machine.output_product == sub_product:
                        sub_product_has_provider = True
                if not sub_product_has_provider:
                    print(f"Machine <{self.name}> has no provider for required input <{sub_product.name}>")
                    new_supplier = ExternalSupplier(output_product=sub_product, next_machines=[self])
                    _new_suppliers.append(new_supplier)
            self.suppliers += _new_suppliers

    @property
    def min_performance(self):
        return self._min_output_rate if self.is_on else 0.0

    @property
    def max_performance(self):
        return self._min_output_rate if self.is_on else 0.0

    @property
    def output_rate(self):
        return self._output_rate if self.is_on else 0.0

    @output_rate.setter
    def output_rate(self, value):
        self._output_rate = value

    @min_performance.setter
    def min_performance(self, value):
        self._min_output_rate = value

    @max_performance.setter
    def max_performance(self, value):
        self._max_output_rate = value

    def add_next_machine(self, machine: 'Machine'):
        self.next_machines.append(machine)

    def add_suppliers(self, suppliers):
        if not isinstance(suppliers, list):
            suppliers = [suppliers]
        for supplier in suppliers:
            self.suppliers.append(supplier)
            supplier.add_next_machine(self)

    def to_dict(self):
        the_dict = {}
        for supplier in self.suppliers:
            if isinstance(supplier, Machine):
                the_dict = {**the_dict, **supplier.to_dict()}
        the_dict[self.name] = {"min_output_rate": self._min_output_rate,
                               "max_output_rate": self._max_output_rate,
                               "output_rate": self._output_rate,
                               "is_on": self.is_on,
                               "output_product": self.output_product.name
                               }
        return the_dict

    def get_graph(self):
        graph = [[self.name, *[supplier.name for supplier in self.suppliers]]]
        for supplier in self.suppliers:
            graph += supplier.get_graph()
        return graph
