import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np



class PrimalGG:

  def restricoes(self, prob, m_colnames, t_colnames, m_rhs, A, constraints, N, m_rownames, m_senses, m_obj, m_ub, m_lb, r_name, r_obj, s_name, s_obj):
    cont = 0
    Aaux = []
    Aaux2 = []
    t_colnamesaux = []
    for i in range(len(m_rhs)): #Por periodo
      for j in range(len(m_rhs[0])): #por item
        m_rownames[cont] = str("demanda" + str(i+1)+ str(j+1))
        m_senses[cont] = "G"
        cont = cont + 1
        r_obj.append(1)
        r_name.append("r" + str(i+1) + str(j+1))
        m_ub.append(cplex.infinity)
        m_lb.append(0)

    for i in range(len(m_rhs)):    
      m_rownames[cont] = str("estoque" + str(i+1))
      m_senses[cont] = "L"
      cont = cont + 1

    for j in range(len(m_rhs[0])):
      for i in range(N[0]):
        m_obj.append(1)
        m_ub.append(cplex.infinity)
        m_lb.append(0)
        m_colnames.append(str("x" + str(j+1) + str(i+1)))
      for k in range(len(m_rhs)):
        t_colnames[k][j] = m_colnames[0+j*len(m_rhs[0]):len(m_rhs[0])+j*len(m_rhs[0])]

    for j in range(len(m_rhs)):
      Aaux = list(A[j])
      for i in range(len(m_rhs[0])):
        if(j==0):
          Aaux[i].append(-1)
        else:
          Aaux[i].append(1)
          Aaux[i].append(-1)
      for k in range(len(m_rhs[0])):
        if (j==0):
          t_colnames[j][k].append(r_name[0+k+j]) #PRIMEIRO PERIODO
        else:
          t_colnames[j][k].append(r_name[0+k+(j-1)*len(m_rhs[0])])
          t_colnames[j][k].append(r_name[len(m_rhs[0])+k+(j-1)*len(m_rhs[0])])
      Aaux2.append(Aaux)    




    cont = 0;
    for t in range(len(m_rhs)):
      for i in range(N[0]):
        constraints[cont][0] = t_colnames[t][i]
        constraints[cont][1] = A[t][i]
        cont = cont + 1
    for i in range(len(m_rhs)):
      constraints[cont][0] = m_colnames[0+i*len(m_rhs[0]):len(m_rhs[0])+i*len(m_rhs[0])]
      constraints[cont][1] = m_obj[0+i*len(m_rhs[0]):len(m_rhs[0])+i*len(m_rhs[0])]  
      cont = cont + 1
    #print(m_colnames)
    #print(constraints)
  
  def restricaoestoque(self, m_rownames, m_senses, estoque, m_colnames, m_obj):
    estoque[0] = m_colnames
    estoque.append(m_obj)
    m_senses.append("L")
    m_rownames.append("Estoque")
 


  def padroesiniciais(self, m_colnames, L, l, A, N, D):
    for j in range(len(l)):
      if j != N[0]:
        for t in range(len(D)):
          A[t][j][N[0]] = 0
      else: 
        for t in range(len(D)):
          A[t][j][N[0]] = np.floor(L/l[j])
      #aux +=
      #constraints.append([""])  
      N[0] += 1
  def __init__(self):
    print("inicioprimal")

  def addvariables(self, prob, m_obj, m_lb, m_ub, m_colnames, r):
    #print(m_obj)
    #print(m_lb)
    #print(m_ub)
    #print(m_colnames)
    prob.variables.add(obj = m_obj, lb = m_lb, ub = m_ub, names = m_colnames)

  def addconstraints(self, prob, constraints, m_senses, D, ek, m_rownames):
    m_rhs = []
    for i in range(len(D)):
      for j in range(len(D[i])):
        m_rhs.append(D[i][j])
    for e in range(len(D)):
      m_rhs.append(ek[e])
    prob.linear_constraints.add(lin_expr = constraints, senses = m_senses, rhs = m_rhs, names = m_rownames)