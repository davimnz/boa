import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')


def max_stock_stats(data):
    supply_sites = data['Supply Site Code'].unique()
    metric = []
    for i in range(len(supply_sites)):
        supply_site = supply_sites[i]
        supply_site_rows = (data['Supply Site Code'] == supply_site)
        supply_site_data = data[supply_site_rows]
        skus = supply_site_data['SKU'].unique()
        for j in range(len(skus)):
            sku_rows = (data['SKU'] == skus[j])
            grid_rows = supply_site_rows & sku_rows
            grid = data[grid_rows]
            balanced_sites = 0
            for row in grid.itertuples():
                closing_stock = row[8]
                max_stock = row[7]
                if max_stock >= closing_stock:
                    balanced_sites = balanced_sites + 1
            new_metric = (balanced_sites / len(grid)) * 100
            metric.append(new_metric)
    plt.hist(metric, bins=20, density=True)
    plt.xlabel('Porcentagem')
    plt.ylabel('Quantidade de grids')
    plt.xlim(0, 100)
    plt.tight_layout()
    plt.savefig('figures/max_stock_stats.png')


if __name__ == '__main__':
    raw_data = pd.read_csv('data/new_data.csv', delimiter=';', decimal=',')
    max_stock_stats(raw_data)
