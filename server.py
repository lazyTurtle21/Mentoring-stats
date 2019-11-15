from flask import render_template, url_for, redirect
from sources.api import app

app.config['JSON_AS_ASCII'] = False
app.config['CREDS'] = 'credentials.json'


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/ralabs_logo.png'))


if __name__ == '__main__':
    app.run(debug=True)
