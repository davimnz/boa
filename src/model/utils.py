import numpy as np
import cvxopt
import qpsolvers
import time

# converter modelo (Mx-n)^2 para 1/2 x.T P x + q.T x
def get_pq(M, n):
    P = np.dot(M.T, M)
    q =  -np.dot(M.T, n)
    if type(q) == np.ndarray:
        return P, q
    return P, q.A1

# wrapper do cvxopt
def cvxopt_solve_qp(P, q, G=None, h=None, A=None, b=None):
    P = .5 * (P + P.T)  # make sure P is symmetric
    args = [cvxopt.matrix(P), cvxopt.matrix(q)]
    if G is not None:
        args.extend([cvxopt.matrix(G), cvxopt.matrix(h)])
        if A is not None:
            args.extend([cvxopt.matrix(A), cvxopt.matrix(b)])
    sol = cvxopt.solvers.qp(*args)
    if 'optimal' not in sol['status']:
        return None
    return np.array(sol['x']).reshape((P.shape[1],))

# wrapper do cvxopt
def cvxopt_solve_lp(c, G, h, A=None, b=None):
    args = [cvxopt.matrix(c), cvxopt.matrix(G), cvxopt.matrix(h)]
    if A is not None:
        args.extend([cvxopt.matrix(A), cvxopt.matrix(b)])
    sol = cvxopt.solvers.lp(*args)
    return np.array(sol['x']).reshape((c.shape[0],))

class QPSolver:
    def __init__(self, preferred_solver):
        self.preferred_solves_count = 0
        self.fallback_solves_count = 0
        self.times = []
        self.preferred_solver = preferred_solver

    def solve_qp(self, P, q, G=None, h=None, A=None, b=None):
        P0 = P
        # tenta com quadprog
        x, elapsed_time = self.solve_qp_with(P, q, G, h, A, b, solver=self.preferred_solver)
        if x is not None:
            self.preferred_solves_count += 1
            self.times.append(elapsed_time)
            return x  
        # evita erro usando + epsilon I
        eps = 1e-6
        P = 0.5*(P + P.T) + np.identity(P.shape[0]) * eps
        x, elapsed_time = self.solve_qp_with(P, q, G, h, A, b, solver=self.preferred_solver)
        if x is not None:
            self.preferred_solves_count += 1
            self.times.append(elapsed_time)
            return x 
        # fallback para o cvxopt
        start = time.perf_counter()
        x, elapsed_time = self.solve_qp_with(P0, q, G, h, A, b, solver='cvxopt')
        if x is not None:
            self.times.append(elapsed_time)
            self.fallback_solves_count += 1
            return x
        raise Exception('Could not solve')
            

    def solve_qp_with(self, P, q, G=None, h=None, A=None, b=None, solver='quadprog'):
        start, end = 0, 0
        try:
            start = time.perf_counter()
            x = qpsolvers.solve_qp(P, q, G, h, A, b, solver=solver)
            end = time.perf_counter()
        except:
            x = None
        elapsed_time = end - start
        return x, elapsed_time
    
    def get_times(self):
        return np.array(self.times)


def print_vector(x):
    with np.printoptions(precision=4, suppress=True, linewidth=100):
        print(x)