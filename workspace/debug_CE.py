import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manim import *
from manim_smart_algebra import *


class CheckStuff(Scene):
    def construct(self):
        A = x**2 + y**2
        self.add(A.mob)
        A['10'].set_color(RED)

CheckStuff().render()