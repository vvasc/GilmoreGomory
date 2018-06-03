import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np



class PrimalGG:

  def restricoes(self, prob, m_colnames, m_rhs, A, constraints, N, m_rownames, m_senses, m_obj, m_ub, m_lb):
    for i in range(len(m_rhs)+1):
      if (i==len(m_rhs)):
        m_rownames[i] = "estoque"
        m_senses[i] = "E"
      else:
        m_rownames[i] = str("demanda" + str(i+1))
        m_senses[i] = "E"
    for i in range(N[0]):
      m_obj.append(1)
      m_ub.append(cplex.infinity)
      m_lb.append(0)
      m_colnames.append(str("x" + str(i))) 
    for i in range(len(m_rhs)+1):
      if (i==len(m_rhs)):
        constraints[i][0] = m_colnames
        constraints[i][1] = m_obj
      else:
        constraints[i][0] = m_colnames #first_constraint = [["x1", "x2"], [1, 1.0]]
      #print(A[i])
        constraints[i][1] = A[i]
    #print(m_colnames)
    #print(constraints)
  
  def restricaoestoque(self, m_rownames, m_senses, estoque, m_colnames, m_obj):
    estoque[0] = m_colnames
    estoque.append(m_obj)
    m_senses.append("L")
    m_rownames.append("Estoque")
 


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
    #print(m_obj)
    #print(m_lb)
    #print(m_ub)
    #print(m_colnames)
    prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)

  def addconstraints(self, prob, constraints, m_senses, D, ek, m_rownames):
    m_rhs = []
    for i in range(len(D)):
      m_rhs.append(D[i])
    m_rhs.append(ek[0])
    prob.linear_constraints.add(lin_expr = constraints, senses = m_senses, rhs = m_rhs, names = m_rownames)