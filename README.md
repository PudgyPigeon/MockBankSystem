# How to Run
To install dependencies for this module run:
```
pip install -r requirements.txt
```

Then in your terminal run:

```
./run_bank_app.sh
```

Then follow the onscreen prompts to use the mock banking system.

You may view the CSV state file within the data directory.

### Password for both users in Git repo (bank_app/data/bank_system.csv) 
"hello"

## Unit tests
Run the unit test script in order to run tests
Script adds CWD to python path
```
./run_unit_tests.sh
```
## Things I Would Add Given More Time
- Containerization of runtime with Docker image or Conda Envs
- More error handling surrounding incorrect input validation
- More custom exceptions
- Collapse common functionality into simpler system design
- Use Rich-Click Package for pretty printing and bette formatting