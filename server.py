from flask import render_template
from sources.api import app

# app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def main_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
