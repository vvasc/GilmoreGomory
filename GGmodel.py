import cplex
from cplex.exceptions import CplexError
import sys
import numpy

print('testing')

m_obj = [-2.0, -1.0]
m_ub = [cplex.infinity, cplex.infinity]
m_colnames = ["x1", "x2"]
m_rhs = [4.0, 3.0]
m_rownames = ["cq", "c2"] 
m_sense = "LL"
prob = cplex.Cplex()
prob.objective.set_sense(prob.objective.sense.maximize)
prob.variables.add(obj = m_obj, names = m_colnames, ub = m_ub)
print(prob.variables.get_lower_bounds())


