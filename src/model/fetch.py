import numpy as np
import pandas as pd

class DataSet:
    def __init__(self):
        self.data = pd.read_csv('data/data.csv', delimiter=';', decimal=',')

    def get_grid(self, supplier='PL-1505', sku=85023):
        supplier = self.data[self.data['Supply Site Code'] == supplier]
        grid = supplier[supplier['SKU'] == sku]
        return grid

    def get_depots(self, supplier='PL-1505', sku=85023, remove_hub=False):
        grid = self.get_grid(supplier, sku)
        depots = grid[grid['Location Type'] == 'DEP']
        depots = depots[depots['Location Code'] != supplier]
        return depots

    def get_hub(self, supplier='PL-1505', sku=85023):
        grid = self.get_grid(supplier, sku)
        hub = grid[grid['Location Code'] == supplier]
        return hub

    def get_dist(self, supplier='PL-1505', sku=85023, remove_hub=False):
        grid = self.get_grid(supplier, sku)
        depots = grid[grid['Location Type'] == 'DIST']
        dists = depots[depots['Location Code'] != supplier]
        return dists