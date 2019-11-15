from flask import render_template
from sources.api import app

app.config['JSON_AS_ASCII'] = False
app.config['CREDS'] = 'credentials.json'


@app.route('/')
def main_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
