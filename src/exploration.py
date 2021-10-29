from features.fetch import DataSet
dataset = DataSet(data_file='data/raw_data.csv')
grids = dataset.list_grids()

print('Número de grids: ', len(grids), '\n')
print('Valores distintos por coluna:')
print(dataset.data.nunique())
print('\n')

print('Depósitos:')
print(dataset.data[dataset.data['Location Type'] == 'DEP']['Location Code'].nunique())
print('\n')

print('CDDs:')
print(dataset.data[dataset.data['Location Type'] == 'DIST']['Location Code'].nunique())
print('\n')

print('Grids por cenário:')
df = grids.groupby(by=['Scenario']).count()
print(df)
print('\n')
# Anomalies
print('Anomalias de dados')
max_larger_min = dataset.data.query('`MaxDOC (Hl)`<`MinDOC (Hl)`')
print('Anomalia Max < Min:')
print(max_larger_min)

# No Hub
print('Sem Hub:')
no_hub_count = 0
for _, g in grids.iterrows():
    supplier = g['Supply Site Code']
    sku = g['SKU']
    scenario = g['Scenario']

    grid = dataset.select_grid(supplier=supplier, sku=sku)
    if len(grid.hub) == 0:
        print(supplier, sku, scenario)
        no_hub_count += 1
print(no_hub_count, 'sem hub')
