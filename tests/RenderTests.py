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

        P = (x**2 + y**2) / r**2
        self.add(P)


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
        )
        
        eqs_and_trees = VGroup(*[
            VGroup(
                eq.set_color_by_subex(color_dict),
                create_graph(eq)
            ).arrange(DOWN)
            for eq in eqs
        ]).arrange(RIGHT, index_of_submobject_to_align=0)
        # for eq in eqs:
        #     eq.set_color_by_subex(color_dict)
        self.add(eqs_and_trees)
        self.wait()


class NewActions(Scene):
    def construct(self):
        E = (x**2 + y**2) / r**2
        self.add(E)
        SC = SwapChildren(preaddress="01")
        SC.input_expression = E
        self.wait()
        self.play(AnimationGroup(*SC.get_animations()))
        self.wait()


NewActions().render()