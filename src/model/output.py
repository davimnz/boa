import pandas as pd
class Output:
    def __init__(self):
        self.df = None

    def add_data(self, supplier, sku, location_type, location_codes, x_opt):
        data = [ [supplier, sku, location_type, lc, x] for (lc, x) in zip(location_codes, x_opt)]
        new_df = pd.DataFrame(data, columns = ['supplier', 'sku', 'location_type', 'location_code', 'x_opt'])

        if self.df is None:
            self.df = new_df
        else:
            self.df = self.df.append(new_df)

    def print(self, output_file):
        self.df.to_csv(output_file,  index=False, float_format='%.1f')