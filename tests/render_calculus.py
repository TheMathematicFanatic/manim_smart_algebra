import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from manim import *
from manim_smart_algebra.expressions import *
from manim_smart_algebra.actions import *
from manim_smart_algebra.nicknames import *
from manim_smart_algebra.vstack import *
from manim_smart_algebra.calculus import *


class TestCalculus(Scene):
    def construct(self):
        dx = d(x)
        f = x**2 * cos(x**3)
        I = Integral(0, inf)(f*dx)

        self.add(I.scale(2))
        self.wait()
        self.add(index_labels(I[0], color=RED))
        self.wait(5)


