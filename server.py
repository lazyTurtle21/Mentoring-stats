from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, Flask
from sources.api import api

app = Flask(__name__)
main = Blueprint('app', __name__)

app.config['JSON_AS_ASCII'] = False
app.register_blueprint(api, url_prefix='/api/v1')


@app.route('/')
def main_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
