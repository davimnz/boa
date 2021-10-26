# BOA - Beverage Optimal Allocation

## Overview
todo

### Problem
Given the data set of Ambev's supply chain, distribute the available products between supply sites, distributors, and depots in order to have a balanced stock in all sites. Moreover, calculate the optimal exchange of products between supply sites, distributors, and depots considering the geopositioning of each site.

### Solution
todo


#### Solution Architecture
todo


## Dependencies
Install the requirements in `requirements.txt` in a virtual environment, such as `venv`. [You can find venv installation guide here.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

## Run

Run `make all` to execute all source files if you have `make`. Otherwise, run the following `src` files in order.

````
python3 src/features/preprocessing.py      # removes useless data and generates geopositioning to sites
python3 src/model/main.py                  # generates first step output with desired final stocks
python3 src/model/calculate_exchanges.py   # generates second step output with all exchanges needed
python3 src/visualization/plot_metric.py   # plots stock balance metrics
python3 src/visualization/plot_grid.py     # plots grid stocks after/before rebalancing and exchange map for a given grid
````

## Team

| [<img src="https://avatars.githubusercontent.com/u/56287238?v=4" width="115"><br><sub>@alexandremr01</sub>](https://github.com/alexandremr01) | [<img src="https://avatars.githubusercontent.com/u/63565370?v=4" width="115"><br><sub>@davimnz</sub>](https://github.com/davimnz) |
| :---: | :---: |
