from .calculus_core import *
from ...expressions.common import *


inf = Infinity()
d = Differential()
dx = d(x)
dy = d(y)
dz = d(z)
dt = d(t)
dr = d(r)
theta = SmVar("\\theta")
dtheta = d(theta)

# None of this works currently due to a problem in SmartFunction lol
# a = SmartVariable('a')
# b = SmartVariable('b')
# SumRule = AlgebraicAction(d(a+b), d(a) + d(b))
# DifferenceRule = AlgebraicAction(d(a-b), d(a) - d(b))
# ProductRule = AlgebraicAction(d(a*b), d(a)*b + a*d(b))
# QuotientRule = AlgebraicAction(d(a/b), (d(a)*b - a*d(b))/b**2)
# PowerRule = AlgebraicAction(d(a**b), b*d(a**(b-1))*d(a))
