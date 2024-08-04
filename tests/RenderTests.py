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


class TestSubexColor(Scene):
    def construct(self):
        color_dict = {theta:GREEN, x:RED, y:BLUE, r:YELLOW}

        P = (x**2 + y**2) & r**2
        P.set_color_by_subex(color_dict)
        self.add(P)
        self.wait()


class Interactive(Scene):
    def construct(self):
        A = 3*x+5
        self.interactive_embed()
        Square().rotate()


#TestAlwaysColorConfig().render()

class PolarRectConversions(Scene):
    def construct(self):
        color_dict = {theta:GREEN, x:RED, y:BLUE, r:YELLOW}

        eqs = VGroup(
            x**2 + y**2 & r**2,
            sin(theta) & y/r,
            cos(theta) & x/r,
            tan(theta) & y/x,
            f(x,y,theta)+3*r,
        )
        
        eqs_and_trees = VGroup(*[
            VGroup(
                eq.set_color_by_subex(color_dict),
                create_graph(eq)
            ).arrange(DOWN)
            for eq in eqs
        ])
        for eqt in eqs_and_trees:
            self.add(eqt)
            self.wait()
            self.clear()


class NewActions(Scene):
    def construct(self):
        E = a/b+(c-4)/d**2
        preads = {ad[:-1] for ad in E.get_all_addresses()}
        print(preads)
        for ad in preads:
            E_ = E.copy()
            SC = SwapChildren(preaddress=ad)
            SC.input_expression = E_
            self.add(E_)
            self.wait()
            self.play(AnimationGroup(*SC.get_animations()))
            self.wait()
            self.clear()
        self.wait()