import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from manim import *
from manim_smart_algebra.expressions import *
from manim_smart_algebra.actions import *
from manim_smart_algebra.nicknames import *


class TestApplyAction(Scene):
    def construct(self):
        A = x**2-5
        A /= 2
        B = A >> swap_children_()
        self.add(B)
        self.wait()
        self.play(swap_children_(address='1')(B))
        self.wait()


class TestAlwaysColorConfig(Scene):
    def construct(self):
        algebra_config['always_color'] = {theta:GREEN, x:RED, y:BLUE, r:YELLOW}

        P = (x**2 + y**2) * r**2
        self.add(P)