import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')


def plot_stock_balance(data, data_name):
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
                closing_stock = row[8]
                max_stock = row[7]
                reorder_stock = row[6]
                if max_stock >= closing_stock:
                    balanced_max = balanced_max + 1
                if closing_stock >= reorder_stock:
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


if __name__ == '__main__':
    unbalanced = pd.read_csv('data/new_data.csv', delimiter=';', decimal=',')
    plot_stock_balance(unbalanced, 'unbalanced')
