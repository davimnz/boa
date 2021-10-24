import pandas as pd
import numpy as np
from fetch import DataSet
from scenarios import BalanceScenarioFactory
from output import Output
from utils import print_vector, QPSolver
from step2 import Step2Solver
dataset = DataSet()

# supplier = 'PL-1601'
# sku = 92102
# scenario = 0

supplier = 'PL-1721'
sku = 85735
scenario = 1

# supplier = 'PL-1721'
# sku = 85728
# scenario = 2

# supplier = 'PL-1505'
# sku = 85023
# scenario = 3

# supplier = 'PL-1505'
# sku = 88840
# scenario = 4

grid = dataset.select_grid(supplier = supplier, sku = sku)
qpsolver = QPSolver('quadprog')

x_opt_dist, x_opt_dep, x_opt_hub = BalanceScenarioFactory.create(grid, scenario=scenario).solve(qpsolver)
# print_vector(x_opt_dist)
# print_vector(x_opt_dep)
# print_vector(x_opt_hub)

output = Output()
dep_codes, dist_codes = grid.get_location_codes()
output.add_data(supplier, sku, 'DEPOT', dep_codes, x_opt_dep)
output.add_data(supplier, sku, 'DEPOT', [supplier], [x_opt_hub])
output.add_data(supplier, sku, 'DIST', dist_codes, x_opt_dist)
output.print('output.csv')

from_supply, exchanges, A, b, solution = Step2Solver(grid, x_opt_dist, x_opt_dep, x_opt_hub).solve()

xopt = np.hstack([x_opt_dist, x_opt_dep, [x_opt_hub]])
n = len(from_supply)
deltas = np.zeros((n))
for i in range(n):
    deltas[i] = from_supply[i] + np.sum(exchanges[:, i]) - np.sum(exchanges[i, :])
current_stocks = grid.get_total_current_stock()
final_stock = current_stocks + deltas
print('Diferenças entre o otimizado e o obtido')
print_vector(final_stock - xopt)
print('Estoque vindo da fábrica')
print_vector(from_supply)
print('Trocas de estoque')
print_vector(exchanges)