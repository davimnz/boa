import pandas as pd
import numpy as np

NUM_WAREHOUSES = 5
NUM_BREWERIES = 3
NUM_PRODUCTS = 2

def create_data_model():
    """Stores the data for the problem."""
    data = {}

    df = pd.read_csv('dataset/costs.csv', dtype=np.float64)
    costs = []
    for i in range(NUM_PRODUCTS):
        costs.append(df.values[i:i+NUM_WAREHOUSES, :].T)
    data['costs'] = costs

    df = pd.read_csv('dataset/brewery_capacities.csv', dtype=np.float64)
    data['brewery_capacity'] = df.values

    df = pd.read_csv('dataset/target_inventory.csv', dtype=np.float64)
    data['target_inventory'] = df.values

    data['num_product'] = NUM_PRODUCTS
    data['num_brewery'] = NUM_BREWERIES
    data['num_warehouse'] = NUM_WAREHOUSES

    return data