from ...expressions.expression_core import *
from ...expressions.numbers import Real
from ...expressions.functions import Function
from ...expressions.relations import Equation
from ...utils import *


class Infinity(Real):
    def __init__(self, **kwargs):
        super().__init__(np.inf, "\\infty", **kwargs)



class Limit(Function):
    def __init__(self, variable, value, **kwargs):
        self.variable = Smarten(variable)
        self.value = Smarten(value)
        super().__init__(
            symbol = "\\lim_{" + str(self.variable) + "\\to" + str(self.value) + "}",
            symbol_glyph_length = 3 + len(self.variable) + 1 + len(self.value),
            parentheses_mode = "weak",
            **kwargs
        )
        self.children += [self.variable, self.value]


class Differential(Function):
    def __init__(self, **kwargs):
        super().__init__(
            symbol = "\\text{d} \\! \\!",
            symbol_glyph_length = 1,
            parentheses_mode="weak",
            **kwargs
        )


class Integral(Function):
    def __init__(self, lower_bound=None, upper_bound=None, **kwargs):
        self.bounds = [Smarten(bound) if bound is not None else None for bound in (lower_bound, upper_bound)]
        symbol = "\\int"
        symbol_glyph_length = 1
        for connector, bound in zip(["_", "^"], self.bounds):
            if bound is not None:
                symbol += connector + "{" + str(bound) + "}"
                symbol_glyph_length += len(bound)
        super().__init__(
            symbol,
            symbol_glyph_length,
            parentheses_mode="weak",
            **kwargs
        )


class Sum(Function):
    def __init__(self, variable, lower_bound, upper_bound, **kwargs):
        self.variable = Smarten(variable)
        self.lower_bound = Smarten(lower_bound)
        self.lower_equation = Equation(self.variable, self.lower_bound)
        self.upper_bound = Smarten(upper_bound)
        super().__init__(
            symbol = "\\sum_{" + str(self.lower_equation) + "}^{" + str(self.upper_bound) + "}",
            symbol_glyph_length = 1 + len(self.lower_equation) + len(self.upper_bound),
            parentheses_mode = "weak",
            **kwargs
        )
        self.children += [self.lower_equation, self.upper_bound]




