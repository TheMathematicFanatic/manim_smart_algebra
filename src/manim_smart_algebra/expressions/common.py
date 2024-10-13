from .expression_core import *
from .numbers import *
from .operations import *
from .functions import *
from .relations import *
import numpy as np


SmE = SmartExpression
SmZ = SmartInteger
SmQ = SmartRational
SmR = SmartReal
SmAdd = SmartAdd
SmSub = SmartSub
SmMul = SmartMul
SmDiv = SmartDiv
SmPow = SmartPow
SmNeg = SmartNegative
SmVar = SmartVariable
SmFunc = SmartFunction
SmEq = SmartEquation

a = SmVar("a")
b = SmVar("b")
c = SmVar("c")

n = SmVar("n")
m = SmVar("m")

r = SmVar("r")
t = SmVar("t")
u = SmVar("u")
v = SmVar("v")

x = SmVar("x")
y = SmVar("y")
z = SmVar("z")

e = SmR(np.e, "e")
pi = SmR(np.pi, "\\pi")
tau = SmR(np.pi*2, "\\tau")

f = SmFunc("f", 1)
g = SmFunc("g", 1)
h = SmFunc("h", 1)



def log(base):
    return SmFunc(f"\\log_{base}", 3+len(str(base)),
    rule=lambda x: np.log(x)/np.log(base),
    parentheses_mode="weak")


for i in range(16):
    exec(f"_{i} = SmZ({i})")
