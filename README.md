# BOA - Beverage Optimal Allocation

## Overview
todo

### Problem
To avoid misconceptions, we explain some concepts before introducing the problem. There are three types of a site: supply site, distributor, and depot. A supply site produces beverages for distributors and depots. A distributor can send a product to a depot, and vice versa. However, a supply site cannot receive a product from distributor or depot. On these premisses, we define the first version of the problem. Moreover, the second version assumes that products of distributors cannot be send to depots, and vice versa.

Given the data set of Ambev's supply chain, we want to distribute the available products between supply sites, distributors, and depots in order to have a balanced stock in all sites with a minimum transportation cost. The problem can be broken into two subproblems: evaluation of the optimal stock in each site, and generation of the optimal exchange map. The optimal stock should be evaluated in relation to some reference stock, such as reorder stock or maximum stock. The exchange map of a product is defined as the amount of product that leaves or goes to each site. Furthermore, the geopositioning of each site should be used to estimate the distance between two sites. We solved the two subproblems for the two versions of the problem.

### Solution
The solution can be divided into four steps: data preprocessing, evaluation of optimal stock, generation of optimal exchange map, and definition of metrics to compare each version of the problem. The following paragraphs explain each step.

We removed all rows with infinite values in the Ambev's data set, since they had a maximum stock of zero. We generated geopositioning for all sites based on longitude and latitude of Belgium cities. The sites' position were generated using a uniform distribution with a fixed seed for reproducibility purposes.

We chose the reference stock based on the scenario of a grid.

todo


#### Solution Architecture

![](figures/readme/architecture.svg)


## Dependencies
Install the requirements in `requirements.txt` in a virtual environment, such as `venv`. [You can find venv installation guide here.](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

## Run

Run `make all` to execute all main source files if you have `make`. Otherwise, run the following files in order.

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
