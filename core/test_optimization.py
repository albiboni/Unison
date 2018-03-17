"""
Created by Alejandro Daniel Noel
"""
from core import ale_optimizer
from core.plant_graph.ExternalSupplier import ExternalSupplier
from core.plant_graph.machine import Machine
from core.plant_graph.product import Product
from core.plant_graph.json_parser import write_json

ExternalSupplier.reset_instance_tracker()
flour = Product(name="flour", units='kg')
water = Product(name="water", units='liter')
cream = Product(name="cream", units='kg')
dough = Product(name="dough", units='kg', sub_products_quantities={flour: 0.4, water: 0.6})
filling = Product(name="filling", units='liter', sub_products_quantities={cream: 0.7, flour: 0.3})
pie = Product(name="pie", units='unit', sub_products_quantities={dough: 0.5, filling: 0.2})
dough_maker1 = Machine(name="Dough maker 1", min_batch_time=200, max_batch_time=1000, batch_time=500, batch_size=50,
                      output_product=dough)
dough_maker2 = Machine(name="Dough maker 2", min_batch_time=200, max_batch_time=1000, batch_time=500, batch_size=50,
                      output_product=dough)
filling_maker1 = Machine(name="Filling maker 1", min_batch_time=100, max_batch_time=500.0, batch_time=150, batch_size=20,
                         output_product=filling)
filling_maker2 = Machine(name="Filling maker 2", min_batch_time=100, max_batch_time=500.0, batch_time=150, batch_size=20,
                         output_product=filling)
filling_maker3 = Machine(name="Filling maker 3", min_batch_time=100, max_batch_time=500.0, batch_time=150, batch_size=20,
                         output_product=filling)
output_machine = Machine(name="Pie maker", min_batch_time=10, max_batch_time=300, batch_time=50, batch_size=30,
                         output_product=pie,
                         suppliers=[dough_maker1, dough_maker2, filling_maker1, filling_maker2, filling_maker3], delays=[22.3, 20.1,  13.2, 11.1, 15.3])

# maximum_output = ale_optimizer.maximize_output(output_machine)
maximum_output = ale_optimizer.optimize_topology(output_machine, 1.55)
# maximum_output = ale_optimizer.maximize_output(output_machine)
# output_machine.set_supplier_rates(0.2)
write_json(output_machine, "Optimized_plant.json")
print("\nMaximum production is 1 pie every {:.2f} seconds".format(1 / maximum_output))
