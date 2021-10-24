import pandas as pd
import numpy as np
from fetch import DataSet
from scenarios import BalanceScenarioFactory
from utils import print_vector
from output import Output

dataset = DataSet()

# supplier = 'PL-1721'
# sku = 85735
# scenario = 1

# supplier = 'PL-1721'
# sku = 85728
# scenario = 2

# supplier = 'PL-1505'
# sku = 85023
# scenario = 3

supplier = 'PL-1505'
sku = 88840
scenario = 4

grid = dataset.select_grid(supplier = supplier, sku = sku)

x_opt_dist, x_opt_dep, x_opt_hub = BalanceScenarioFactory.create(grid, scenario=scenario).solve()
print_vector(x_opt_dist)
print_vector(x_opt_dep)
print_vector(x_opt_hub)

output = Output()
dep_codes, dist_codes = grid.get_location_codes()
output.add_data(supplier, sku, 'DEPOT', dep_codes, x_opt_dep)
output.add_data(supplier, sku, 'DEPOT', [supplier], [x_opt_hub])
output.add_data(supplier, sku, 'DIST', dist_codes, x_opt_dist)
output.print('output.csv')
