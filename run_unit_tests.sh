#!/bin/bash

# Add the current working directory to the Python path
export PYTHONPATH=$PYTHONPATH:`pwd`

# Run pytest
python -m pytest