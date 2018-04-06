import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np


class DualGG:
  
  def addvariables(self, prob, m_obj, m_lb, D, m_colnames):
    prob.variables.add(obj = m_obj, lb = m_lb, ub = D, names = m_colnames)

  def __init__(self, prob):
    print("iniciodual")

  def mochilainicio(self, m_colnames, l):
    for j in range(len(l)):
      m_colnames[j] = str("a"+ str(j))


  def restricoes(self, prob, m_colnames, m_rhs, l, constraints, M):
    m_rownames = ["" for x in range(len(l))]
    m_senses = ["L" for x in range(len(l))]
    for i in range(len(M)):
      m_rownames[i] = str("existencia" + str(i+1))
      constraints[i][0] = m_colnames #first_constraint = [["x1", "x2"], [1, 1.0]]
      constraints[i][1] = l
    prob.linear_constraints.add(lin_expr = constraints, senses = m_senses, rhs = m_rhs, names = m_rownames)
  