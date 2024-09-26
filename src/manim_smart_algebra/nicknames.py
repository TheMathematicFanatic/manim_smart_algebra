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

f = SmartFunction("f", 1)
g = SmartFunction("g", 1)
h = SmartFunction("h", 1)

sin = SmartFunction("\\sin", 3, rule=np.sin, parentheses_mode="weak")
cos = SmartFunction("\\cos", 3, rule=np.cos, parentheses_mode="weak")
tan = SmartFunction("\\tan", 3, rule=np.tan, parentheses_mode="weak")

def log(base):
    return SmartFunction(f"\\log_{base}", 3+len(str(base)),
    rule=lambda x: np.log(x)/np.log(base),
    parentheses_mode="weak")

# i = SmartComplex(1j) ? Don't have this class currently
