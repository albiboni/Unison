"""
Created by Alejandro Daniel Noel
"""
from core.plant_graph.ExternalSupplier import ExternalSupplier
from core.plant_graph.Machine import Machine
from core.plant_graph.Product import Product
from core.plant_graph.json_parser import write_json
from core import ale_optimizer


ExternalSupplier.reset_instance_tracker()
flour = Product(name="flour", units='kg')
water = Product(name="water", units='liter')
cream = Product(name="cream", units='kg')
dough = Product(name="dough", units='kg', sub_products_quantities={flour: 0.3, water: 0.5})
filling = Product(name="filling", units='liter', sub_products_quantities={cream: 0.5, flour: 0.1})
pie = Product(name="pie", units='unit', sub_products_quantities={dough: 0.4, filling: 0.6})
dough_maker = Machine(name="Dough maker", min_batch_time=200, max_batch_time=1000, batch_time=500, batch_size=50,
                           output_product=dough)
filling_maker = Machine(name="Filling maker", min_batch_time=100, max_batch_time=500.0, batch_time=150, batch_size=20,
                             output_product=filling)
output_machine = Machine(name="Pie maker", min_batch_time=30, max_batch_time=300, batch_time=50, batch_size=30,
                              output_product=pie,
                              suppliers=[dough_maker, filling_maker], delays=[1.3, 1.2])

output_machine = ale_optimizer.optimize_plant(output_machine)
write_json(output_machine, "Optimized_plant.json")

