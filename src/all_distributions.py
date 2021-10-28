import numpy as np
from features.fetch import DataSet
from model.scenarios import BalanceScenarioFactory
from model.utils import print_vector, QPSolver
from features.output import DistributionOutput

dataset = DataSet()


def solve_all(solver, verbose=False):
    output = DistributionOutput()
    grids = dataset.list_grids()
    qpsolver = QPSolver(solver)
    print('\nStarting with solver', solver)

    for _, g in grids.iterrows():
        supplier = g['Supply Site Code']
        sku = g['SKU']
        scenario = g['Scenario']

        grid = dataset.select_grid(supplier=supplier, sku=sku)
        # TODO: no hub
        if len(grid.hub) == 0:
            continue
        x_opt_dist, x_opt_dep, x_opt_hub = BalanceScenarioFactory.create(
            grid, scenario=scenario).solve(qpsolver)
        if verbose:
            print_vector(x_opt_dist)
            print_vector(x_opt_dep)
            print_vector(x_opt_hub)

        dist_codes, dep_codes = grid.get_location_codes()
        current_stock_dist, current_stock_dep, current_stock_hub = grid.get_current_stock()
        available = grid.get_available()
        output.add_data(supplier, sku, 'DIST', dist_codes,
                        scenario, x_opt_dist, current_stock_dist, available)
        output.add_data(supplier, sku, 'DEP', dep_codes,
                        scenario, x_opt_dep, current_stock_dep, available)
        output.add_data(supplier, sku, 'DEP', [supplier], scenario, [
                        x_opt_hub], current_stock_hub, available)

    output.print('output/distribution_output_' + solver + '.csv')
    print('Preferred solves:', qpsolver.preferred_solves_count)
    print('Fallback solves:', qpsolver.fallback_solves_count)
    times = qpsolver.get_times()
    print('Avg time: %.2f ms' % (np.mean(times) * 1000))
    print('Std time: %.2f ms' % (np.std(times) * 1000))
    print('Min time: %.2f ms' % (np.min(times) * 1000))
    print('Max time: %.2f ms' % (np.max(times) * 1000))


solvers = ['cvxopt', 'quadprog', 'osqp']
for solver in solvers:
    solve_all(solver)
