import pandas as pd
import numpy as np


def clear_inf(raw_data) -> None:
    """
    Deletes rows with inf values
    """
    raw_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    raw_data.dropna(inplace=True)
    raw_data.to_csv('data/data.csv', sep=';', decimal=',', index=False)


def generate_positions(raw_data,
                       max_latitude=51.3494, min_latitude=49.5677,
                       max_longitude=5.8641, min_longitude=2.6622) -> None:
    """
    Generates latitude and longitude for supply sites and locations.

    max latitude (Belgium): 51.3494
    min latitude (Belgium): 49.5677
    max longitude (Belgium: 5.8641
    min longitude (Belgium): 2.6622
    """
    distances = pd.DataFrame()
    supply_sites = raw_data['Supply Site Code'].unique()
    locations = raw_data['Location Code'].unique()
    codes = np.unique(np.concatenate((supply_sites, locations), 0))

    np.random.seed(16)  # reproducibility
    latitude = np.random.uniform(min_latitude, max_latitude, len(codes))
    longitude = np.random.uniform(min_longitude, max_longitude, len(codes))
    distances['code'] = codes
    distances['latitude'] = latitude
    distances['longitude'] = longitude
    distances.to_csv('data/geopositioning.csv',
                     sep=';', decimal=',', index=False)


if __name__ == "__main__":
    raw_data = pd.read_csv('data/raw_data.csv', delimiter=';', decimal=',')
    clear_inf(raw_data)
    generate_positions(raw_data)
