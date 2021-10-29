import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv( 'output/distribution_output_quadprog.csv', delimiter=';', decimal=',')

data = data[abs(data['Reorder Point (Hl)']) > 1]
# data = data[data['Scenario'] != 1]

data['cs_over_ro_before'] = data['Closing Stock']/data['Reorder Point (Hl)']
data['cs_over_ro_after'] = data['x_opt']/data['Reorder Point (Hl)']

data['cs_over_max_before'] = data['Closing Stock']/data['MaxDOC (Hl)']
data['cs_over_max_after'] = data['x_opt']/data['MaxDOC (Hl)']

print('CS/RP')
print('Before: Mean', data['cs_over_ro_before'].mean(), 'Std', data['cs_over_ro_before'].std())
print('After: Mean', data['cs_over_ro_after'].mean(), 'Std', data['cs_over_ro_after'].std())

print('CS/Max')
print('Before: Mean', data['cs_over_max_before'].mean(), 'Std', data['cs_over_max_before'].std())
print('After: Mean', data['cs_over_max_after'].mean(), 'Std', data['cs_over_max_after'].std())


data.hist('cs_over_ro_before', range=(0, 15))
data.hist('cs_over_ro_after', range=(0, 15) )

plt.show()