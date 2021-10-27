import pandas as pd
import numpy as np
from features.fetch import OptimizedDataSet
from model.scenarios import BalanceScenarioFactory
from model.utils import print_vector, QPSolver
from model.output import Output
from model.exchanges import ExchangesSolver

dataset = OptimizedDataSet()

def solve_all(verbose=False):
    output = Output()
    grids = dataset.list_grids()

    for _, g in grids.iterrows():
        supplier = g['Supply Site Code']
        sku = g['SKU']
        grid = dataset.select_grid(supplier = supplier, sku = sku)
        x_opt_dist, x_opt_dep, x_opt_hub = grid.get_xopt()
        from_supply, exchanges = Step2Solver(grid, x_opt_dist, x_opt_dep, x_opt_hub).solve()
        # output_step_2.add_data(from_supply, exchanges)

    output.print('output_step2.csv')


solve_all()