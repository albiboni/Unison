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
                 suppliers: List['Machine'] = None, delays: List[float] = None,
                 is_on=True, output_rate: float = None,
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
        self._suppliers = []
        self.next_machines = []
        self.is_on = is_on
        self._delays = []

        if len(delays or []) == 0:
            delays = [0.0] * len(suppliers or [])
        for i in range(len(suppliers or [])):
            self.add_supplier(suppliers[i], delays[i])

        if test_suppliers:
            # Check if a subproduct is not being provided
            # If a provider is missing, add  a generic one
            _new_suppliers = []
            for sub_product in output_product.sub_products_list:
                sub_product_has_provider = False
                for prev_machine in self._suppliers:
                    if prev_machine.output_product == sub_product:
                        sub_product_has_provider = True
                if not sub_product_has_provider:
                    print(f"Machine <{self.name}> has no provider for required input <{sub_product.name}>")
                    new_supplier = ExternalSupplier(output_product=sub_product, next_machines=[self])
                    _new_suppliers.append(new_supplier)
            for new_supplier in _new_suppliers:
                self.add_supplier(new_supplier, 0.0)

    @property
    def min_output_rate(self):
        return self._min_output_rate if self.is_on else 0.0

    @property
    def max_output_rate(self):
        return self._max_output_rate if self.is_on else 0.0

    @property
    def output_rate(self):
        return self._output_rate if self.is_on else 0.0

    @output_rate.setter
    def output_rate(self, value):
        self._output_rate = value

    @min_output_rate.setter
    def min_output_rate(self, value):
        self._min_output_rate = value

    @max_output_rate.setter
    def max_output_rate(self, value):
        self._max_output_rate = value

    @property
    def suppliers(self):
        return self._suppliers

    def add_next_machine(self, machine: 'Machine'):
        self.next_machines.append(machine)

    def add_supplier(self, supplier, delay):
        self._suppliers.append(supplier)
        self._delays.append(delay)
        supplier.add_next_machine(self)

    def delay_for_supplier(self, supplier):
        return self._delays[self._suppliers.index(supplier)]

    def to_dict(self):
        the_dict = {}
        for supplier in self._suppliers:
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
        graph = [[self.name, self._suppliers[i].name, self._delays[i]] for i in range(len(self._suppliers))]
        for supplier in self._suppliers:
            graph += supplier.get_graph()
        return graph

    def get_scheduling(self, end_time, output_units_required):
        # Row data: [process_name, duration, end_time, dependencies, performance_percent]
        duration = output_units_required / self.output_rate
        scheduling = [[self.name,
                       output_units_required / self.output_rate,
                       end_time,
                       ', '.join([supplier.name for supplier in self.suppliers]),
                       100 * self.output_rate / self.max_output_rate]]
        for supplier in self.suppliers:
            scheduling += supplier.get_scheduling(end_time=end_time - duration - self.delay_for_supplier(supplier),
                                                  output_units_required=output_units_required *
                                                                        self.output_product.sub_products_quantities[supplier.output_product])
        return scheduling
