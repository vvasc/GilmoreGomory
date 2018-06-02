# coding=utf-8
import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
from Primal import PrimalGG
from Sub import SubGG

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
  L = 0 
  l = [] 
  D = [] 
  ek = []
  A = [[0 for x in range(len(l))] for y in range(len(l))] 
  constraints = [[[0 for x in range(len(l)+1)] for y in range(2)] for w in range(len(l)+1)] 
  estoque = [[[0 for x in range(len(l))] for y in range(2)]]
  m_rownames = ["" for x in range(len(D)+1)]
  m_senses = ["" for x in range(len(D)+1)]
  custred = [0, 0, 0, 0]
  inicio = True
  
  corte = cplex.Cplex()
  mochila = cplex.Cplex()


  gg = PrimalGG()
  mo = SubGG()

    
  def method(self, reseau):
    self.gg.padroesiniciais(self.m_colnames, self.L, self.l, self.A, self.N)
    while(self.STOP | self.inicio):
      self.IT+=1
      self.gg.restricoes(self.corte, self.m_colnames, self.D, self.A, self.constraints, self.N, self.m_rownames, self.m_senses, self.m_obj, self.m_ub, self.m_lb)
      self.gg.addvariables(self.corte, self.m_obj, self.m_lb, self.m_ub, self.m_colnames)
      self.gg.addconstraints(self.corte, self.constraints, self.m_senses, self.D, self.ek, self.m_rownames)
      self.corte.objective.set_sense(self.corte.objective.sense.minimize)
      try:
        self.corte.solve()
      except IOError:
        self.corte.solve()
      reseau.write('Solution: ' + str(self.corte.solution.get_values()) + '\n')
      self.M = self.corte.solution.get_dual_values()
      self.M.pop()
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
      try:
        self.mochila.solve()
      except IOError:
        self.mochila.solve()
      self.a = self.mochila.solution.get_values()
      self.f = self.mochila.solution.get_objective_value()
      if (1 - self.f >= 0):
        self.STOP = False
      reseau.write('Padrão novo: ' + str(self.a) + '\n')
      self.N[0] += 1
      self.A = np.transpose(self.A)
      self.A = np.vstack([self.A, self.a])
      self.A = np.transpose(self.A)
      self.custred = self.corte.solution.get_reduced_costs()
      self.m_colnames = []
      self.m_obj = []
      self.m_ub = []
      self.m_lb = []
      self.m_rhs = []
      self.a = []
      reseau.write('Função Objetivo: ' + str(self.corte.solution.get_objective_value()) + '\n')
      self.corte = cplex.Cplex()
      self.mochila = cplex.Cplex()
      self.constraints = [[[0 for x in range(self.N[0]+1)] for y in range(2)] for w in range(len(self.l)+1)]
      self.estoque = [[0 for x in range(self.N[0])] for y in range(2)]
      self.inicio = False


  def __init__(self, l, D, L, ek, name):
    reseau = 0
    self.l = l
    self.D = D
    self.L = L
    self.ek = ek
    self.A = [[0 for x in range(len(l))] for y in range(len(l))] 
    self.constraints = [[[0 for x in range(len(l)+1)] for y in range(2)] for w in range(len(l)+1)] 
    self.estoque = [[[0 for x in range(len(l))] for y in range(2)]]
    self.m_rownames = ["" for x in range(len(D)+1)]
    self.m_senses = ["" for x in range(len(D)+1)]
    reseau = open(name, 'w', 0)
    self.method(reseau)
    reseau.close()

    


      







