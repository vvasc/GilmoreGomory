import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np



class PrimalGG:

  def restricoes(self, prob, m_colnames, m_rhs, A, constraints):
    m_rownames = ["" for x in range(len(m_rhs))]
    m_senses = ["" for x in range(len(m_rhs))]
    for i in range(len(m_rhs)):
      m_rownames[i] = str("demanda" + str(i+1))
      m_senses[i] = "G"
      constraints[i][0] = m_colnames #first_constraint = [["x1", "x2"], [1, 1.0]]
      constraints[i][1] = A[i]
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
    print("inicioprimal")

  def addvariables(self, prob, m_obj, m_lb, m_ub, m_colnames):
    prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)