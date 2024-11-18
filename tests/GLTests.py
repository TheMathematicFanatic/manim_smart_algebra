from manimlib import *
import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manim_smart_algebra import *


class Test1(Scene):
    def construct(self):
        A = x**2 + y**2
        self.add(A.mob)
        s = swap_children_()
        B = A >= s
        self.wait()
        self.play(s.get_animation(A,B))
        C = B >= (a:=add_(4))
        self.wait()
        self.play(a.get_animation(B,C))
        D = C >= (m:=mul_(2**z, side="left"))
        self.wait()
        self.play(m.get_animation(C,D))
        self.wait()
        self.embed()
        
        