import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np


class SubGG:
  
  def addvariables(self, prob, M, l, m_lb, D, m_colnames):
    m_obj = []
    for i in range(len(M)):
      m_obj.append(M[i] + l[i])
    #print(m_obj)
    #print(m_lb)
    #print(D)
    #print(m_colnames)
    prob.variables.add(obj = m_obj, lb = m_lb, ub = D, names = m_colnames)

  def __init__(self):
    print("iniciodual")

  def mochilainicio(self, m_colnames, l, m_obj, m_lb):
    for j in range(len(l)):
      m_colnames.append(str("a"+ str(j)))
      m_obj.append(1)
      m_lb.append(0)
    #print(m_colnames)


  def restricoes(self, prob, m_colnames, m_rhs, l, constraints, M):
    m_rownames = ["" for x in range(len(l))]
    m_senses = ["L" for x in range(len(l))]
    for i in range(len(M)):
      m_rownames[i] = str("existencia" + str(i+1))
      constraints[i][0] = m_colnames #first_constraint = [["x1", "x2"], [1, 1.0]]
      constraints[i][1] = l
      prob.variables.set_types([(i, prob.variables.type.integer)])
    #print(m_colnames)
    #print(m_rhs)
    #print(l)
    #print(constraints)
    #print(M)
    prob.linear_constraints.add(lin_expr = constraints, senses = m_senses, rhs = m_rhs, names = m_rownames)
    
  