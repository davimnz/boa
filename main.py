from ortools.linear_solver import pywraplp
from data_model import create_data_model

class VariableMatrix:
    def __init__(self):
        self._matrix = {}

    def set(self, i, j, k, value):
        if self._matrix.get(i) is None:
            self._matrix[i] = {}
        if self._matrix.get(i).get(j) is None:
            self._matrix[i][j] = {}
        if self._matrix.get(i).get(j).get(k) is None:
            self._matrix[i][j][k] = {}
        self._matrix[i][j][k] = value
        
    def get(self, i, j, k):
        if self._matrix.get(i) is None or self._matrix.get(i).get(j) is None or self._matrix.get(i).get(j).get(k) is None:
            raise 
        return self._matrix.get(i).get(j).get(k)

def main():
    data = create_data_model()
    solver = pywraplp.Solver.CreateSolver('SCIP')

    infinity = solver.infinity()
    varMatrix = VariableMatrix()
    objective = solver.Objective()
    for i in range(data['num_product']):
        for j in range(data['num_brewery']):
            for k in range(data['num_warehouse']):
                var = solver.IntVar(0, infinity, 'x[%i, %i, %i]' % (i, j, k))
                varMatrix.set(i, j, k, var)
                objective.SetCoefficient(var, data['costs'][i][j][k])
    objective.SetMinimization()


    for i in range(data['num_product']):
        for j in range(data['num_brewery']):
            brewery_capacity_constraint = solver.RowConstraint(0, data['brewery_capacity'][i][j], '')
            for k in range(data['num_warehouse']):
                brewery_capacity_constraint.SetCoefficient(varMatrix.get(i, j, k), 1)


    for i in range(data['num_product']):
        for k in range(data['num_warehouse']):
            target_inventory_constraint = solver.RowConstraint(data['target_inventory'][i][j], data['target_inventory'][i][j], '')
            for j in range(data['num_brewery']):
                brewery_capacity_constraint.SetCoefficient(varMatrix.get(i, j, k), 1)

    print('Number of constraints =', solver.NumConstraints())
    
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        for i in range(data['num_product']):
            for j in range(data['num_brewery']):
                for k in range(data['num_warehouse']):
                    print(varMatrix.get(i, j, k).name(), ' = ', varMatrix.get(i, j, k).solution_value())
        print('Problem solved in %f milliseconds' % solver.wall_time())
        print('Problem solved in %d iterations' % solver.iterations())
        print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    main()
 