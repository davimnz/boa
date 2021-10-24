import numpy as np
from utils import print_vector, cvxopt_solve_lp
class Step2Solver:
    def __init__(self, grid, x_opt_dist, x_opt_dep, x_opt_hub):
        self.grid = grid
        self.x_opt = np.hstack([x_opt_dist, x_opt_dep, [x_opt_hub]])

    def solve(self):        
        dist_size, dep_size = self.grid.get_sizes()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()
        available_to_deploy = self.grid.get_available()
        current_stock = np.hstack([current_stock_dist, current_stock_dep, current_stock_hub])
        
        n = dist_size + dep_size + 1
        k = n*n

        supplier_distances = np.random.rand(n)
        destination_distances = np.random.rand(n, n)

        c = np.hstack([supplier_distances, destination_distances.flatten()])
        G = np.zeros(n+k)
        G[:n] = 1.0

        G = np.vstack([G, -np.identity(n+k)])
        h = available_to_deploy
        h = np.hstack([h, np.zeros(n+k)])

        # print_vector(G)

        A_left = np.identity(n)
        A_right = np.zeros((n, k))

        for i in range(n):
            aux = np.zeros((n, n))
            aux[i, :] = -1
            aux[:, i] = 1
            aux[i, i] = 0
            A_right[i, :] = aux.flatten()
        A = np.hstack([A_left, A_right])
        b = self.x_opt - current_stock

        solution = cvxopt_solve_lp(c, G, h, A, b)
        solution[solution < 1] = 0
        print(A.shape)
        print(b.shape)
        print_vector(np.dot(A, solution) - b)
        from_supply = solution[:n]
        exchanges = solution[n:].reshape(n, n)
        return from_supply, exchanges, A, b, solution