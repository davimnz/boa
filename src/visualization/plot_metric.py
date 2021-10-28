from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')


def distance(latitude_1, longitude_1, latitude_2, longitude_2) -> float:
    """
    Evaluates the distance between two points on the Earth surface.
    """
    earth_radius = 6373.0  # unit : km

    latitude_1_rad = radians(latitude_1)
    longitude_1_rad = radians(longitude_1)
    latitude_2_rad = radians(latitude_2)
    longitude_2_rad = radians(longitude_2)

    distance_longitude = longitude_2_rad - longitude_1_rad
    distance_latitude = latitude_2_rad - latitude_1_rad

    a = sin(distance_latitude / 2)**2 + cos(latitude_1_rad) * \
        cos(latitude_2_rad) * sin(distance_longitude / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius*c


def evaluate_distance(distances, origin, destiny, supply_site_code) -> float:
    """
    Evaluates the distance between origin and destiny
    """
    if origin != 'Available' and destiny != 'Available':
        origin_position = distances.loc[distances['code'] == origin]
        origin_position = (origin_position['latitude'],
                           origin_position['longitude'])

        destiny_position = distances.loc[distances['code'] == destiny]
        destiny_position = (destiny_position['latitude'],
                            destiny_position['longitude'])

        return distance(origin_position[0], origin_position[1],
                        destiny_position[0], destiny_position[1])
    elif origin == 'Available' and destiny != supply_site_code:
        origin_position = distances.loc[distances['code'] == supply_site_code]
        origin_position = (origin_position['latitude'],
                           origin_position['longitude'])

        destiny_position = distances.loc[distances['code'] == destiny]
        destiny_position = (destiny_position['latitude'],
                            destiny_position['longitude'])

        return distance(origin_position[0], origin_position[1],
                        destiny_position[0], destiny_position[1])
    elif origin == 'Available' and destiny == supply_site_code:
        return 0


def evaluate_exchange_map_cost(exchanges, distances,
                               supply_site_code, sku_code) -> float:
    """
    Evaluates the cost of a given exchange map.
    """
    exchange_grid = exchanges[exchanges['Supply Site Code']
                              == supply_site_code]
    exchange_grid = exchange_grid[exchange_grid['SKU'] == sku_code]

    cost = 0
    origin_index = exchange_grid.columns.to_list().index('Origin')
    destiny_index = exchange_grid.columns.to_list().index('Destiny')
    amount_index = exchange_grid.columns.to_list().index('Amount')
    for row in exchange_grid.itertuples():
        origin = row[origin_index + 1]
        destiny = row[destiny_index + 1]
        amount = row[amount_index + 1]

        new_cost = amount * evaluate_distance(distances, origin,
                                              destiny, supply_site_code)
        cost = cost + new_cost
    return cost


def plot_exchange_map_comparison(exchanges, distances) -> None:
    exchanges_cost = []

    supply_sites = exchanges['Supply Site Code'].unique()
    for supply_site_code in supply_sites:
        supply_site_df = exchanges[exchanges['Supply Site Code']
                                   == supply_site_code]

        skus = supply_site_df['SKU'].unique()
        for sku_code in skus:
            grid_cost = evaluate_exchange_map_cost(exchanges, distances,
                                                   supply_site_code, sku_code)

            exchanges_cost.append(grid_cost / 1e6)
    return exchanges_cost


def plot_stock_balance(data, data_name, balance=False) -> None:
    """
    Plots two histograms of the percentage of balanced stocks in a grid.
    The balance points are max stock and reorder stock.
    """
    supply_sites = data['Supply Site Code'].unique()
    max_metric = []
    reorder_metric = []
    for i in range(len(supply_sites)):
        supply_site = supply_sites[i]
        supply_site_rows = (data['Supply Site Code'] == supply_site)
        supply_site_data = data[supply_site_rows]
        skus = supply_site_data['SKU'].unique()
        for j in range(len(skus)):
            sku_rows = (data['SKU'] == skus[j])
            grid_rows = supply_site_rows & sku_rows
            grid = data[grid_rows]
            balanced_max = 0
            balanced_reorder = 0
            for row in grid.itertuples():
                if balance:
                    stock_index = data.columns.to_list().index('x_opt')
                else:
                    stock_index = data.columns.to_list().index('Closing Stock')

                max_stock_index = data.columns.to_list().index('MaxDOC (Hl)')
                reorder_stock_index = data.columns.to_list().index('Reorder Point (Hl)')

                current_stock = row[stock_index + 1]
                max_stock = row[max_stock_index + 1]
                reorder_stock = row[reorder_stock_index + 1]
                if max_stock >= current_stock:
                    balanced_max = balanced_max + 1
                if current_stock >= reorder_stock:
                    balanced_reorder = balanced_reorder + 1
            max_percentage = (balanced_max / len(grid)) * 100
            reorder_percentage = (balanced_reorder / len(grid)) * 100
            max_metric.append(max_percentage)
            reorder_metric.append(reorder_percentage)
    plt.hist(max_metric, bins=20)
    plt.title('Estoques balanceados no grid (max)')
    plt.xlabel('Porcentagem')
    plt.ylabel('Quantidade de grids')
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig('figures/' + data_name + '_max_stock.png')
    plt.figure()

    plt.hist(reorder_metric, bins=20)
    plt.title('Estoques balanceados no grid (reorder)')
    plt.xlabel('Porcentagem')
    plt.ylabel('Quantidade de grids')
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig('figures/' + data_name + '_reorder_stock.png')
    plt.figure()


if __name__ == '__main__':
    unbalanced = pd.read_csv('data/data.csv', delimiter=';', decimal=',')
    balanced = pd.read_csv('output/distribution_output_cvxopt.csv',
                           delimiter=';', decimal=',')
    distances = pd.read_csv('data/distance.csv', delimiter=';', decimal=',')
    exchanges = pd.read_csv('output/exchanges_output.csv',
                            delimiter=';', decimal=',')

    plot_stock_balance(unbalanced, 'unbalanced')
    plot_stock_balance(balanced, 'balanced', balance=True)
    plot_exchange_map_comparison(exchanges, distances)
