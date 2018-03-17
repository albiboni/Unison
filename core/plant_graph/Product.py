"""
Created by Alejandro Daniel Noel
"""
from typing import List, Dict


class Product:
    def __init__(self, name, units, sub_products: Dict['Product', float] = None):
        self.name = name
        self.units = units
        self._sub_products = sub_products or {}

    @property
    def sub_products_list(self):
        return list(self._sub_products.keys())

    @property
    def sub_products_quantities(self):
        return self._sub_products

    def __hash__(self):
        return hash(self.name)
