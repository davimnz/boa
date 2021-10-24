from utils import cvxopt_solve_qp
import numpy as np
from utils import get_pq

class Solver:
    def solve(self):
        pass

class SolverAbstractFactory:
    def create(self, scenario) -> Solver:
        pass

class SimpleSolverFactory (SolverAbstractFactory):
    def create(self, scenario) -> Solver:
        pass

class BalanceScenarioFactory (SolverAbstractFactory):
    def create(grid, scenario) -> Solver:
        if scenario == 0:
            return Scenario0Solver(grid)
        elif scenario == 1:
            return Scenario1Solver(grid)
        elif scenario == 2:
            return Scenario2Solver(grid)
        elif scenario == 3:
            return Scenario3Solver(grid)
        elif scenario == 4:
            return Scenario4Solver(grid)
        else:
            raise Exception('Scenario does not exist')

class Scenario0Solver (Solver):
    def __init__(self, grid):
        self.grid = grid

    def solve(self):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()
        reorder_point_dist, reorder_point_dep, reorder_point_hub = self.grid.get_reorder_point()
        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()

        k = 1 + dist_size + dep_size
        # minimizar (Mx - n), onde x = [dists; deps; hub]
        M = np.identity(k)

        n = np.bmat([reorder_point_dist, reorder_point_dep, reorder_point_hub]).reshape(k, 1)
        # Transforma para a forma padrão
        P, q = get_pq(M, n)
    
        total_current_stock = current_stock_dist.sum() + current_stock_dep.sum() + current_stock_hub.sum()
        # Gx <= h
        # uma inequação para cada dist + 2 gerais
        G = np.zeros((2+dist_size, k), dtype=np.float64)
        h = np.zeros(2+dist_size)

        # primeira inequação: limite de produto disponivel
        G[0, :] = np.ones(k)
        h[0] = available_to_deploy + total_current_stock
        # segunda inequação: nada sai do sistema 
        G[1, :] = - np.ones(k)
        h[1] = - total_current_stock
        # demais inequaçãoes: dist tem no mínimo CS + order
        for i in range(dist_size):
            G[2+i, i] = -1.0
        h[2:] = - (orders + current_stock_dist)

        # nao negatividade
        G = np.vstack([G, -np.identity(k)])
        h = np.hstack([h, np.zeros(k)])
        
        x_opt = cvxopt_solve_qp(P, q, G=G, h=h)
        return x_opt[:dist_size], x_opt[dist_size:dep_size], x_opt[-1]

class Scenario1Solver (Solver):
    def __init__(self, grid):
        self.grid = grid

    def solve(self):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()

        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()

        k = 1 + dist_size + dep_size
        # minimizar (Mx - n), onde x = [dists; deps; hub]
        M = np.identity(k)
        M[k-1, k-1] = 0

        n = np.bmat([max_dist, max_dep, [0]]).reshape(k, 1)
        # Transforma para a forma padrão
        P, q = get_pq(M, n)
    
        total_current_stock = current_stock_dist.sum() + current_stock_dep.sum() + current_stock_hub.sum()
        # Ax = b
        # sum(xi) = a + TCS
        A = np.ones((1, k))
        b = available_to_deploy + total_current_stock

        # Gx <= h
        # -sum(dist_i) <= -order_i - current_stock_i
        G = np.zeros((k, k), dtype=np.float64)
        for i in range(dist_size):
            G[i, i] = -1.0
        h = np.zeros(k)
        h[:len(orders)] = - (orders + current_stock_dist)
        # nao negatividade
        G = np.vstack([G, -np.identity(k)])
        h = np.hstack([h, np.zeros(k)])
        
        x_opt = cvxopt_solve_qp(P, q, G=G, h=h, A=A, b=b)
        return x_opt[:dist_size], x_opt[dist_size:dep_size], x_opt[-1]


class Scenario2Solver (Solver):
    def __init__(self, grid):
        self.grid = grid

    def solve(self):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()
        reorder_point_dist, reorder_point_dep, reorder_point_hub = self.grid.get_reorder_point()
        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()

        k = 1 + dist_size + dep_size
        # minimizar (Mx - n), onde x = [dists; deps; hub]
        M = np.identity(k)

        n = np.bmat([reorder_point_dist, reorder_point_dep, reorder_point_hub]).reshape(k, 1)
        # Transforma para a forma padrão
        P, q = get_pq(M, n)
    
        total_current_stock = current_stock_dist.sum() + current_stock_dep.sum() + current_stock_hub.sum()
        # Gx <= h
        # uma inequação para cada dist + 2 gerais
        G = np.zeros((2+dist_size, k), dtype=np.float64)
        h = np.zeros(2+dist_size)

        # primeira inequação: limite de produto disponivel
        G[0, :] = np.ones(k)
        h[0] = available_to_deploy + total_current_stock
        # segunda inequação: nada sai do sistema 
        G[1, :] = - np.ones(k)
        h[1] = - total_current_stock
        # demais inequaçãoes: dist tem no mínimo CS + order
        for i in range(dist_size):
            G[2+i, i] = -1.0
        h[2:] = - (orders + current_stock_dist)
        # nao negatividade
        G = np.vstack([G, -np.identity(k)])
        h = np.hstack([h, np.zeros(k)])
        
        x_opt = cvxopt_solve_qp(P, q, G=G, h=h)
        return x_opt[:dist_size], x_opt[dist_size:dep_size], x_opt[-1]


class Scenario3Solver (Solver):
    def __init__(self, grid):
        self.grid = grid

    def solve(self):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()
        reorder_point_dist, reorder_point_dep, reorder_point_hub = self.grid.get_reorder_point()
        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()

        k = dist_size + dep_size
        _, _, hub = self.grid.get_min_stock()

        # minimizar (Mx - n), onde x = [dists; deps]
        M = np.identity(k)
        n = np.bmat([reorder_point_dist, reorder_point_dep]).reshape(k, 1)
        # Transforma para a forma padrão
        P, q = get_pq(M, n)
    
        total_current_stock = current_stock_dist.sum() + current_stock_dep.sum() + current_stock_hub.sum()
        # Gx <= h
        # uma inequação para cada dist + 2 gerais
        G = np.zeros((2+dist_size, k), dtype=np.float64)
        h = np.zeros(2+dist_size)

        # primeira inequação: limite de produto disponivel
        G[0, :] = np.ones(k)
        h[0] = available_to_deploy + total_current_stock - hub
        # segunda inequação: nada sai do sistema 
        G[1, :] = - np.ones(k)
        h[1] = - total_current_stock + hub
        # demais inequaçãoes: dist tem no máximo CS + order
        for i in range(dist_size):
            G[2+i, i] = -1.0
        h[2:] = (orders + current_stock_dist)
        # nao negatividade
        G = np.vstack([G, -np.identity(k)])
        h = np.hstack([h, np.zeros(k)])
        
        x_opt = cvxopt_solve_qp(P, q, G=G, h=h)
        return x_opt[:dist_size], x_opt[dist_size:dep_size], hub[0]


class Scenario4Solver (Solver):
    def __init__(self, grid):
        self.grid = grid

    def solve(self):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()
        reorder_point_dist, reorder_point_dep, reorder_point_hub = self.grid.get_reorder_point()
        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()

        k = dist_size + dep_size + 1
        # minimizar (Mx - n), onde x = [dists; deps]
        M = np.identity(k)
        for i in range(dist_size):
            if reorder_point_dist[i]>1e-3:
                M[i, i] = 1/reorder_point_dist[i]
            else: 
                M[i, i] = 1000
        for i in range(dep_size):
            if reorder_point_dep[i]>1e-3:
                M[dist_size + i, dist_size + i] = 1/reorder_point_dep[i]
            else: 
                M[dist_size + i, dist_size + i] = 1000
        n = np.ones(k)
        # Transforma para a forma padrão
        P, q = get_pq(M, n)
    
        total_current_stock = current_stock_dist.sum() + current_stock_dep.sum() + current_stock_hub.sum()
        # Gx <= h
        # uma inequação para cada dist + 2 gerais
        G = np.zeros((2+dist_size, k), dtype=np.float64)
        h = np.zeros(2+dist_size)

        # primeira inequação: limite de produto disponivel
        G[0, :] = np.ones(k)
        h[0] = available_to_deploy + total_current_stock 
        # segunda inequação: nada sai do sistema 
        G[1, :] = - np.ones(k)
        h[1] = - total_current_stock 
        # demais inequaçãoes: dist tem no máximo CS + order
        for i in range(dist_size):
            G[2+i, i] = -1.0
        h[2:] = (orders + current_stock_dist)
        # nao negatividade
        G = np.vstack([G, -np.identity(k)])
        h = np.hstack([h, np.zeros(k)])
        
        x_opt = cvxopt_solve_qp(P, q, G=G, h=h)
        return x_opt[:dist_size], x_opt[dist_size:dep_size], x_opt[-1]