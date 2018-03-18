from flask import Flask, request, session, g, redirect, url_for, safe_join, Response, \
    abort, render_template, make_response, send_from_directory, send_file, has_request_context, jsonify
from jinja2 import Markup, escape

from core import ale_optimizer
from core.plant_graph.ExternalSupplier import ExternalSupplier
from core.plant_graph.machine import Machine
from core.plant_graph.product import Product
from core.plant_graph.json_parser import write_json

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')


@app.route('/import', methods=["GET", "POST"])
def run_python():
    json = request.get_json()
    print(json)
    ExternalSupplier.reset_instance_tracker()
    flour = Product(name="flour", units='kg')
    water = Product(name="water", units='liter')
    cream = Product(name="cream", units='kg')
    dough = Product(name="dough", units='kg', sub_products_quantities={flour: 0.4, water: 0.6})
    filling = Product(name="filling", units='liter', sub_products_quantities={cream: 0.4, flour: 0.3})
    pie = Product(name="pie", units='unit', sub_products_quantities={dough: 0.4, filling: 0.4})
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
                             suppliers=[dough_maker1, dough_maker2, filling_maker1, filling_maker2, filling_maker3],
                             delays=[22.3, 20.1, 13.2, 11.1, 15.3])

    # maximum_output = ale_optimizer.maximize_output(output_machine)
    maximum_output = ale_optimizer.optimize_topology(output_machine, 1.55)
    print("\nMaximum production is 1 pie every {:.2f} seconds".format(1 / maximum_output))
    write_json(output_machine, filename="../Optimized_plant2.json")

    return write_json(output_machine)


if __name__ == '__main__':
    app.run()

