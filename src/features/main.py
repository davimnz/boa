import pandas as pd
import numpy as np


def clear_inf(raw_data):
    """
    Deletes rows with inf values
    """
    raw_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    raw_data.dropna(inplace=True)


def generate_positions(raw_data,
                       max_latitude=51.3494, min_latitude=49.5677,
                       max_longitude=5.8641, min_longitude=2.6622):
    """
    Generates latitude and longitude for supply sites and locations.

    max latitude (Belgium): 51.3494
    min latitude (Belgium): 49.5677
    max longitude (Belgium: 5.8641
    min longitude (Belgium): 2.6622
    """
    num_rows = raw_data.shape[0]
    latitude = np.random.uniform(min_latitude, max_latitude, num_rows)
    longitude = np.random.uniform(min_longitude, max_longitude, num_rows)
    raw_data['latitude'] = latitude
    raw_data['longitude'] = longitude
    raw_data.to_csv('data/new_data.csv', sep=';', decimal=',', index=False)


if __name__ == "__main__":
    raw_data = pd.read_csv('data/data.csv', delimiter=';', decimal=',')
    clear_inf(raw_data)
    generate_positions(raw_data)
