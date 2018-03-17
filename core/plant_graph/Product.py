"""
Created by Alejandro Daniel Noel
"""
from typing import List, Dict


class Product:
    def __init__(self, name, units, sub_products_quantities: Dict['Product', float] = None):
        self.name = name
        self.units = units
        self.sub_products_quantities = sub_products_quantities or {}

    @property
    def sub_products_list(self):
        return list(self.sub_products_quantities.keys())

    def __hash__(self):
        return hash(self.name)

    def to_dict(self):
        the_dict = {}
        for sub_product in self.sub_products_list:
            the_dict = {**the_dict, **sub_product.to_dict()}
        the_dict[self.name] = {"units": self.units,
                               "sub_products": {sub_product.name: self.sub_products_quantities[sub_product] for sub_product in self.sub_products_list}
                               }
        return the_dict
