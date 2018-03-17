"""
Created by Alejandro Daniel Noel
"""
from weakref import WeakSet
from typing import List

from core.plant_graph.Product import Product


class ExternalSupplier:
    instances = WeakSet()

    def __new__(cls, output_product: Product, next_machines: List = (),
                min_output_rate: float = 0.0, max_output_rate: float = 10000000000000.0):
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
        self.output_product = output_product
        self.next_machines = next_machines

        print(f"    A generic supplier of <{output_product.name}> has been created")

        cls.instances.add(self)
        return self

    def __hash__(self):
        return hash(self.name)
