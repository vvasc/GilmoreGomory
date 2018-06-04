import cplex
from cplex.exceptions import CplexError
import sys
import numpy as np
from Primal import PrimalGG
from Sub import SubGG
from GGmodel import GGmodel as GG
import time

#Classe 1
#prob = GG([4, 3, 2], [10, 5, 3], 9, [10], "teste1.txt") 
#prob = GG([28, 27, 26, 24, 23, 19, 17, 16, 10, 5], [90, 69, 100, 88, 59, 25, 25, 34, 25, 39], 66, [1000], "exemplo 0")
#prob = GG([20, 13, 12, 10, 9], [6, 1, 4, 1, 8], 71, [54], "exemplo 0")
#prob = GG([23, 17, 16, 14, 13], [9, 5, 3, 1, 10], 93, [189], "exemplo 1")
#prob = GG([13, 12, 11, 10, 8], [9, 9, 5, 5, 8], 73, [116], "exemplo 2")
#prob = GG([12, 10, 8, 6, 5], [9, 6, 3, 10, 1], 69, [48], "exemplo 3")
#prob = GG([29, 17, 14, 13, 12], [2, 2, 1, 7, 8], 97, [188], "exemplo 4")
#prob = GG([30, 14, 13, 12, 10], [7, 8, 7, 8, 10], 96, [163], "exemplo 5")
#prob = GG([16, 15, 12, 11, 10], [2, 4, 2, 10, 8], 95, [152], "exemplo 6")
#prob = GG([30, 15, 10, 9, 8], [5, 3, 10, 5, 9], 76, [108], "exemplo 7")
#prob = GG([26, 16, 8, 6, 5], [1, 8, 6, 5, 6], 57, [179], "exemplo 8")
#prob = GG([15, 14, 13, 11, 8], [8, 2, 3, 2, 5], 85, [76], "exemplo 9")
#Classe 2
#prob = GG([74, 25, 22, 16, 13], [8, 8, 9, 7, 4], 95, [55], "exemplo 0")
#prob = GG([43, 38, 37, 9, 6], [4, 4, 2, 5, 8], 66, [115], "exemplo 1")
#prob = GG([54, 42, 34, 33, 15], [2, 2, 9, 1, 3], 79, [148], "exemplo 2")
#prob = GG([58, 51, 40, 29, 14], [10, 6, 1, 3, 2], 95, [135], "exemplo 3")
#prob = GG([64, 46, 23, 17, 15], [9, 5, 8, 9, 7], 85, [184], "exemplo 5")
#prob = GG([37, 31, 29, 22, 13], [7, 1, 7, 5, 1], 51, [158], "exemplo 6")
#prob = GG([50, 43, 42, 14, 8], [8, 7, 5, 6, 10], 85, [179], "exemplo 7")
#prob = GG([47, 42, 41, 22, 16], [6, 7, 9, 7, 10], 62, [146], "exemplo 8")
#prob = GG([48, 33, 17, 16, 10], [5, 5, 10, 1, 2], 67, [71], "exemplo 9")
#Classe 3
#prob = GG([24, 19, 18, 16, 15, 14, 12, 11, 10, 5], [8, 3, 1, 3, 9, 3, 6, 7, 10, 8], 99, [93], "exemplo 0")
#prob = GG([26, 24, 21, 17, 16, 14, 12, 11, 8, 7], [9, 10, 7, 5, 3, 3, 8, 3, 9, 4], 70, [191], "exemplo 1")
#prob = GG([23, 17, 16, 15, 14, 12, 11, 9, 8, 7], [5, 7, 1, 1, 4, 9, 10, 9, 10, 9], 86, [473], "exemplo 2")
#prob = GG([28, 14, 13, 12, 11, 9, 8, 7, 6, 5], [7, 8, 4, 10, 5, 10, 6, 7, 7, 4], 74, [231], "exemplo 3")
#prob = GG([29, 20, 16, 15, 14, 13, 12, 10, 8, 5], [5, 7, 2, 8, 1, 5, 3, 1, 2, 5], 82, [336], "exemplo 4")
#prob = GG([28, 21, 18, 17, 16, 15, 12, 11, 10, 9], [6, 5, 5, 3, 4, 3, 4, 8, 5, 1], 92, [415], "exemplo 5")
#prob = GG([28, 25, 19, 17, 10, 9, 8, 7, 6, 5], [2, 9, 9, 1, 7, 7, 2, 9, 5, 10], 56, [366], "exemplo 6")
#prob = GG([28, 17, 14, 13, 12, 11, 10, 9, 8, 7], [1, 6, 1, 8, 5, 8, 5, 2, 5, 5], 72, [292], "exemplo 7")
#prob = GG([30, 24, 21, 19, 18, 16, 10, 9, 8, 7], [1, 1, 2, 1, 4, 4, 8, 2, 2, 7], 64, [292], "exemplo 8")
#prob = GG([29, 21, 16, 15, 14, 13, 12, 10, 9, 6], [9, 7, 5, 1, 2, 2, 4, 9, 1, 2], 84, [303], "exemplo 9")
#Classe 4
#prob = GG([67, 50, 45, 41, 36, 34, 28, 17, 11, 9], [10, 2, 4, 7, 6, 8, 8, 1, 2, 4], 94, [155], "exemplo 0")
#prob = GG([66, 59, 46, 44, 32, 31, 29, 28, 22, 13], [1, 5, 2, 8, 7, 4, 2, 2, 1, 10], 93, [100], "exemplo 1")
#prob = GG([80, 66, 57, 54, 51, 29, 25, 22, 20, 18], [8, 1, 4, 2, 5, 10, 8, 10, 7, 7], 100, [21], "exemplo 2")
#prob = GG([59, 45, 42, 40, 37, 34, 32, 25, 15, 9], [5, 8, 6, 5, 6, 7, 5, 6, 6, 6], 92, [435], "exemplo 3")
#prob = GG([44, 40, 36, 31, 29, 27, 26, 21, 16, 7], [4, 10, 5, 6, 3, 1, 3, 3, 3, 10], 62, [196], "exemplo 4")
#prob = GG([53, 50, 42, 36, 29, 28, 26, 19, 17, 16], [4, 7, 6, 1, 2, 7, 10, 3, 7, 3], 85, [497], "exemplo 5")
#prob = GG([44, 41, 36, 30, 26, 25, 14, 12, 9, 6], [6, 7, 1, 9, 9, 7, 2, 3, 10, 1], 65, [456], "exemplo 6")
#prob = GG([55, 54, 48, 41, 39, 35, 31, 28, 17, 8], [6, 8, 1, 8, 7, 4, 4, 1, 5, 9], 73, [433], "exemplo 7")
#prob = GG([66, 65, 64, 63, 59, 36, 19, 15, 12, 11], [2, 1, 8, 1, 10, 1, 5, 8, 1, 3], 86, [220], "exemplo 8")
#prob = GG([58, 56, 55, 49, 44, 41, 18, 12, 8, 7], [7, 4, 3, 3, 10, 10, 9, 10, 6, 10], 83, [455], "exemplo 9")
#Classe 5
#prob = GG([30, 29, 28, 25, 24, 23, 22, 21, 18, 17, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6], [3, 2, 9, 4, 6, 10, 8, 7, 1, 6, 8, 2, 3, 9, 7, 4, 5, 7, 1, 3], 61, [227], "exemplo 0")
#prob = GG([30, 29, 28, 27, 26, 24, 23, 22, 20, 18, 17, 15, 14, 13, 12, 11, 10, 9, 8, 5], [8, 5, 2, 9, 7, 5, 2, 5, 6, 9, 2, 1, 9, 10, 3, 5, 7, 3, 7, 5], 83, [415], "exemplo 1")
#prob = GG([30, 29, 28, 27, 26, 24, 21, 20, 19, 17, 16, 15, 14, 13, 12, 10, 9, 8, 7, 5], [1, 4, 8, 9, 3, 8, 5, 2, 3, 7, 3, 6, 10, 5, 3, 6, 2, 9, 4, 10], 82, [385], "exemplo 2")
#prob = GG([30, 29, 28, 27, 25, 22, 20, 19, 18, 17, 15, 14, 12, 11, 10, 9, 8, 7, 6, 5], [3, 1, 7, 8, 3, 3, 5, 7, 4, 7, 1, 10, 5, 3, 5, 10, 9, 8, 4, 1], 52, [713], "exemplo 3")
#prob = GG([30, 29, 28, 27, 25, 23, 22, 20, 19, 18, 17, 15, 14, 13, 12, 10, 9, 7, 6, 5], [8, 4, 8, 9, 1, 2, 10, 2, 5, 1, 5, 5, 9, 1, 9, 5, 9, 10, 10, 4], 100, [759], "exemplo 4")
#prob = GG([29, 27, 25, 23, 22, 21, 20, 19, 18, 17, 15, 14, 13, 11, 10, 9, 8, 7, 6, 5], [10, 3, 7, 1, 2, 3, 6, 9, 4, 9, 8, 6, 1, 4, 4, 2, 8, 8, 6, 2], 58, [204], "exemplo 5")
#prob = GG([29, 28, 27, 26, 24, 23, 21, 20, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 5], [3, 10, 1, 8, 4, 8, 4, 4, 6, 5, 3, 7, 1, 3, 5, 9, 2, 10, 8, 8], 89, [959], "exemplo 6")
#prob = GG([29, 28, 26, 25, 24, 23, 22, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7], [7, 9, 2, 2, 4, 8, 8, 4, 9, 1, 2, 10, 8, 8, 9, 8, 9, 9, 5, 6], 75, [748], "exemplo 7")
#prob = GG([30, 29, 28, 27, 25, 20, 19, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5], [6, 4, 7, 8, 3, 5, 4, 3, 10, 2, 3, 3, 3, 10, 8, 6, 3, 7, 8, 2], 76, [838], "exemplo 8")


t0 = time.time()
#prob = GG([30, 29, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 6, 5], [1, 5, 6, 2, 5, 8, 7, 5, 2, 8, 1, 2, 8, 3, 1, 9, 2, 7, 9, 10], 94, [19], "exemplo 9")
#prob = GG([4, 3, 2], [10, 5, 3], 9, [10], "teste1.txt") 
#prob = GG([9, 16, 11, 11, 15, 16, 11, 12, 13, 12], [6, 2, 3, 9, 19, 13, 13, 7, 7, 6], 80,[102], "exemplotestet1")
#prob = GG([9, 16, 11, 11, 15, 16, 11, 12, 13, 12], [14, 8, 9, 17, 18, 12, 8, 6, 6, 4], 80,[23], "exemplotestet2")
#prob = GG([9, 16, 11, 11, 15, 16, 11, 12, 13, 12], [4, 12, 2, 2, 12, 9, 15, 0, 8, 6], 80,[53], "exemplotestet3")
#prob = GG([9, 16, 11, 11, 15, 16, 11, 12, 13, 12], [4, 1, 2, 15, 20, 4, 3, 3, 15, 20], 80,[116], "exemplotestet4")
#prob = GG([9, 16, 11, 11, 15, 16, 11, 12, 13, 12], [19, 11, 6, 19, 20, 14, 17, 18, 0, 20], 80,[167], "exemplotestet5")
#prob = GG([63, 39, 36, 17, 41, 31, 46, 22, 18, 62], [12, 19, 4, 9, 9, 3, 15, 13, 5, 6], 84,[30], "exemploteste1t1")
#prob = GG([63, 39, 36, 17, 41, 31, 46, 22, 18, 62], [4, 17, 7, 4, 20, 14, 2, 7, 16, 6], 84,[256], "exemploteste1t2")
#prob = GG([63, 39, 36, 17, 41, 31, 46, 22, 18, 62], [9, 13, 0, 6, 12, 10, 20, 6, 6, 9], 84,[245], "exemploteste1t3")
#prob = GG([63, 39, 36, 17, 41, 31, 46, 22, 18, 62], [7, 4, 10, 17, 1, 10, 15, 17, 9, 8], 84,[274], "exemploteste1t4")
#prob = GG([63, 39, 36, 17, 41, 31, 46, 22, 18, 62], [2, 19, 1, 1, 1, 16, 2, 4, 5, 20], 84,[85], "exemploteste1t5")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [18, 2, 6, 12, 11, 11, 14, 2, 17, 20], 53,[149], "exemploteste2t1")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [11, 11, 2, 19, 9, 10, 4, 20, 17, 16], 53,[398], "exemploteste2t2")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [9, 6, 11, 0, 18, 17, 19, 9, 0, 6], 53,[469], "exemploteste2t3")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [15, 20, 2, 20, 15, 19, 1, 14, 16, 1], 53,[187], "exemploteste2t4")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [6, 6, 11, 20, 0, 18, 4, 1, 5, 10], 53,[61], "exemploteste2t5")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [8, 0, 19, 4, 5, 7, 1, 1, 3, 10], 53,[99], "exemploteste2t6")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [12, 8, 13, 8, 15, 6, 7, 20, 9, 1], 53,[56], "exemploteste2t7")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [20, 19, 0, 2, 9, 16, 1, 10, 7, 8],53,[47], "exemploteste2t8")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [16, 6, 12, 12, 11, 2, 19, 20, 7, 7], 53,[96], "exemploteste2t9")
#prob = GG([5, 7, 8, 12, 6, 11, 5, 7, 7, 9], [17, 10, 13, 5, 15, 7, 11, 11, 20, 3], 53,[234], "exemploteste2t10")

#prob = GG([4, 3, 2], [10, 5, 3], 9, [20], "testet1.txt") 
#prob = GG([4, 3, 2], [15, 25, 2], 9, [15], "testet2.txt") 
#prob = GG([4, 3, 2], [12, 0, 7], 9, [35], "testet3.txt") 
#prob = GG([4, 3, 2], [5, 6, 20], 9, [8], "testet4.txt") 

#prob = GG([4, 3, 2], [10, 5, 3], 9, [10], "teste1.txt") 
#prob = GG([4, 3, 2], [0, 5, 7], 9, [9], "teste2.txt") ]

#prob = GG([4, 3, 2], [10, 5, 3], 9, [10], "testet1.txt") 
#prob = GG([4, 3, 2], [0, 5, 7], 9, [9], "testet2.txt") 
#prob = GG([4, 3, 2], [7, 10, 6], 9, [10], "testet3.txt") 
#prob = GG([4, 3, 2], [3, 0, 4], 9, [10], "testet4.txt") 

print time.time() - t0,




