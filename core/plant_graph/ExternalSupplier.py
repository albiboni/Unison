"""
Created by Alejandro Daniel Noel
"""
from typing import List
from weakref import WeakSet

from core.plant_graph.Product import Product


class ExternalSupplier:
    _instances = WeakSet()

    def __new__(cls,
                output_product: Product,
                batch_size=10000000, batch_time=0.001, min_batch_time=0.001, max_batch_time=1,
                next_machines: List = None):
        name = 'supplier of ' + output_product.name

        for instance in cls._instances:
            if instance.name == name:
                print(f"    <{name}> already exists, subscribing also to {','.join([f'<{machine.name}>' for machine in next_machines])}")
                instance.next_machines += next_machines
                return instance

        self = object.__new__(ExternalSupplier)
        self.name = name
        self.min_batch_time = float(min_batch_time)
        self.max_batch_time = float(max_batch_time)
        self.batch_time = float(batch_time)
        self.batch_size = float(batch_size)
        self.output_product = output_product
        self.next_machines = next_machines or []

        print(f"    A generic supplier of <{output_product.name}> has been created")

        cls._instances.add(self)
        return self

    @property
    def min_output_rate(self):
        return self.batch_size / self.max_batch_time

    @property
    def max_output_rate(self):
        return self.batch_size / self.min_batch_time

    @property
    def output_rate(self):
        return self.batch_size / self.batch_time

    def __hash__(self):
        return hash(self.name)

    def add_next_machine(self, next_machine):
        self.next_machines.append(next_machine)

    @classmethod
    def to_dict(cls):
        the_dict = {}
        for supplier in cls._instances:
            the_dict[supplier.name] = {"min_batch_time": supplier.min_batch_time,
                                       "max_batch_time": supplier.max_batch_time,
                                       "batch_time": supplier.batch_time,
                                       "batch_size": supplier.batch_size,
                                       "output_product": supplier.output_product.name
                                       }
        return the_dict

    @classmethod
    def reset_instance_tracker(cls):
        cls._instances = WeakSet()
        print("\nExternalSupplier was reset \n")

    @staticmethod
    def get_graph():
        return []

    def get_scheduling(self, end_time, output_units_required):
        return []

    def set_supplier_rates(self, required_output_rate):
        if required_output_rate > self.max_output_rate:
            return False
        else:
            self.batch_time = self.batch_size / required_output_rate
            return True
