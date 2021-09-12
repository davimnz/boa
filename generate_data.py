import pandas as pd
import numpy as np

NUM_WAREHOUSES = 5
NUM_BREWERIES = 3
NUM_PRODUCTS = 2

# Generate costs.
# Each column is a brewery, each line from 0 to NUM_WAREHOUSES is a warehouse.
# From i*NUM_WAREHOUSES to (i+1)*NUM_WAREHOUSES we have product i.
df = pd.DataFrame(np.random.randint(0, 100, size=(NUM_WAREHOUSES*NUM_PRODUCTS, NUM_BREWERIES)))
df.to_csv('dataset/costs.csv', index=False)

# Brewery capacity
df = pd.DataFrame(np.random.randint(0, 500, size=(NUM_PRODUCTS, NUM_BREWERIES)))
df.to_csv('dataset/brewery_capacities.csv', index=False)

# Target inventory
df = pd.DataFrame(np.random.randint(0, 500, size=(NUM_PRODUCTS, NUM_WAREHOUSES)))
df.to_csv('dataset/target_inventory.csv', index=False)