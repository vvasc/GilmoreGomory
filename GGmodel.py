import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np

class GilmoreGomory:

  
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


  def getdados(self, prob):
    m_obj = [1]
    m_colnames = ["x1"]
    m_rhs = D
    m_rownames = ["demanda1", "demanda2", "demanda3", "demanda4"]

    #prob.objective.set_sense(prob.objective.sense.minimize)
    #prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)
    for i in range(len(D)):
      #constraints.append(["x1", "x2"], [])
      print("teste")


  def padroesiniciais(self, m_colnames, m_obj):
    N = 0
    L = 100
    l = [50, 40, 30, 15]
    D = [50, 50, 100, 100]
    A = {}
    constraints = []
    #aux = ""
    for j in range(len(l)):
      if j != N:
        A[j, N] = 0
      else: 
        A[j, N] = np.floor(L/l[j])
      #aux +=
      #constraints.append([""])  
      N += 1
      m_colnames[j] = ("x" + str(j))
      m_obj[j] = 1
      
    print(A)
    
   # prob.linear_constraints.add()

  def __init__(self, prob):
    print("inicio")

print('testing')
m_colnames = ["0", "0", "0", "0"]
m_obj = [0, 0, 0, 0]
m_ub = [cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity]
m_lb = [0, 0, 0, 0]
corte = cplex.Cplex()
mochila = cplex.Cplex()
gg = GilmoreGomory(corte)
gg.padroesiniciais(m_colnames, m_obj)


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


