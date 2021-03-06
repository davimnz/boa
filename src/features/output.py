import pandas as pd
from .constants import *
import numpy as np

class DistributionOutput:
    def __init__(self):
        self.df = None

    def add_data(self, grid, x_opt_dist, x_opt_dep, x_opt_hub):
        new_df = grid.dist.assign(x_opt=x_opt_dist)
        new_df = new_df.append(grid.dep.assign(x_opt=x_opt_dep))
        new_df = new_df.append(grid.hub.assign(x_opt=x_opt_hub))
        self.update(new_df)
    
    def update(self, new_df):
        if self.df is None:
            self.df = new_df
        else:
            self.df = self.df.append(new_df)

    def print(self, output_file):
        self.df.to_csv(output_file,  index=False, float_format='%.1f', sep=';', decimal=',')

class ExchangesOutput:
    def __init__(self):
        self.df = None

    def add_data(self, supplier, sku, location_codes, from_supply, exchanges):
        data = [ [supplier, sku, 'Available', d, x] for (d, x) in zip(location_codes, from_supply) if x != 0]
        np.save( 'test', exchanges)

        nonzero_indexes = np.where(abs(exchanges)>1e-3)
        nonzero_x = nonzero_indexes[0]
        nonzero_y = nonzero_indexes[1]

        for k in range(len(nonzero_x)):
            x = nonzero_x[k]
            y = nonzero_y[k]
            data.append([supplier, sku, location_codes[x], location_codes[y], exchanges[x, y]])

       
        new_df = pd.DataFrame(data, 
            columns = [SUPPLY_SITE_CODE_LABEL, SKU_LABEL, 'Origin', 
                        'Destiny', 'Amount'])
        self.update(new_df)
    
    def update(self, new_df):
        if self.df is None:
            self.df = new_df
        else:
            self.df = self.df.append(new_df)

    def print(self, output_file):
        self.df.to_csv(output_file,  index=False, float_format='%.1f', sep=';', decimal=',')