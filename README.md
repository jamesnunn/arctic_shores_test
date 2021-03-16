## Installation
```
git clone arctic_shores_test
virtualenv env
pip install -r requirements

# Run some tests
cd arctic_shores_test
pytest test
```

## Create the DB
```
python database.py
```

## Run the test server
```
cd arctic_shores_test
uvicorn app:app --reload
```

## Check the database is empty, will return csv with header only
```
curl http://127.0.0.1:8000/get-candidates/
```

## Add the candidates
```
cat candidates.json | curl http://127.0.0.1:8000/create-candidates/ -d @-
```

## Get the candidates as CSV
```
curl http://127.0.0.1:8000/get-candidates/
# or:
curl http://127.0.0.1:8000/get-candidates/ > output.csv
```
