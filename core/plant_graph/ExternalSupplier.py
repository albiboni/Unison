"""
Created by Alejandro Daniel Noel
"""
from typing import List
from weakref import WeakSet

from core.plant_graph.Product import Product


class ExternalSupplier:
    instances = WeakSet()

    def __new__(cls, output_product: Product, next_machines: List = (),
                min_output_rate: float = 0.0, max_output_rate: float = 10000000000000.0, output_rate=0.0):
        name = 'Supplier_of_' + output_product.name

        for instance in cls.instances:
            if instance.name == name:
                print(f"    <{name}> already exists, subscribing also to {','.join([f'<{machine.name}>' for machine in next_machines])}")
                instance.next_machines += next_machines
                return instance

        self = object.__new__(ExternalSupplier)
        self.name = 'Supplier_of_' + output_product.name
        self.min_output_rate = min_output_rate
        self.max_output_rate = max_output_rate
        self.output_rate = output_rate
        self.output_product = output_product
        self.next_machines = next_machines

        print(f"    A generic supplier of <{output_product.name}> has been created")

        cls.instances.add(self)
        return self

    def __hash__(self):
        return hash(self.name)

    def add_next_machine(self, next_machine):
        self.next_machines.append(next_machine)

    @classmethod
    def to_dict(cls):
        the_dict = {}
        for supplier in cls.instances:
            the_dict[supplier.name] = {"min_output_rate": supplier.min_output_rate,
                                       "max_output_rate": supplier.max_output_rate,
                                       "output_rate": supplier.output_rate,
                                       "output_product": supplier.output_product.name
                                       }
        return the_dict

    @staticmethod
    def get_graph():
        return []
