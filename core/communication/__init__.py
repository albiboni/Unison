from flask import Flask, request, session, g, redirect, url_for, safe_join, Response, \
    abort, render_template, make_response, send_from_directory, send_file, has_request_context
from jinja2 import Markup, escape

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')


@app.route('/run_python', methods=["GET", "POST"])
def run_python():
    json = request.get_json()
    if json is not None:
        print('DO PYTHON')
    return render_template('export_data.html')


if __name__ == '__main__':
    app.run()