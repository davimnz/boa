import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from math import cos, radians


def shift_position(pos, x_shift, y_shift) -> dict:
    """
    Moves nodes' position by (x_shift, y_shift)
    """
    return {n: (x + x_shift, y + y_shift) for n, (x, y) in pos.items()}


def convert_to_2d(latitude, longitude, center_latitude=50.0):
    """
    Converts (lat, long) to (x, y) using approximation for small areas.
    """
    earth_radius = 6373.0  # unit : km
    aspect_ratio = radians(center_latitude)
    x = earth_radius * longitude * cos(aspect_ratio)
    y = earth_radius * latitude
    return x, y


def plot_stock_grid(data, position, supply_site_code, sku_code) -> None:
    """
    Plots a map containing the amount of stock in each location of a given
    grid: Hub, Depot or Distributor.
    """
    grid_table = data[(data['Supply Site Code'] == supply_site_code)]
    grid_table = grid_table[(grid_table['SKU'] == sku_code)]

    positions = {}
    labels = {}
    colors = []
    color_dict = {"DEP": "#3f60e1", "DIST": "#60e13f", "HUB": "#e13f60"}

    for row in grid_table.itertuples():
        location_code = row[3]
        stock = round(row[8])
        type = row[4]

        if location_code == supply_site_code:
            color = color_dict["HUB"]
            colors.append(color)
        else:
            color = color_dict[type]
            colors.append(color)

        position_row = position[position['code'] == location_code]

        latitude = position_row['latitude']
        longitude = position_row['longitude']
        position_2d = convert_to_2d(latitude, longitude)

        positions[location_code] = position_2d
        labels[location_code] = stock

    positions_nodes = shift_position(positions, 0, 500)

    grid = nx.Graph()
    for key, value in labels.items():
        grid.add_node(key, stock=value)

    nx.draw_networkx(grid, pos=positions, with_labels=False,
                     node_size=350, node_color=colors)
    nx.draw_networkx_labels(grid, pos=positions_nodes,
                            labels=labels, font_size=16)

    ylim = plt.ylim()
    plt.ylim(0.99 * ylim[0], 1.01 * ylim[1])

    dep_legend = mpatches.Patch(color=color_dict["DEP"], label='Depósito')
    dist_legend = mpatches.Patch(color=color_dict["DIST"], label='CDD')
    hub_legend = mpatches.Patch(color=color_dict["HUB"], label="Cervejaria")

    plt.legend(handles=[dep_legend, dist_legend, hub_legend], fontsize=20)
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    unbalanced = pd.read_csv('data/data.csv', delimiter=';', decimal=',')
    position = pd.read_csv('data/distance.csv', delimiter=';', decimal=',')

    # choose which grid to plot
    supply_site_code = 'PL-1505'
    sku_code = 85023

    plot_stock_grid(unbalanced, position, supply_site_code, sku_code)
