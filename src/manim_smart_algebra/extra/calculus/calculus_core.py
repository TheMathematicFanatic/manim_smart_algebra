from ...expressions.expression_core import *
from ...expressions.numbers import SmartReal
from ...expressions.functions import SmartFunction
from ...utils import *


class Infinity(SmartReal):
    def __init__(self, **kwargs):
        super().__init__(np.inf, "\\infty", **kwargs)



class Limit(SmartFunction):
    def __init__(self, variable, value, **kwargs):
        self.variable = variable
        self.value = value
        super().__init__(
            "\\lim_{" + str(variable) + "\\to" + str(value) + "}",
            3 + len(variable) + 1 + len(value),
            parentheses_mode="never",
            **kwargs
        )


class Differential(SmartFunction):
    def __init__(self, **kwargs):
        super().__init__("\\text{d} \\! \\!", 1, parentheses_mode="weak", **kwargs)


class Integral(SmartFunction):
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

