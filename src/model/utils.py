import numpy as np
import cvxopt

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

def print_vector(x):
    with np.printoptions(precision=4, suppress=True, formatter={'float': '{:0.4f}'.format}, linewidth=100):
        print(x)