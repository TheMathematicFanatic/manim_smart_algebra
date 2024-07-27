from .expressions import *


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

a = SmartVariable("a")
b = SmartVariable("b")
c = SmartVariable("c")
d = SmartVariable("d")

n = SmartVariable("n")

r = SmartVariable("r")
t = SmartVariable("t")
u = SmartVariable("u")
v = SmartVariable("v")

x = SmartVariable("x")
y = SmartVariable("y")
z = SmartVariable("z")

theta = SmartVariable("\\theta")

e = SmartReal(np.e, "e")
pi = SmartReal(np.pi, "\\pi")
tau = SmartReal(np.pi*2, "\\tau")

f = SmartFunction("f")
g = SmartFunction("g")
h = SmartFunction("h")

# i = SmartComplex(1j) ? Don't have this class currently
