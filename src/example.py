import pandas as pd
import numpy as np
from features.fetch import DataSet
from model.scenarios import BalanceScenarioFactory
from features.output import DistributionOutput, ExchangesOutput
from model.utils import print_vector, QPSolver
from model.exchanges import ExchangesSolver
dataset = DataSet()

# supplier = 'PL-1601'
# sku = 92102
# scenario = 0

supplier = 'PL-1505'
sku = 85023
scenario = 3

# supplier = 'PL-1721'
# sku = 85728
# scenario = 2

# supplier = 'PL-1505'
# sku = 85023
# scenario = 3

# supplier = 'PL-1901'
# sku = 85001
# scenario = 4

grid = dataset.select_grid(supplier = supplier, sku = sku)

qpsolver = QPSolver('quadprog')

balanceSolver = BalanceScenarioFactory.create(grid, scenario=scenario)
balanceSolver.solve(qpsolver)
x_opt_dist, x_opt_dep, x_opt_hub = balanceSolver.get_xopt_per_type()
# print_vector(x_opt_dist)
# print_vector(x_opt_dep)
# print_vector(x_opt_hub)

distributionOutput = DistributionOutput()
distributionOutput.add_data(grid, x_opt_dist, x_opt_dep, x_opt_hub)
distributionOutput.print('output.csv')

n = grid.get_size()
location_codes = grid.get_all_location_codes()
supplier_distances = grid.get_supplier_distances()
destination_distances = grid.get_destination_distances()

print(location_codes)
print('Distancias do fornecedor')
print_vector(supplier_distances)
print('Distancias ao destino')
print_vector(destination_distances)

from_supply, exchanges = ExchangesSolver(grid, x_opt_dist, x_opt_dep, x_opt_hub, supplier_distances, destination_distances).solve()
exchangesOutput = ExchangesOutput()
exchangesOutput.add_data(supplier, sku, location_codes, from_supply, exchanges)
exchangesOutput.print('exchanges_output.csv')

xopt = np.hstack([x_opt_dist, x_opt_dep, [x_opt_hub]])
print('Estoque otimizado')
print_vector(xopt)
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