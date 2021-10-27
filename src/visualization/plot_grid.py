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


def plot_exchange_map(data, exchange, position,
                      supply_site_code, sku_code) -> None:
    """
    Plots the optimal exchange map for a given grid.
    """
    exchange_table = exchange[(
        exchange['Supply Site Code'] == supply_site_code)]
    exchange_table = exchange_table[(exchange_table['SKU'] == sku_code)]

    grid_table = data[(data['Supply Site Code'] == supply_site_code)]
    grid_table = grid_table[(grid_table['SKU'] == sku_code)]

    labels = {'Hub': 'Hub'}
    colors = {}
    color_dict = {"DEP": "#3f60e1", "DIST": "#60e13f", "HUB": "#e13f60"}

    for row in grid_table.itertuples():
        location_code = row[3]
        type = row[4]

        if location_code == supply_site_code:
            color = color_dict["HUB"]
            colors[location_code] = color
        else:
            color = color_dict[type]
            colors[location_code] = color

        labels[location_code] = location_code

    grid = nx.DiGraph()
    for key, value in labels.items():
        grid.add_node(key, stock=value)

    nodes_with_edges = []
    for row in exchange_table.itertuples():
        origin = row[3]
        destiny = row[4]
        amount = round(row[5])

        if origin == "Available":
            origin = supply_site_code
        if destiny == supply_site_code:
            destiny = 'Hub'
            colors['Hub'] = colors[supply_site_code]

        grid.add_edge(origin, destiny, weight=amount)
        nodes_with_edges.append(origin)
        nodes_with_edges.append(destiny)

    layout = nx.planar_layout(grid)
    layout_label = shift_position(layout, 0.0, 0.02)

    nodes_with_edges = list(set(nodes_with_edges))
    nodes_colors = []
    nodes_labels = {}

    for node in nodes_with_edges:
        nodes_colors.append(colors[node])
        nodes_labels[node] = labels[node]

    nx.draw_networkx(grid, layout, node_color=nodes_colors,
                     nodelist=nodes_with_edges, with_labels=False,
                     arrowsize=20)
    grid_edge_labels = nx.get_edge_attributes(grid, 'weight')
    nx.draw_networkx_edge_labels(grid, layout,
                                 edge_labels=grid_edge_labels)
    nx.draw_networkx_labels(grid, pos=layout_label, labels=nodes_labels)

    dep_legend = mpatches.Patch(color=color_dict["DEP"], label='Depósito')
    dist_legend = mpatches.Patch(color=color_dict["DIST"], label='CDD')
    hub_legend = mpatches.Patch(color=color_dict["HUB"], label="Cervejaria")

    plt.legend(handles=[dep_legend, dist_legend, hub_legend], fontsize=20)
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    unbalanced = pd.read_csv('data/data.csv', delimiter=';', decimal=',')
    position = pd.read_csv('data/distance.csv', delimiter=';', decimal=',')
    exchange = pd.read_csv('output/exchanges_output.csv',
                           delimiter=';', decimal=',')

    # choose which grid to plot. The grid cannot be scenario 0
    supply_site_code = 'PL-1505'
    sku_code = 85023

    # plot_stock_grid(unbalanced, position, supply_site_code, sku_code)
    plot_exchange_map(unbalanced, exchange, position,
                      supply_site_code, sku_code)
