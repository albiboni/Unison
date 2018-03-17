"""
Created by Alejandro Daniel Noel 
"""
from typing import List
from core.plant_graph.Product import Product
from core.plant_graph.ExternalSupplier import ExternalSupplier


class Machine:
    def __init__(self, name, min_output_rate: float, max_output_rate: float, output_product: Product,
                 suppliers: List['Machine'] = None, is_on=True):
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
        self._min_performance = min_output_rate
        self._max_performance = max_output_rate
        self.output_product = output_product
        self.suppliers = suppliers or []
        for machine in self.suppliers:
            machine.add_next_machine(self)
        self.next_machines = []
        self.is_on = is_on

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
        return self._min_performance if self.is_on else 0.0

    @property
    def max_performance(self):
        return self._min_performance if self.is_on else 0.0

    @min_performance.setter
    def min_performance(self, value):
        self._min_performance = value

    @max_performance.setter
    def max_performance(self, value):
        self._max_performance = value

    def add_next_machine(self, machine: 'Machine'):
        self.next_machines.append(machine)
