import pandas as pd
from constants import *
class Output:
    def __init__(self):
        self.df = None

    def add_data(self, supplier, sku, location_type, location_codes, scenario, x_opt):
        data = [ [supplier, sku, location_type, lc, scenario, x] for (lc, x) in zip(location_codes, x_opt)]
        new_df = pd.DataFrame(data, 
            columns = [SUPPLY_SITE_CODE_LABEL, SKU_LABEL, LOCATION_TYPE_LABEL, 
                        LOCATION_CODE_LABEL, SCENARIO_LABEL, XOPT_LABEL])
        self.update(new_df)
    
    def update(self, new_df):
        if self.df is None:
            self.df = new_df
        else:
            self.df = self.df.append(new_df)

    def print(self, output_file):
        self.df.to_csv(output_file,  index=False, float_format='%.1f')