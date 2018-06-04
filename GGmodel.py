# coding=utf-8
import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
from Primal import PrimalGG
from Sub import SubGG

import copy as copy

class GGmodel:

  STOP = True
  IT = 0
  f = []
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
  ek = [0 for x in range(len(D))]
  A = [[[0 for x in range(len(l))] for y in range(len(l))] for z in range(len(D))] 
  At = A
  constraints = [[[0 for x in range(len(l)+1)] for y in range(2)] for w in range(len(l)+1)] 
  estoque = [[[0 for x in range(len(l))] for y in range(2)]]
  m_rownames = ["" for x in range(len(D)*len(D)+len(D))]
  m_senses = ["" for x in range(len(D)*len(D)+len(D))]
  r = [[0 for x in range(len(l))] for y in range(len(D))]
  r_obj = [0 for x in range(len(l)*len(D))]
  r_name = []
  s_name = [('s' + str(x+1)) for x in range(len(ek))]
  s_obj =[1 for x in range(len(ek))]
  t_colnames = [[[0 for x in range(len(l))] for y in range(len(l))] for z in range(len(D))] 
  custred = [0, 0, 0, 0]
  inicio = True
  Aaux = []
  pi = []

  corte = cplex.Cplex()
  mochila = cplex.Cplex()


  gg = PrimalGG()
  mo = SubGG()

  def solucaootima(self, f):
    for i in range(len(f)):
      if (1-f[i]-self.pi[i]<0):
        return False
    return True

    
  def method(self, reseau):
    self.gg.padroesiniciais(self.m_colnames, self.L, self.l, self.A, self.N, self.D)
    self.Aaux = np.copy(self.A)
    while(self.STOP | self.inicio):
      self.IT+=1
      self.Aaux = np.copy(self.A)
      self.gg.restricoes(self.m_colnames, self.t_colnames, self.D, self.A, self.constraints, self.N, self.m_rownames, self.m_senses, self.m_obj, self.m_ub, self.m_lb, self.r_name, self.r_obj, self.s_name, self.s_obj, self.l, self.L)
      self.gg.addvariables(self.corte, self.m_obj, self.m_lb, self.m_ub, self.m_colnames, self.r_name, self.s_name)
      self.gg.addconstraints(self.corte, self.constraints, self.m_senses, self.D, self.ek, self.m_rownames)
      self.corte.objective.set_sense(self.corte.objective.sense.minimize)
      try:
        self.corte.solve()
      except IOError:
        self.corte.solve()
      sol = self.corte.solution.get_values(self.m_colnames)
      tot = self.corte.solution.get_values()
      sol = sum(sol)
      reseau.write('Solution: ' + str(sol) + '\n')
      self.M = self.corte.solution.get_dual_values()
      for i in range(len(self.s_name)):
        self.pi.append(self.M.pop())
      self.A = list(self.Aaux)
      
      for i in range(len(self.D)):
        self.m_obj = []
        self.constraints = []
        self.m_colnames = []
        self.m_ub = []
        self.m_lb = []
        self.m_rhs = []
        self.constraints = [[[0 for x in range(len(self.l))] for y in range(2)] for w in range(1)]
        self.mo.mochilainicio(self.m_colnames, self.l, self.m_obj, self.m_lb)
        self.mo.addvariables(self.mochila, self.M[0+i*len(self.D[0]): len(self.D[0])+i*len(self.D[0])], self.l, self.m_lb, self.D[i], self.m_colnames)
        self.m_rhs.append(self.L)
        self.mo.restricoes(self.mochila, self.m_colnames, self.m_rhs, self.l, self.constraints, self.M[0+i*len(self.D[0]): len(self.D[0])+i*len(self.D[0])])
        self.mochila.objective.set_sense(self.mochila.objective.sense.maximize)
        try:
          self.mochila.solve()
        except IOError:
          self.mochila.solve()
        self.a = self.mochila.solution.get_values()
        reseau.write('Solution mochila: ' + str(self.mochila.solution.get_objective_value()) + '\n')
        self.f.append(self.mochila.solution.get_objective_value())
        if (self.solucaootima(self.f)): 
          self.STOP = False
        reseau.write('Padrão novo: ' + str(self.a) + '\n')
        self.At = []
        self.At = self.A[i]     
        self.At = np.transpose(self.At)
        self.At = np.vstack([self.At, self.a])
        self.At = np.transpose(self.At)
        self.A[i] = self.At
        self.custred = self.corte.solution.get_reduced_costs()
        self.mochila = cplex.Cplex()  
      
      self.N[0] += 1
      self.m_colnames = []
      self.m_obj = []
      self.m_ub = []
      self.m_lb = []
      self.m_rhs = []
      self.a = []
      self.f = []
      self.r_name = []
      self.pi = []
      reseau.write('Função Objetivo: ' + str(self.corte.solution.get_objective_value()) + '\n')
      self.corte = cplex.Cplex()
      self.constraints = [[[0 for x in range(len(self.D))] for y in range(2)] for w in range(len(self.D)*len(self.D[0]) + len(self.D))] 
      self.t_colnames = [[[0 for x in range(len(self.l))] for y in range(self.N[0])] for z in range(len(self.D))] 
      self.estoque = [[0 for x in range(self.N[0])] for y in range(2)]
      self.inicio = False
      if (self.STOP):
        self.inicio = True


  def __init__(self, l, D, L, ek, name):
    reseau = 0
    self.l = l
    self.D = D
    self.L = L
    self.ek = ek
    self.A = [[[0 for x in range(len(l))] for y in range(len(l))] for z in range(len(D))] 
    self.At = self.A
    self.constraints = [[[0 for x in range(len(l))] for y in range(2)] for w in range(len(D)*len(D[0]) + len(D))] 
    self.estoque = [[[0 for x in range(len(l))] for y in range(2)]]
    self.m_rownames = ["" for x in range(len(D)*len(D[0]) + len(D))]
    self.m_senses = ["" for x in range(len(D)*len(D[0]) +len(D))]
    self.r = [[0 for x in range(len(l))] for y in range(len(D)+1)]
    self.r_obj = [0 for x in range(len(l)*len(D))]
    self.r_name = []
    self.s_name = [('s' + str(x+1)) for x in range(len(ek))]
    self.s_obj =[1 for x in range(len(ek))]
    self.t_colnames = [[[0 for x in range(len(self.l))] for y in range(len(self.l))] for z in range(len(self.D))] 
    reseau = open(name, 'w', 0)
    self.method(reseau)
    reseau.close()

    


      







