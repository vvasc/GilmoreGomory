import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np


class SubGG:
  
  def __init__(self):
    print("inicioSub")
  
  def addVariables(self, prob, M, l, m_lb, D, m_colnames):
    m_obj = []
    for i in range(len(M)):
      m_obj.append(M[i])
    prob.variables.add(obj = m_obj, lb = m_lb, ub = D, names = m_colnames)

  def addConstraints(self, prob, constraints, m_senses, m_rhs, m_rownames):
    m_rownames = [""]
    m_senses = ["L"]
    m_rhs = [m_rhs]
    m_rownames = [str("existencia" + str(1))]
    prob.linear_constraints.add(lin_expr = constraints, senses = m_senses, rhs = m_rhs, names = m_rownames)
  
  def setVariablesTypes(self, prob, M):
    for i in range(len(M)):
      prob.variables.set_types([(i, prob.variables.type.integer)])

  def mochilainicio(self, m_colnames, l, m_obj, m_lb):
    for j in range(len(l)):
      m_colnames.append(str("a"+ str(j)))
      m_obj.append(1)
      m_lb.append(0)

  def restricoes(self, prob, m_colnames, m_rhs, l, constraints, M):
    constraints[0][0] = (m_colnames) 
    constraints[0][1] = (l)
    self.setVariablesTypes(prob, M)
    
  