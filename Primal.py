import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np



class PrimalGG:

  def setNomeRestricoes(self, D, L, m_rownames, m_senses):
    for i in range(len(D)):
      m_rownames[i] = str("demanda" + str(i+1))
      m_senses[i] = "G"
    for j in range(len(D), len(D)+len(L), 1):
      m_rownames[j] = "estoque"
      m_senses[j] = "L"
  
  def setVariaveisDecisao(self, m_obj, m_ub, m_lb, m_colnames, N, L):
    for k in range(len(L)):
      for i in range(N[k]):
        m_obj[k][i] = 1
        m_ub[k][i] = cplex.infinity
        m_lb[k][i] = 0
        m_colnames[k][i] = (str("x" + str(i) + str(k))) 
  
  def setLinearExpressionConstsDemanda(self, D, m_colnames, A, constraints):
    for d in range(len(D)):
      constraints[d][0] = np.append(m_colnames[0], m_colnames[1])
      constraints[d][1] = np.append(A[0][d], A[1][d])
  
  def setLinearExpressionConstsEstoque(self, D, L, m_colnames, constraints, m_obj):
    for e in range(len(D), len(D)+len(L), 1):
      constraints[e][0] = m_colnames[e-len(D)]
      constraints[e][1] = m_obj[e-len(D)]
    
  def restricoes(self, prob, m_colnames, D, A, constraints, N, m_rownames, m_senses, m_obj, m_ub, m_lb, L):
    self.setNomeRestricoes(D, L, m_rownames, m_senses)
    self.setVariaveisDecisao(m_obj, m_ub, m_lb, m_colnames, N, L)
    self.setLinearExpressionConstsDemanda(D, m_colnames, A, constraints)
    self.setLinearExpressionConstsEstoque(D, L, m_colnames, constraints, m_obj)
 
  def padroesiniciais(self, m_colnames, L, l, A, N):
    for k in range(len(L)):
      for j in range(len(l)):
        if j != N[k]:
          A[k][j][N[k]] = 0
        else: 
          A[k][j][N[k]] = np.floor(L[k]/l[j])
        N[k] += 1

  def __init__(self):
    print("inicioprimal")
  #a.flatten('F')

  def flattenVariable(self, obj):
    obj_aux = np.reshape(obj, (1, -1))
    for i in range(len(obj_aux)):
      obj[i] = obj_aux[0:1][i]
    return obj[0]
     
  def addvariables(self, prob, m_obj, m_lb, m_ub, m_colnames):
    m_obj = self.flattenVariable(m_obj)
    m_lb = self.flattenVariable(m_lb)
    m_ub = self.flattenVariable(m_ub)
    m_colnames = self.flattenVariable(m_colnames)
    prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)

  def addconstraints(self, prob, constraints, m_senses, D, ek, m_rownames):
    m_rhs = []
    for i in range(len(D)):
      m_rhs.append(D[i])
    m_rhs.append(ek[0])
    prob.linear_constraints.add(lin_expr = constraints, senses = m_senses, rhs = m_rhs, names = m_rownames)