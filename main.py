import pandas as pd
import numpy as np

def get_grid(supplier='PL-1505', sku=85023, remove_hub=False):
    if remove_hub:
        grid = grid[grid['Location Code'] != supplier]
    n = len(grid)
    rp = grid['Reorder Point (Hl)'].values.reshape(n, 1)
    k = grid['Closing Stock'].sum()
    from_available = 0
    available = grid['Available to Deploy'].mean()
    if k < grid['Reorder Point (Hl)'].sum():
        from_available = available - k
        k = grid['Reorder Point (Hl)'].sum()
    return grid, n, k, rp, from_available

def scenario1():
    pass

def scenario2():
    pass

def scenario3():
    pass

def scenario4():
    pass

# n = 3
lambdas = [1.0, 10000.0]
grid, n, k, rp, from_available = get_grid()

I = np.identity(n)
C = np.ones((1, n))
A_tilde = np.bmat(
    [
        [np.sqrt(lambdas[0])*I], 
        [np.sqrt(lambdas[1])*C]
    ]
)

# k = 5
# rp = np.ones((n, 1))
y_tilde = np.bmat(
    [
        [np.sqrt(lambdas[0])*rp], 
        [(np.sqrt(lambdas[1])*k).reshape(1, 1)]
    ]
)

w = np.linalg.inv(A_tilde.T@A_tilde)@A_tilde.T@y_tilde