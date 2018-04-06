import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np


  
  # para variaveis: 
    #obj, lb, ub, names
  #para linear_constrainsts
    #lin_expr, senses, rhs, names
#        >>> import cplex
#        >>> c = cplex.Cplex()
 #       >>> indices = c.linear_constraints.add(names = ["c0", "c1", "c2", "c3"])
  #      >>> c.linear_constraints.get_rhs()
   #     [0.0, 0.0, 0.0, 0.0]
    #    >>> c.linear_constraints.set_rhs("c1", 1.0)
     #   >>> c.linear_constraints.get_rhs()
      #  [0.0, 1.0, 0.0, 0.0]
      #  >>> c.linear_constraints.set_rhs([("c3", 2.0), (2, -1.0)])
       # >>> c.linear_constraints.get_rhs()
       # [0.0, 1.0, -1.0, 2.0]
       # """
       
    #prob.linear_constraints.add(lin_expr = constraints, senses = constraints_senses, rhs = m_rhs,  names = m_rownames)
    #prob.objective.set_sense(prob.objective.sense.minimize)
    #prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)
    #for i in range(len(D)):
      #constraints.append(["x1", "x2"], [])
      #print("teste")

#m_obj = [-2.0, -1.0]
#m_ub = [cplex.infinity, cplex.infinity]
#m_lb = [0, 0]
#m_colnames = ["x1", "x2"]
#m_rhs = [4.0, 3.0, 3.5]
#m_rownames = ["r1", "r2", "r3"] 
#m_sense = "LL"
#prob.objective.set_sense(prob.objective.sense.minimize)
#prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)

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



class PrimalGilmoreGomory:

  def restricoes(self, prob, m_colnames, m_rhs, A, constraints):
    m_rownames = ["demanda1", "demanda2", "demanda3", "demanda4"]
    m_senses = ["G", "G", "G", "G"]
    for i in range(len(m_rhs)):
      constraints[i][0] = m_colnames #first_constraint = [["x1", "x2"], [1, 1.0]]
      constraints[i][1] = A[i]
    #print(m_rhs)
    #print(m_colnames)
    #print(constraints)
    prob.linear_constraints.add(lin_expr = constraints, senses = m_senses, rhs = m_rhs, names = m_rownames)


  def padroesiniciais(self, m_colnames, m_obj, L, l, A):
    N = 0
    constraints = []
    #aux = ""
    for j in range(len(l)):
      if j != N:
        A[j][N] = 0
      else: 
        A[j][N] = np.floor(L/l[j])
      #aux +=
      #constraints.append([""])  
      N += 1
      m_colnames[j] = str("x" + str(j))
      m_obj[j] = 1
   

  def __init__(self, prob):
    print("inicio")

  def addvariables(self, prob):
    prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)

  


class DualGilmoreGomory:
  
  def addvariables(self, prob, m_obj, m_lb, ub, names):
    prob.variables.add(obj = m_obj, lb = m_lb, ub = D, names = m_colnames)

  def __init__(self, prob):
    print("iniciomochila")

  def mochilainicio(self, m_colnames, l):
    for j in range(len(l)):
      m_colnames[j] = str("a"+ str(j))


  def restricoes(self, prob, m_colnames, m_rhs, l, constraints):
    m_rownames = ["existencia1", "existencia2", "existencia3", "existencia4"]
    m_senses = ["L", "L", "L", "L"]
    for i in range(len(M)):
      constraints[i][0] = m_colnames #first_constraint = [["x1", "x2"], [1, 1.0]]
      constraints[i][1] = l
    prob.linear_constraints.add(lin_expr = constraints, senses = m_senses, rhs = m_rhs, names = m_rownames)
  

print('testing')
A = [[0 for x in range(4)] for y in range(4)]
constraints = [[[0 for x in range(4)] for y in range(2)] for w in range(4)]
m_colnames = ["0", "0", "0", "0"]
m_obj = [0, 0, 0, 0]
m_rhs = [0, 0, 0, 0]
m_ub = [cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity]
m_lb = [0, 0, 0, 0]
L = 100
l = [50, 40, 30, 15]
D = [50, 50, 100, 100]
corte = cplex.Cplex()
mochila = cplex.Cplex()
gg = PrimalGilmoreGomory(corte)
mo = DualGilmoreGomory(mochila)
gg.padroesiniciais(m_colnames, m_obj, L, l, A)
gg.addvariables(corte)
gg.restricoes(corte, m_colnames, D, A, constraints)
corte.objective.set_sense(corte.objective.sense.minimize)
print(corte.solve())
print(corte.solution.get_values())
M = corte.solution.get_dual_values()
constraints = [[[0 for x in range(4)] for y in range(2)] for w in range(4)]
mo.mochilainicio(m_colnames, l)
for i in range(len(M)):
  m_rhs[i] = L
mo.addvariables(mochila, M, m_lb, D, m_colnames)
mo.restricoes(mochila, m_colnames, m_rhs, l, constraints)
mochila.objective.set_sense(mochila.objective.sense.maximize)
print(mochila.solve())
print(mochila.solution.get_values())





