from features.fetch import DataSet
from features.output import ExchangesOutput
from model.exchanges import ExchangesSolver

dataset = DataSet('output/distribution_output_quadprog.csv')


def solve_all(verbose=False):
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
        from_supply, exchanges = ExchangesSolver(grid, x_opt_dist, x_opt_dep,
                                                 x_opt_hub, supplier_distances,
                                                 destination_distances).solve()
        exchangesOutput.add_data(supplier, sku, location_codes,
                                 from_supply, exchanges)

    exchangesOutput.print('output/exchanges_output.csv')


solve_all()
