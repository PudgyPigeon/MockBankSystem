#!/bin/bash

# Add the current working directory to the Python path
export PYTHONPATH=$PYTHONPATH:`pwd`

python ./entrypoint.py