import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
from Primal import PrimalGG
from Dual import DualGG

  
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




def checacustosrelativos(custred):
  for i in range(len(custred)):
    if (custred[i]<=0):
      return True
    return False


a =[0]
N = [0] 
m_colnames = []
m_obj = [] 
m_rhs = [0, 0, 0, 0]
m_ub = [cplex.infinity, cplex.infinity, cplex.infinity, cplex.infinity]
m_lb = [0, 0, 0, 0]
L = 100
l = [50, 40, 30, 15]
D = [50, 50, 100, 100]
A = [[0 for x in range(len(l))] for y in range(len(l))] 
constraints = [[[0 for x in range(len(l))] for y in range(2)] for w in range(len(l))] 
#constraints = [[[],[]],[[],[]]]
m_rownames = ["" for x in range(len(m_rhs))]
m_senses = ["" for x in range(len(m_rhs))]
custred = [0, 0, 0, 0]
inicio = True


corte = cplex.Cplex()
mochila = cplex.Cplex()


gg = PrimalGG()
mo = DualGG()


gg.padroesiniciais(m_colnames, L, l, A, N)

while(checacustosrelativos(custred) | inicio):
  inicio = False
  gg.restricoes(corte, m_colnames, D, A, constraints, N, m_rownames, m_senses, m_obj)
  gg.addvariables(corte, m_obj, m_lb, m_ub, m_colnames)
  gg.addconstraints(corte, constraints, m_senses, D, m_rownames)
  corte.objective.set_sense(corte.objective.sense.minimize)

    
    
  corte.solve()
  print(corte.solution.get_values())


  M = corte.solution.get_dual_values()
  print(M)

  m_colnames = []
  m_obj = []

  mo.mochilainicio(m_colnames, l, m_obj)
  for i in range(len(M)):
    m_rhs[i] = L

  mo.addvariables(mochila, M, m_lb, D, m_colnames)
  mo.restricoes(mochila, m_colnames, m_rhs, l, constraints, M)
  mochila.objective.set_sense(mochila.objective.sense.maximize)
  mochila.variables.set_types([(0, mochila.variables.type.integer),(1, mochila.variables.type.integer), (2, mochila.variables.type.integer), (3, mochila.variables.type.integer)])
  print(mochila.solve())
  a = mochila.solution.get_values()
  N[0] += 1
  A.append(a)
  print(N)
  custred = corte.solution.get_reduced_costs()
  print(A)
  m_colnames = []
  constraints = [[[0 for x in range(N[0])] for y in range(2)] for w in range(N[0])]
  








