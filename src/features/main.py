import pandas as pd
import numpy as np


def generate_uniform_position(min_value, max_value):
    """
    Generates two dimensional positions for locations in the same grid.
    """
    raw_data = pd.read_csv('data/data.csv', delimiter=';', decimal=',')
    positions_x = []
    positions_y = []
    for row in raw_data.itertuples(index=False):
        if row[0] == row[2]:
            position_x = 0.0
            position_y = 0.0
        else:
            position_x = np.random.uniform(min_value, max_value)
            position_y = np.random.uniform(min_value, max_value)
        positions_x.append(position_x)
        positions_y.append(position_y)
    raw_data['position_x'] = positions_x
    raw_data['position_y'] = positions_y
    raw_data.to_csv('data/new_data.csv', sep=';', decimal=',', index=False)


if __name__ == "__main__":
    generate_uniform_position(0.0, 1000.0)
