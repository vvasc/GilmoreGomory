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
  f = []
  a = [0]
  N = [] 
  m_colnames = []
  m_obj = [] 
  m_rhs = []
  m_ub = []
  m_lb = []
  L = 0 
  l = [] 
  D = [] 
  ek = []
  A = []
  constraints = []
  estoque = []
  m_rownames = []
  m_senses = []
  custred = []
  inicio = True
  
  corte = cplex.Cplex()
  mochila = cplex.Cplex()

  gg = PrimalGG()
  mo = SubGG()

  def mochilaAttribute(self):
    self.constraints = [[[0 for x in range(len(self.l))] for y in range(2)] for w in range(1)]

  def corteAttribute(self):
    self.constraints = [[[0] for y in range(2)] for w in range(len(self.D)+len(self.L))]
    self.estoque = [[[0 for x in range(len(self.l))] for y in range(2)]]
    self.m_rownames = ["" for x in range(len(self.D)+len(self.L))]
    self.m_colnames = [["" for x in range(len(self.l))] for y in range(len(self.L))]
    self.m_senses = ["" for x in range(len(self.D)+len(self.L))]
    self.m_obj  = [[0 for x in range(self.N[y])] for y in range(len(self.L))]
    self.m_ub = [[0 for x in range(self.N[y])] for y in range(len(self.L))]
    self.m_lb = [[0 for x in range(self.N[y])] for y in range(len(self.L))]

  def initAttribute(self):
    self.A = [[[0 for x in range(len(self.l))] for y in range(len(self.l))] for z in range(len(self.L))]
    self.N = [0 for x in range(len(self.L))]

  def initCorteAttribute(self):
    self.constraints = [[[0 for x in range(len(self.l)*2)] for y in range(2)] for w in range(len(self.L)+len(self.D))] 
    self.m_obj  = [[0 for x in range(len(self.l))] for y in range(len(self.L))]

  attributeSwitcher = {
    'mochila': mochilaAttribute,
    'corte': corteAttribute,
    'init': initAttribute,
    'initCorte': initCorteAttribute
  }

  def removeDualValuesFromEstoque(self, M):
    for i in range(len(self.ek)):
      M.pop()
  
  def setAllValuesNull(self):
    self.m_colnames = []
    self.m_obj = []
    self.m_ub = []
    self.m_lb = []
    self.constraints = []
    self.m_rhs = []
    self.a = []

  def setCorte(self):
    self.gg.restricoes(self.corte, self.m_colnames, self.D, self.A, self.constraints, self.N, self.m_rownames, self.m_senses, self.m_obj, self.m_ub, self.m_lb, self.L)
    self.gg.addvariables(self.corte, self.m_obj, self.m_lb, self.m_ub, self.m_colnames)
    self.gg.addconstraints(self.corte, self.constraints, self.m_senses, self.D, self.ek, self.m_rownames)
    self.corte.objective.set_sense(self.corte.objective.sense.minimize)

  def setMochila(self, usedL):
    self.mo.mochilainicio(self.m_colnames, self.l, self.m_obj, self.m_lb)
    self.mo.addVariables(self.mochila, self.M, self.l, self.m_lb, self.D, self.m_colnames)
    self.mo.restricoes(self.mochila, self.m_colnames, usedL, self.l, self.constraints, self.M)
    self.mo.addConstraints(self.mochila, self.constraints, self.m_senses, usedL, self.m_rownames)
    self.mochila.objective.set_sense(self.mochila.objective.sense.maximize)
  
  def solveMochila(self):
    try:
      self.mochila.solve()
    except IOError:
      self.mochila.solve()

  def solveCorte(self):
    try:
      self.corte.solve()
    except IOError:
      self.corte.solve()

  def setObjectsNull(self):
    self.corte = cplex.Cplex()
    self.mochila = cplex.Cplex()

  def setMochilaNull(self):
    self.mochila = cplex.Cplex()

  def getMochilaValuesAndTranspose(self):
    self.a = self.mochila.solution.get_values()
    self.f.append(self.mochila.solution.get_objective_value())
    self.N[j] += 1 
    self.A[j] = np.transpose(self.A[j]) 
    self.A[j] = np.vstack([self.A[j], self.a])
    self.A[j] = np.transpose(self.A[j])


  stateSwitcher = {
    'solveMochila': solveMochila
    'solveCorte': solveCorte
    'setObjectsNull': setObjectsNull
    'setMochilaNull': setMochilaNull
    'getMochilaValuesAndTranspose': getMochilaValuesAndTranspose
  }

  def stateChanges(self, argument):
    state = self.stateSwitcher.get(argument, "nothing")
    return state(self)

  def attributeConsts(self, argument):
    attr = self.attributeSwitcher.get(argument, "nothing")
    return attr(self)

  def canStop(self, f):
    for i in range(len(f)):
      if (1 - f[i] < 0):
        self.STOP = True
        return 
    self.STOP = False
    return

  def method(self, reseau):
    self.attributeConsts('corte')
    self.attributeConsts('initCorte')
    self.gg.padroesiniciais(self.m_colnames, self.L, self.l, self.A, self.N)
    while(self.STOP | self.inicio):
      self.IT+=1
      self.stateChanges('setCorte')
      self.stateChanges('solveCorte')
      #reseau.write('Solution: ' + str(self.corte.solution.get_values()) + '\n')
      self.M = self.corte.solution.get_dual_values()
      self.removeDualValuesFromEstoque(self.M)
      self.setAllValuesNull()
      self.attributeConsts('mochila')
      for j in range(len(self.L)):
        self.stateChanges('setMochila')
        self.stateChanges('solveMochila')
        self.stateChanges('getMochilaValuesAndTranspose')
        self.setAllValuesNull()
        self.attributeConsts('mochila')
        self.stateChanges('setMochilaNull')
      self.canStop(self.f)
      #reseau.write('Padrão novo: ' + str(self.a) + '\n')
      self.custred = self.corte.solution.get_reduced_costs()
      self.setAllValuesNull()
      #reseau.write('Função Objetivo: ' + str(self.corte.solution.get_objective_value()) + '\n')
      self.stateChanges('setObjectsNull')
      self.attributeConsts('corte')
      self.inicio = False


  def __init__(self, l, D, L, ek, name):
    reseau = 0
    self.l = l
    self.D = D
    self.L = L
    self.ek = ek
    self.attributeConsts('init')
    #reseau = open(name, 'w', 0)
    self.method(reseau)
    #reseau.close()

    


      







