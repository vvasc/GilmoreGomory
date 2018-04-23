# coding=utf-8
import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
from Primal import PrimalGG
from Sub import SubGG
import matplotlib.pyplot as plt
import matplotlib as mpl
  
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

class GGmodel:

  STOP = True
  IT = 0
  f = 0
  a = [0]
  N = [0] 
  m_colnames = []
  m_obj = [] 
  m_rhs = []
  m_ub = []
  m_lb = []
  L = 100
  l = [50, 40, 30, 15]
  D = [50, 50, 100, 100]
  ek = [300]
  A = [[0 for x in range(len(l))] for y in range(len(l))] 
  constraints = [[[0 for x in range(len(l)+1)] for y in range(2)] for w in range(len(l)+1)] 
  estoque = [[[0 for x in range(len(l))] for y in range(2)]]
  #constraints = [[[],[]],[[],[]]]
  m_rownames = ["" for x in range(len(D)+1)]
  m_senses = ["" for x in range(len(D)+1)]
  custred = [0, 0, 0, 0]
  inicio = True
  
  corte = cplex.Cplex()
  mochila = cplex.Cplex()


  gg = PrimalGG()
  mo = SubGG()

  #def declarations(self):

  """  def checacustosrelativos(self, custred):
    for i in range(len(custred)):
      if (custred[i]<=0):
        return True
      return False"""
    
  def method(self):
    self.gg.padroesiniciais(self.m_colnames, self.L, self.l, self.A, self.N)
    while(self.STOP | self.inicio):
      self.IT+=1
      self.gg.restricoes(self.corte, self.m_colnames, self.D, self.A, self.constraints, self.N, self.m_rownames, self.m_senses, self.m_obj, self.m_ub, self.m_lb)
      self.gg.addvariables(self.corte, self.m_obj, self.m_lb, self.m_ub, self.m_colnames)
      self.gg.addconstraints(self.corte, self.constraints, self.m_senses, self.D, self.ek, self.m_rownames)
      self.corte.objective.set_sense(self.corte.objective.sense.minimize)

        
        
      self.corte.solve()
      print(self.corte.solution.get_values())
      print(self.corte.solution.get_dual_values())

      self.M = self.corte.solution.get_dual_values()
      self.M.pop()


      #print(M)

      self.m_colnames = []
      self.m_obj = []
      self.m_ub = []
      self.m_lb = []
      self.constraints = []
      self.constraints = [[[0 for x in range(len(self.l))] for y in range(2)] for w in range(1)]

      self.mo.mochilainicio(self.m_colnames, self.l, self.m_obj, self.m_lb)
      self.mo.addvariables(self.mochila, self.M, self.l, self.m_lb, self.D, self.m_colnames)
      self.m_rhs.append(self.L)
      self.mo.restricoes(self.mochila, self.m_colnames, self.m_rhs, self.l, self.constraints, self.M)
      self.mochila.objective.set_sense(self.mochila.objective.sense.maximize)
      self.mochila.solve()
      self.a = self.mochila.solution.get_values()
      print(self.mochila.solution.get_objective_value())
      self.f = self.mochila.solution.get_objective_value()
      if (self.L - self.f >= -1):
        self.STOP = False
      print(self.a)
      self.N[0] += 1
      self.A = np.transpose(self.A)
      self.A = np.vstack([self.A, self.a])
      self.A = np.transpose(self.A)
      #print(N)
      self.custred = self.corte.solution.get_reduced_costs()
      #print(A)
      self.m_colnames = []
      self.m_obj = []
      self.m_ub = []
      self.m_lb = []
      self.m_rhs = []
      self.a = []
      self.corte = cplex.Cplex()
      self.mochila = cplex.Cplex()
      self.constraints = [[[0 for x in range(self.N[0]+1)] for y in range(2)] for w in range(len(self.l)+1)]
      self.estoque = [[0 for x in range(self.N[0])] for y in range(2)]
      #print(constraints)
      print(self.IT)
      self.inicio = False


  def __init__(self):
    self.method()
    


      







