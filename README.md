# BOA - Beverage Optimal Allocation

## Overview
todo

### Problem
todo

### Solution
todo


#### Solution Architecture
todo


## Dependencies
Install the requirements in `requirements.txt` in a virtual environment, such as `venv`. [You can find venv installation guide here.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

## Run

Run `make all` to execute all source files if you have `make`. Otherwise, run the following `src` files in order.
  - Features
    - `preprocessing.py` removes useless data and generates geopositioning to sites.
  - Model
    - `main.py` generates step 1 outputs with desired final stocks
    - `calculate_exchanges` generates step 2 output with all the exhanges needed
  - Visualization
    - `visualization.py` plots stock balance metrics.

## Team
todo
