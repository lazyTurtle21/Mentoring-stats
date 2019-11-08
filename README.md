# Mentoring-stats
> A flask app which shows the mentoring statistics.



## How to run:

[Clone](https://github.com/lazyTurtle21/Mentoring-stats/archive/master.zip) the repository.
Unzip it, and in the root folder run:
```sh
pip install -r requirements.txt
python server.py
```
After that, a window with google account login should open. Give permissions, and then the app is available under this [link](http://127.0.0.1:5000/).

## Documentation:
Documention can be accessed via several ways(after previous step):
* [/docs/openapi.json](http://127.0.0.1:5000/docs/openapi.json) if you want to see plain json.
* [/docs/swagger_ui](http://127.0.0.1:5000/docs/swagger_ui) if you want to see documentation representation using Swagger UI.
* [/docs/redoc_ui](http://127.0.0.1:5000/docs/redoc_ui) if you want to see documentation representation using ReDoc UI.

## Tests:
To run unittests: 
```sh
cd tests
python <test_name>
```
To see the report of tests coverage:
```sh
cd tests
coverage run <test_name>
coverage report
```
