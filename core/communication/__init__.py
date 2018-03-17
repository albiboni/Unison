from flask import Flask, request, session, g, redirect, url_for, safe_join, Response, \
    abort, render_template, make_response, send_from_directory, send_file, has_request_context
from jinja2 import Markup, escape

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')


@app.route('/export', methods=["GET", "POST"])
def export_data():
    with open("test.json", "r") as f:  # TODO: Change that
        json = " ".join(f.readlines())
    return render_template('export_data.html', json=json)


@app.route('/import', methods=["GET", "POST"])
def import_data():
    return render_template('import_data.html')


@app.route('/run_python', methods=["GET", "POST"])
def run_python():
    json = str(request.args.get('json') or None)
    if json is not None:
        print(json)
        return render_template('export_data.html', json=json)


if __name__ == '__main__':
    app.run()