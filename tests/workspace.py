import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manim import *
from manim_smart_algebra import *

class Escapism(Scene):
    def construct(self):
        A = x**2 + y**2
        B = A.swap_children_()
        self.add(VGroup(A,B).arrange(DOWN))

# Escapism().render()


class TestAgain(Scene):
    def construct(self):
        B = z.add_(5)
        self.add(VGroup(z,B).arrange(DOWN))

TestAgain().render()


class NLTest(Scene):
    def construct(self):
        NL = NumberLine(
            include_ticks=False
        )
        self.add(NL)
        NL.get_tick(2.5)
