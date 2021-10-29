import numpy as np
from .utils import get_pq, cvxopt_solve_qp

class DistributionSolver:
    def __init__(self, grid, allow_rebalance):
        self.grid = grid
        self.allow_rebalance = allow_rebalance

    def solve(self):
        pass

    def get_xopt(self):
        return self.x_opt
    
    def set_xopt(self, x_opt_dist, x_opt_dep, x_opt_hub):
        self.x_opt = np.concatenate([x_opt_dist, x_opt_dep, [x_opt_hub]])
        self.x_opt_dist = x_opt_dist
        self.x_opt_dep = x_opt_dep
        self.x_opt_hub = x_opt_hub

    def get_xopt_per_type(self):
        return self.x_opt_dist, self.x_opt_dep, self.x_opt_hub
    
    def add_non_negativity_constraint(self, G, h, k):
        return self.add_all_x_larger_than_constraint(G, h, k, np.zeros(k))
    
    def add_all_x_larger_than_constraint(self, G, h, k, lower_bound):
        G = np.vstack([G, -np.identity(k)])
        h = np.concatenate([h, -lower_bound])
        return G, h
    
    def relative_minimize_in_relation_to(self, y):
        k = y.size
        M = np.identity(k)
        for i in range(k):
            if y[i] > 1e-3:
                M[i, i] = 1 / y[i]
            else:
                M[i, i] = 1000
        n = np.ones(k)
        P, q = get_pq(M, n)
        return P, q
    
    def minimize_in_relation_to(self, y):
        n = y.reshape(-1, 1)
        k = n.shape[0]
        M = np.identity(k)
        P, q = get_pq(M, n)
        return P, q
    
    def add_total_stock_does_not_decrease_constraint(self, G, h, total_current_stock):
        k = G.shape[1]
        G = np.vstack([G, - np.ones(k)])
        h = np.concatenate([h, np.array([- total_current_stock]) ])
        return G, h 
    
    def add_dist_has_at_least_constraint(self, G, h, dist_minimum):
        k = G.shape[1]
        n_dist = dist_minimum.size
        aux = np.zeros((n_dist, k), dtype=np.float64)
        for i in range(n_dist):
            aux[i, i] = -1
        G = np.vstack([G, aux])
        h = np.concatenate([h, - dist_minimum])
        return G, h 
    
    def add_dist_has_at_most_constraint(self, G, h, dist_max):
        k = G.shape[1]
        n_dist = dist_max.size
        aux = np.zeros((n_dist, k), dtype=np.float64)
        for i in range(n_dist):
            aux[i, i] = 1
        G = np.vstack([G, aux])
        h = np.concatenate([h, dist_max])
        return G, h 




class BalanceScenarioFactory:
    def create(grid, scenario, allow_redistribution=True) -> DistributionSolver:
        solvers = [Scenario0DistributionSolver, Scenario1DistributionSolver, Scenario2DistributionSolver,
                    Scenario3DistributionSolver, Scenario4DistributionSolver]
        try:
            return solvers[scenario](grid, allow_redistribution)
        except:
            raise Exception('Scenario does not exist')

class Scenario0DistributionSolver (DistributionSolver):
    def __init__(self, grid, allow_rebalance):
        super().__init__(grid, allow_rebalance)

    def solve(self, qpsolver):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()
        reorder_point_dist, reorder_point_dep, reorder_point_hub = self.grid.get_reorder_point()
        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()

        total_current_stock = current_stock_dist.sum() + current_stock_dep.sum() + current_stock_hub.sum()
        k = 1 + dist_size + dep_size
        # minimizar (Mx - n), onde x = [dists; deps; hub]
        reorder_points = np.concatenate([reorder_point_dist, reorder_point_dep, reorder_point_hub])
        P, q = self.minimize_in_relation_to(reorder_points)

        # Desigualdades Gx <= h
        # primeira inequação: limite de produto disponivel
        G = np.ones((1, k))
        h = np.array(available_to_deploy + total_current_stock)
        # segunda inequação: nada sai do sistema 
        G, h = self.add_total_stock_does_not_decrease_constraint(G, h, total_current_stock)
        # demais inequaçãoes: dist tem no mínimo CS + order
        dist_minimum = orders + current_stock_dist
        G, h = self.add_dist_has_at_least_constraint(G, h, dist_minimum)
        # nao negatividade
        G, h = self.add_non_negativity_constraint(G, h, k)
        # se não tiver rebalance ativado: estoque nunca pode diminuir
        if not self.allow_rebalance:
            G, h = self.add_all_x_larger_than_constraint(G, h, k, current_stock)

        x_opt = qpsolver.solve_qp(P, q, G=G, h=h)
        self.set_xopt(x_opt[:dist_size], x_opt[dist_size:-1], x_opt[-1])

class Scenario1DistributionSolver (DistributionSolver):
    def __init__(self, grid, allow_rebalance):
        super().__init__(grid, allow_rebalance)

    def solve(self, qpsolver):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()

        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()

        k = 1 + dist_size + dep_size
        max_points = np.concatenate([max_dist, max_dep, [0]])
        P, q = self.relative_minimize_in_relation_to(max_points)
        P[-1, -1] = 0    
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

        current_stock = np.concatenate([current_stock_dist, current_stock_dep, current_stock_hub])
        # nao negatividade
        G, h = self.add_non_negativity_constraint(G, h, k)
        if not self.allow_rebalance:
            G, h = self.add_all_x_larger_than_constraint(G, h, k, current_stock)
        
        x_opt = qpsolver.solve_qp(P, q, G=G, h=h, A=A, b=b)
        self.set_xopt(x_opt[:dist_size], x_opt[dist_size:-1], x_opt[-1])


class Scenario2DistributionSolver (DistributionSolver):
    def __init__(self, grid, allow_rebalance):
        super().__init__(grid, allow_rebalance)

    def solve(self, qpsolver):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()
        reorder_point_dist, reorder_point_dep, reorder_point_hub = self.grid.get_reorder_point()
        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()

        k = 1 + dist_size + dep_size
        reorder_points = np.concatenate([reorder_point_dist, reorder_point_dep, reorder_point_hub])
        P, q = self.relative_minimize_in_relation_to(reorder_points)
    
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
        G, h = self.add_non_negativity_constraint(G, h, k)
        if not self.allow_rebalance:
            G, h = self.add_all_x_larger_than_constraint(G, h, k, current_stock)
        
        x_opt = qpsolver.solve_qp(P, q, G=G, h=h)
        self.set_xopt(x_opt[:dist_size], x_opt[dist_size:-1], x_opt[-1])


class Scenario3DistributionSolver (DistributionSolver):
    def __init__(self, grid, allow_rebalance):
        super().__init__(grid, allow_rebalance)

    def solve(self, qpsolver):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()
        reorder_point_dist, reorder_point_dep, reorder_point_hub = self.grid.get_reorder_point()
        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()
        total_current_stock = current_stock_dist.sum() + current_stock_dep.sum() + current_stock_hub.sum()

        k = dist_size + dep_size
        _, _, hub_min = self.grid.get_min_stock()
        hub = hub_min[0]

        # minimizar (Mx - n), onde x = [dists; deps]
        reorder_points_excluding_hub = np.concatenate([reorder_point_dist, reorder_point_dep])
        P, q = self.relative_minimize_in_relation_to(reorder_points_excluding_hub)
        # Gx <= h
        # primeira inequação: limite de produto disponivel
        G = np.ones((1, k))
        h = np.array(available_to_deploy + total_current_stock - hub)
        # segunda inequação: nada sai do sistema 
        G, h = self.add_total_stock_does_not_decrease_constraint(G, h, total_current_stock-hub)
        # demais inequaçãoes: dist tem no máximo CS + order
        dist_maximum = orders + current_stock_dist
        G, h = self.add_dist_has_at_most_constraint(G, h, dist_maximum)
        # nao negatividade
        G, h = self.add_non_negativity_constraint(G, h, k)
        if not self.allow_rebalance:
            G, h = self.add_all_x_larger_than_constraint(G, h, k, current_stock)
        
        x_opt = qpsolver.solve_qp(P, q, G=G, h=h)
        self.set_xopt(x_opt[:dist_size], x_opt[dist_size:], hub)


class Scenario4DistributionSolver (DistributionSolver):
    def __init__(self, grid, allow_rebalance):
        super().__init__(grid, allow_rebalance)

    def solve(self, qpsolver):
        dist_size, dep_size = self.grid.get_sizes()
        max_dist, max_dep, max_hub = self.grid.get_max_stock()
        current_stock_dist, current_stock_dep, current_stock_hub = self.grid.get_current_stock()
        reorder_point_dist, reorder_point_dep, reorder_point_hub = self.grid.get_reorder_point()
        available_to_deploy = self.grid.get_available()
        orders = self.grid.get_orders()

        k = dist_size + dep_size + 1
        # minimizar (Mx - n), onde x = [dists; deps]
        reorder_points = np.concatenate([reorder_point_dist, reorder_point_dep, reorder_point_hub])
        P, q = self.relative_minimize_in_relation_to(reorder_points)
        total_current_stock = current_stock_dist.sum() + current_stock_dep.sum() + current_stock_hub.sum()
        # Gx <= h
        # uma inequação para cada dist + 2 gerais
        G = np.zeros((2+dist_size, k), dtype=np.float64)
        h = np.zeros(2+dist_size)

        # primeira inequação: limite de produto disponivel
        G = np.ones((1, k))
        h = np.array(available_to_deploy + total_current_stock)
        # segunda inequação: nada sai do sistema 
        G, h = self.add_total_stock_does_not_decrease_constraint(G, h, total_current_stock)
        # demais inequaçãoes: dist tem no máximo CS + order
        dist_maximum = orders + current_stock_dist
        G, h = self.add_dist_has_at_most_constraint(G, h, dist_maximum)
        # nao negatividade
        G, h = self.add_non_negativity_constraint(G, h, k)
        if not self.allow_rebalance:
            G, h = self.add_all_x_larger_than_constraint(G, h, k, current_stock)
        
        x_opt = qpsolver.solve_qp(P, q, G=G, h=h)
        self.set_xopt(x_opt[:dist_size], x_opt[dist_size:-1], x_opt[-1])