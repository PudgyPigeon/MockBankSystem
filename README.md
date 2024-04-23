# How to Run

# Localhost
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

# Dockerized
This document assumes the Docker daemon has been installed in the user's environment.

If not, please install the necessary tools to build out a Docker image.

Once that is done, simply run:

```
./dockerized_run.sh {arg1} {arg2}

Ex.) ./dockerized_run.sh build current_terminal
```
### Valid arguments for Arg1
build: Build out the docker image
skip: Skip building the docker iamge
### Valid arguments for Arg2
detached: Run docker container in detached mode. Port 80 is mapped to 80. Allows exec commands/SSH, attaching to IDE.
current_terminal: Run docker container in line - will immediately start the `bank_app` process

## Password for both users in Git repo (bank_app/data/bank_system.csv) 
"hello"

# Unit tests
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