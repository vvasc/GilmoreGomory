import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np



class PrimalGG:

  def restricoes(self, prob, m_colnames, m_rhs, A, constraints, N, m_rownames, m_senses, m_obj):
    for i in range(len(m_rhs)):
      m_rownames[i] = str("demanda" + str(i+1))
      m_senses[i] = "G"
    for i in range(len(m_rhs)):
      m_obj.append(1)
      m_colnames.append(str("x" + str(i))) 
    for i in range(N[0]):
      constraints[i][0] = m_colnames #first_constraint = [["x1", "x2"], [1, 1.0]]
      constraints[i][1] = A[i]
    print(m_colnames)
    print(constraints)

  def padroesiniciais(self, m_colnames, L, l, A, N):
    for j in range(len(l)):
      if j != N[0]:
        A[j][N[0]] = 0
      else: 
        A[j][N[0]] = np.floor(L/l[j])
      #aux +=
      #constraints.append([""])  
      N[0] += 1
  def __init__(self):
    print("inicioprimal")

  def addvariables(self, prob, m_obj, m_lb, m_ub, m_colnames):
    prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)

  def addconstraints(self, prob, constraints, m_senses, m_rhs, m_rownames):
    prob.linear_constraints.add(lin_expr = constraints, senses = m_senses, rhs = m_rhs, names = m_rownames)