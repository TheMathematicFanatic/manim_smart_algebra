from manim import *
from .expressions import *
from .actions import *
from .utils import *


class Infinity(SmartReal):
    def __init__(self, **kwargs):
        super().__init__(np.inf, "\\infty", **kwargs)


class Limit(SmartFunction):
    def __init__(self, variable, value)
