from .expression_core import *
from .numbers import Integer, Real, Rational
from .variables import Variable
from .operations import Add, Sub, Mul, Div, Pow, Negative
from .functions import Function
from .relations import Equation, LessThan, LessThanOrEqualTo, GreaterThan, GreaterThanOrEqualTo
import numpy as np


SmE = Expression
SmZ = Integer
SmQ = Rational
SmR = Real
SmAdd = Add
SmSub = Sub
SmMul = Mul
SmDiv = Div
SmPow = Pow
SmNeg = Negative
SmVar = Variable
SmFunc = Function
SmEq = Equation
SmLt = LessThan
SmLeq = LessThanOrEqualTo
SmGt = GreaterThan
SmGeq = GreaterThanOrEqualTo

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

alpha = SmVar("\\alpha")
beta = SmVar("\\beta")
gamma = SmVar("\\gamma")
theta = SmVar("\\theta")

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

