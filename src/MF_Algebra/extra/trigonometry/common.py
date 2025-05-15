from ...expressions.functions import *
from ...expressions.variables import SmartVariable
import numpy as np


theta = SmartVariable("\\theta")

sin = SmartFunction("\\sin", 3, rule=np.sin, parentheses_mode="weak")
cos = SmartFunction("\\cos", 3, rule=np.cos, parentheses_mode="weak")
tan = SmartFunction("\\tan", 3, rule=np.tan, parentheses_mode="weak")
cot = SmartFunction("\\cot", 3, rule=lambda x: 1/np.tan(x), parentheses_mode="weak")
sec = SmartFunction("\\sec", 3, rule=lambda x: 1/np.cos(x), parentheses_mode="weak")
csc = SmartFunction("\\csc", 3, rule=lambda x: 1/np.sin(x), parentheses_mode="weak")

