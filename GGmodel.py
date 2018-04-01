import cplex
from cplex.exceptions import CplexError
import sys
import numpy


def getdates(prob):
  L = [100]
  l = [50, 40, 30, 15]
  D = [50, 50, 100, 100]
  m_ub = [cplex.infinity, cplex.infinity]
  m_lb = [0, 0]
  m_obj = [1]
  m_colnames = ["x1"]
  m_rhs = D
  m_rownames = ["demanda1", "demanda2", "demanda3", "demanda4"]

  prob.objective.set_sense(prob.objective.sense.minimize)
  prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)
  for i in range(len(D)):
    constraints.append(["x1", "x2"], [])


def method(prob):
  N = 0
  for i in range(len(L)): 
    for j in range(len(l)):
      if i != j:
        A[i, j, N] = 0
      else: 
        A[i, j, N] = numpy.floor(L[i]/l[m])
  N += 1
  
  prob.linear_constraints.add()

def init(prob):
  getdates(prob)

print('testing')

corte = cplex.Cplex()
mochila = cplex.Cplex()


#m_obj = [-2.0, -1.0]
#m_ub = [cplex.infinity, cplex.infinity]
#m_lb = [0, 0]
#m_colnames = ["x1", "x2"]
#m_rhs = [4.0, 3.0, 3.5]
#m_rownames = ["r1", "r2", "r3"] 
#m_sense = "LL"
#prob.objective.set_sense(prob.objective.sense.minimize)
#prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)
#first_constraint = [["x1", "x2"], [1, 1.0]]
#second_constraint = [["x1", "x2"], [1.0, 0]]
#third_constraint = [["x1", "x2"], [0, 1.0]]
#constraints = [first_constraint, second_constraint, third_constraint]
#constraints_senses = ["L", "L", "L"]
#prob.linear_constraints.add(lin_expr = constraints, senses = constraints_senses, rhs = m_rhs,  names = m_rownames)
#print(prob.linear_constraints.get_rhs())
#print(prob.linear_constraints.get_senses())
#print(prob.objective.get_sense())
#print(prob.variables.get_names())
#print(prob.solve())
#print(prob.solution.get_reduced_costs())
#for x in m_rhs:
 # print("teste")

#for i in range(len(m_colnames)):
#  m_rownames += "Demanda" + str(i)

#print(m_rownames)  


