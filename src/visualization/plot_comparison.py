import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

def plot(x):
    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(x, facecolor='blue', bins=15, range=(0, 10))
    ax.set_xticks(bins)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
    bin_centers = 0.5 * np.diff(bins) + bins[:-1]
    for count, x in zip(counts, bin_centers):
        percent = '%0.0f%%' % (100 * float(count) / counts.sum())
        ax.annotate(percent, xy=(x, 0), xycoords=('data', 'axes fraction'),
            xytext=(0, -32), textcoords='offset points', va='top', ha='center')
    plt.subplots_adjust(bottom=0.15)



data = pd.read_csv( 'output/distribution_output_quadprog.csv', delimiter=';', decimal=',')

data_no_redistribution = pd.read_csv( 'output/no_redistribution.csv', delimiter=';', decimal=',')

data = data[abs(data['Reorder Point (Hl)']) > 1]
data_no_redistribution = data_no_redistribution[abs(data_no_redistribution['Reorder Point (Hl)']) > 1]

# data = data[data['Scenario'] != 1]

data['cs_over_ro_before'] = data['Closing Stock']/data['Reorder Point (Hl)']
data['cs_over_ro_after'] = data['x_opt']/data['Reorder Point (Hl)']

data_no_redistribution['cs_over_ro_after'] = data_no_redistribution['x_opt']/data_no_redistribution['Reorder Point (Hl)']

data['cs_over_max_before'] = data['Closing Stock']/data['MaxDOC (Hl)']
data['cs_over_max_after'] = data['x_opt']/data['MaxDOC (Hl)']

print('CS/RP')
print('Before: Mean', data['cs_over_ro_before'].mean(), 'Std', data['cs_over_ro_before'].std())
print('After: Mean', data['cs_over_ro_after'].mean(), 'Std', data['cs_over_ro_after'].std())
print('No redistribution: Mean', data_no_redistribution['cs_over_ro_after'].mean(), 'Std', data_no_redistribution['cs_over_ro_after'].std())

plot(data['cs_over_ro_before'].values)
plt.savefig('figures/distribution_before.png', transparent=True)

plot(data['cs_over_ro_after'].values) 
plt.savefig('figures/distribution_after.png', transparent=True)

plot(data_no_redistribution['cs_over_ro_after'].values) 
plt.savefig('figures/distribution_without_redistribution.png', transparent=True)
plt.show()