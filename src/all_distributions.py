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
        balanceSolver = BalanceScenarioFactory.create(grid, scenario=scenario)
        balanceSolver.solve(qpsolver)
        x_opt_dist, x_opt_dep, x_opt_hub = balanceSolver.get_xopt_per_type()

        if verbose:
            print_vector(x_opt_dist)
            print_vector(x_opt_dep)
            print_vector(x_opt_hub)

        output.add_data(grid, x_opt_dist, x_opt_dep, x_opt_hub)


    output.print('output/distribution_output_' + solver + '.csv')
    print('Preferred solves:', qpsolver.preferred_solves_count)
    print('Fallback solves:', qpsolver.fallback_solves_count)
    times = qpsolver.get_times()
    print('Avg time: %.2f ms' % (np.mean(times) * 1000))
    print('Std time: %.2f ms' % (np.std(times) * 1000))
    print('Min time: %.2f ms' % (np.min(times) * 1000))
    print('Max time: %.2f ms' % (np.max(times) * 1000))
    return times

import matplotlib.pyplot as plt
all_times = {}
ax = plt.axes()

solvers = ['cvxopt', 'quadprog', 'osqp']
for i, solver in enumerate(solvers):
    times = solve_all(solver)
    ax.boxplot(1000*times, positions = [i+1], widths = 0.6)
    
    np.save('times_'+solver, times)

plt.ylim(0, 2)
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(solvers)
plt.title('Comparação dos tempos dos solvers')
plt.ylabel('Tempo (ms)')
plt.savefig('figures/qp_solver_comparison.png', transparent=True)
plt.show()