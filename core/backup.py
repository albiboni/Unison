from flask import Flask, request, session, g, redirect, url_for, safe_join, Response, \
    abort, render_template, make_response, send_from_directory, send_file, has_request_context, jsonify
from jinja2 import Markup, escape
from core.plant_graph.json_parser import read_json, write_json
from core.ale_optimizer import maximize_output


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')


@app.route('/import', methods=["GET", "POST"])
def run_python():
    json = request.get_json()
    print(json)
    output_machine = read_json(json_dict=json)
    maximize_output(output_machine)
    return write_json(output_machine)


if __name__ == '__main__':
    app.run()
