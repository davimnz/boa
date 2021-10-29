from features.fetch import DataSet
from features.output import ExchangesOutput
from model.exchanges import ExchangesSolver
import numpy as np


def solve_all(dataset, verbose=False, with_redistribution=True, output_file = None):
    exchangesOutput = ExchangesOutput()
    grids = dataset.list_grids()

    for _, g in grids.iterrows():
        supplier = g['Supply Site Code']
        sku = g['SKU']
        grid = dataset.select_grid(supplier=supplier, sku=sku)
        x_opt_dist, x_opt_dep, x_opt_hub = grid.get_xopt()
        supplier_distances = grid.get_supplier_distances()
        destination_distances = grid.get_destination_distances()
        location_codes = grid.get_all_location_codes()

        x_opt = np.concatenate([x_opt_dist, x_opt_dep, x_opt_hub])
        current_stock = grid.get_total_current_stock()
        if with_redistribution:
            from_supply, exchanges = ExchangesSolver(grid, x_opt_dist, x_opt_dep,
                                                    x_opt_hub, supplier_distances,
                                                    destination_distances).solve()
        else:
            exchanges = np.matrix((0, 0))
            from_supply = x_opt - current_stock
        exchangesOutput.add_data(supplier, sku, location_codes,
                                 from_supply, exchanges)

    exchangesOutput.print(output_file)

dataset_with_redistribution = DataSet('output/distribution_output_quadprog.csv')
dataset_without_redistribution = DataSet('output/no_redistribution.csv')

solve_all(dataset_without_redistribution, with_redistribution=False, output_file='output/exchanges_output.csv')
solve_all(dataset_with_redistribution, with_redistribution=True, output_file='output/exchanges_output_no_redistribution.csv')
