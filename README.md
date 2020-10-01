# Mentoring-stats
> A flask app which shows the mentoring statistics.



## How to run:

* To run tool that copies events from one calendar to another, run:

```sh
git clone https://github.com/lazyTurtle21/Mentoring-stats.git
pip install -r requirements.txt
cd Mentoring-stats/
python3 ./sources/copy_mentoring_events.py --initial INITIAL --to TO
```
Also, you can run help to see detailed description:
```sh
python3 ./sources/copy_mentoring_events.py -h
```

* In case you want to run the UI along with API:

```sh
python3 server.py
```
* To run only API, run:
```sh
python3 sources/api.py
```


After that, a window with google account login should open. Give permissions, and then the app is available under this [link](http://127.0.0.1:5000/).
The API is available under [this](http://127.0.0.1:5000/api/v1)

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
