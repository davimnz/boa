import numpy as np
import pandas as pd
from .constants import *
from .distance import distance
DATA_FILE = 'data/data.csv'
DISTANCE_FILE = 'data/geopositioning.csv'


class DataSet:
    def __init__(self, data_file=DATA_FILE):
        self.data = pd.read_csv(data_file, delimiter=';', decimal=',')
        self.distances = pd.read_csv(DISTANCE_FILE, delimiter=';', decimal=',')

    def get_distance(self, a, b):
        position_a = self.distances[self.distances['code'] == a]
        position_b = self.distances[self.distances['code'] == b]

        return distance(latitude_1=position_a['latitude'], longitude_1=position_a['longitude'],
                        latitude_2=position_b['latitude'], longitude_2=position_b['longitude'])

    def select_grid(self, supplier='PL-1505', sku=85023):
        return Grid(self.data, supplier, sku, self)

    def list_grids(self):
        columns = ['Supply Site Code', 'SKU', 'Scenario']
        return self.data.drop_duplicates(columns)[columns]


class Grid:
    def __init__(self, data, supplier, sku, dataset):
        supplier_data = data[data['Supply Site Code'] == supplier]
        self.grid = supplier_data[supplier_data['SKU'] == sku]
        depots_including_hub = self.grid[self.grid['Location Type'] == 'DEP']
        self.dep = depots_including_hub[depots_including_hub['Location Code'] != supplier]
        self.hub = self.grid[self.grid['Location Code'] == supplier]
        self.dist = self.grid[self.grid['Location Type'] == 'DIST']
        self.supplier = supplier
        self.dataset = dataset

    def get_current_stock(self):
        return self.dist[CURRENT_STOCK_LABEL].values, self.dep[CURRENT_STOCK_LABEL].values, self.hub[CURRENT_STOCK_LABEL].values

    def get_total_current_stock(self):
        dist, dep, hub = self.get_current_stock()
        return np.hstack([dist, dep, hub])

    def get_max_stock(self):
        return self.dist[MAX_LABEL].values, self.dep[MAX_LABEL].values, self.hub[MAX_LABEL].values

    def get_min_stock(self):
        return self.dist[MIN_LABEL].values, self.dep[MIN_LABEL].values, self.hub[MIN_LABEL].values

    def get_reorder_point(self):
        return self.dist[REORDER_POINT_LABEL].values, self.dep[REORDER_POINT_LABEL].values, self.hub[REORDER_POINT_LABEL].values

    def get_available(self):
        return self.hub[AVAILABLE_LABEL].values

    def get_orders(self):
        return self.dist[ORDERS_LABEL].values

    def get_sizes(self):
        return len(self.dist), len(self.dep)

    def get_size(self):
        return len(self.dist) + len(self.dep) + len(self.hub)

    def has_hub(self):
        return len(self.hub) > 0

    def get_xopt(self):
        return self.dist[XOPT_LABEL].values, self.dep[XOPT_LABEL].values, self.hub[XOPT_LABEL].values

    def get_location_codes(self):
        return self.dist[LOCATION_CODE_LABEL].values, self.dep[LOCATION_CODE_LABEL].values

    def get_all_location_codes(self):
        return np.concatenate([self.dist[LOCATION_CODE_LABEL].values,
                               self.dep[LOCATION_CODE_LABEL].values,
                               [self.supplier]])

    def get_supplier_distances(self):
        n = self.get_size()
        location_codes = self.get_all_location_codes()
        return np.matrix([self.dataset.get_distance(self.supplier, x) for x in location_codes]).reshape(1, n)

    def get_destination_distances(self):
        location_codes = self.get_all_location_codes()
        return np.matrix([[self.dataset.get_distance(x, y) for x in location_codes] for y in location_codes])
