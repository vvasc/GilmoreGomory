import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
from Primal import PrimalGG
from Sub import SubGG
import matplotlib.pyplot as plt
import matplotlib as mpl
from GGmodel import GGmodel as GG
import pytest as ptest

prob = GG([4, 3, 2], [10, 5, 3], 9, [10], "teste1.txt") 

