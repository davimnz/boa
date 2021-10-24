import numpy as np
import pandas as pd

class DataSet:
    def __init__(self):
        self.data = pd.read_csv('../../data/data.csv', delimiter=';', decimal=',')

    def select_grid(self, supplier='PL-1505', sku=85023):
        return Grid(self.data, supplier, sku)
    
    def list_grids(self):
        columns = ['Supply Site Code', 'SKU', 'Scenario']
        return self.data.drop_duplicates(columns)[columns]


class Grid:
    def __init__(self, data, supplier, sku):
        supplier_data = data[data['Supply Site Code'] == supplier]
        self.grid = supplier_data[supplier_data['SKU'] == sku]
        depots_including_hub = self.grid[self.grid['Location Type'] == 'DEP']
        self.dep = depots_including_hub[depots_including_hub['Location Code'] != supplier]
        self.hub = self.grid[self.grid['Location Code'] == supplier]
        self.dist = self.grid[self.grid['Location Type'] == 'DIST']

    def get_current_stock(self):
        CURRENT_STOCK_LABEL = 'Closing Stock'
        return self.dist[CURRENT_STOCK_LABEL].values, self.dep[CURRENT_STOCK_LABEL].values, self.hub[CURRENT_STOCK_LABEL].values

    def get_total_current_stock(self):
        dist, dep, hub = self.get_current_stock()
        return np.hstack([dist, dep, hub])

    def get_max_stock(self):
        MAX_LABEL = "MaxDOC (Hl)"
        return self.dist[MAX_LABEL].values, self.dep[MAX_LABEL].values, self.hub[MAX_LABEL].values

    def get_min_stock(self):
        MIN_LABEL = "MinDOC (Hl)"
        return self.dist[MIN_LABEL].values, self.dep[MIN_LABEL].values, self.hub[MIN_LABEL].values

    def get_reorder_point(self):
        REORDER_POINT_LABEL = "Reorder Point (Hl)"
        return  self.dist[REORDER_POINT_LABEL].values, self.dep[REORDER_POINT_LABEL].values, self.hub[REORDER_POINT_LABEL].values

    def get_available(self):
        AVAILABLE_LABEL = 'Available to Deploy'
        return self.hub[AVAILABLE_LABEL].values

    def get_orders(self):
        ORDERS_LABEL = 'Distributor Orders'
        return self.dist[ORDERS_LABEL].values

    def get_sizes(self):
        return len(self.dist), len(self.dep)

    def get_location_codes(self):
        LOCATION_CODE_LABEL = 'Location Code'
        return self.dist[LOCATION_CODE_LABEL].values, self.dep[LOCATION_CODE_LABEL].values
