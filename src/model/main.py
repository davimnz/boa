import pandas as pd
import numpy as np
from fetch import DataSet
from scenarios import BalanceScenarioFactory
from utils import print_vector
from output import Output

dataset = DataSet()
output = Output()

grids = dataset.list_grids()

for _, g in grids.iterrows():
    supplier = g['Supply Site Code']
    sku = g['SKU']
    scenario = g['Scenario']
    # TODO
    if scenario == 0:
        continue
    
    grid = dataset.select_grid(supplier = supplier, sku = sku)
    # TODO: no hub
    if len(grid.hub) == 0:
        continue
    x_opt_dist, x_opt_dep, x_opt_hub = BalanceScenarioFactory.create(grid, scenario=scenario).solve()
    print_vector(x_opt_dist)
    print_vector(x_opt_dep)
    print_vector(x_opt_hub)

    dep_codes, dist_codes = grid.get_location_codes()
    output.add_data(supplier, sku, 'DEPOT', dep_codes, x_opt_dep)
    output.add_data(supplier, sku, 'DEPOT', [supplier], [x_opt_hub])
    output.add_data(supplier, sku, 'DIST', dist_codes, x_opt_dist)

output.print('output.csv')
