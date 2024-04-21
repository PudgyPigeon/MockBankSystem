# How to Run
To install dependencies for this module run:
```
pip install -r requirements.txt
```

Then in your terminal run:

```
python3 -m entrypoint.py

or 

python -m entrypoint.py
```

Then follow the onscreen prompts to use the mock banking system.

You may view the CSV state file within the data directory.

### Password for both users in Git repo (/data/bank_system.csv) 
"hello"

## Unit tests
Run the unit test script in order to run tests
Script adds CWD to python path
```
./run_unit_tests.sh
```
## Things I Would Add Given More Time
- Containerization of runtime with Docker image or Conda Envs
- Refactor mock dataframes in Unit tests to utilize mock_file_paths with real CSVs with fake data instead
    - currently, read operations are mocked correctly but polars.write_csv() can't easily be mocked to a DF
- More unit test coverage if given more time
- More error handling surrounding incorrect input validation
- More custom exceptions
- Collapse common functionality into simpler system design
- Use Rich-Click Package for pretty printing and bette formatting
- Move entrypoint into a /src dir (or bank_app, etc) where services and data will be too
      - Refactoring this would break imports in tests however
