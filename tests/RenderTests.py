import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from manim import *
from manim_smart_algebra.expressions import *
from manim_smart_algebra.actions import *
from manim_smart_algebra.nicknames import *
from manim_smart_algebra.vstack import *


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


class NewSwapChildren(Scene):
    def construct(self):
        E = a/b+(c-4)/d**2
        tree_addresses = E.get_all_nonleaf_addresses()
        for ad in tree_addresses:
            E_ = E.copy()
            SC = swap_children_(preaddress=ad)
            SC.input_expression = E_
            self.add(E_)
            self.wait()
            self.play(SC.get_animations())
            self.wait()
            self.clear()


class NewApplyOperation(Scene):
    def construct(self):
        A = x+2
        self.add(A)
        act = sub_(3+y, side="left")
        act.input_expression = A
        self.wait()
        self.play(act.get_animations())
        self.wait()


class ApplyOpChild(Scene):
    def construct(self):
        A = (x**2+3*x)/(x-2)
        B = e**x
        act = sub_(B, preaddress="0")
        act.input_expression = A
        self.add(A)
        self.wait()
        self.play(act.get_animations())
        self.wait()
        return
        B = act.output_expression
        print(A in self.mobjects)
        print(B in self.mobjects)
        print(self.mobjects)
        for m in self.mobjects:
            print(m)
            self.play(Indicate(m))
        self.wait()


class AnimAutoParen(Scene):
    def construct(self):
        A = -a - -b
        self.add(A)
        act = swap_children_()
        act.input_expression = A
        self.wait()
        self.play(act.get_animations())
        self.wait()


class FindParenNumber(Scene):
    def construct(self):
        A = (2*x+y)/(x-25*y**3)
        A = A**2
        A = A/A
        A = A**2
        self.add(A.scale(2))
        self.add(index_labels(A[0], color=RED))
        self.wait()


class MultiChildren(Scene):
    def construct(self):
        S = SmartAdd(3, (x**2).give_parentheses(), (-2)**x, 3/(x-2))
        S = (3+e**x)/S
        self.add(S.scale(2))
        self.add(index_labels(S[0], color=RED))
        self.wait()


class TestCombiners(Scene):
    def construct(self):
        algebra_config["division_mode"] = "inline"
        algebra_config["multiplication_mode"] = "times" # This does not work :(
        self.add(VGroup(
            SmartAdd(1,2,3,4,5),
            SmartSub(1,2,3,4,5),
            SmartMul(1,2,3,4,5, mode="x"),
            SmartDiv(1,2,3,4,5, mode="inline"),
            #SmartPow(1,2,3,4,5),
            SmartSequence(1,2,3,4,5),
            SmartEquation(1,2,3,4,5)
        ).arrange(DOWN))
        self.wait()
        self.clear()
        pieces = [1, x**2, x/y, f(x,y,theta), -12*(1-x**2)**3]
        self.add(VGroup(
            SmartAdd(*pieces),
            SmartSub(*pieces),
            SmartMul(*pieces, mode="dot"),
            SmartDiv(*pieces, mode="inline"),
            #SmartPow(*pieces),
            SmartSequence(*pieces),
            SmartEquation(*pieces)
        ).arrange(DOWN))
        self.wait()


class TestSubstituteAction(Scene):
    def construct(self):
        A = (x**2+3*x)/(x-2)
        self.add(A)
        act = substitute_({x:3-y*z}, mode="transform", path_arc=PI)
        act.input_expression = A
        self.wait()
        self.play(act.get_animations())
        self.wait()


class TestFunctionParentheses(Scene):
    def construct(self):
        f = sin(x,y)
        self.add(f, index_labels(f[0], color=RED))
        self.wait()


class TestVStack(Scene):
    def construct(self):
        A = x**2+3*x
        V = VStack(A, [
            div_(e**x),
            swap_children_(),
            substitute_({x:z}),
        ])
        #self.add(V[0])
        #self.add(Circle())
        # self.add(A := MathTex("3x+5"))
        # self.add(B := MathTex("x^2+3x"))
        self.wait()
        self.play(V.actions[0].get_animations())
        self.wait()
        self.play(V.actions[1].get_animations())
        self.wait()
        self.interactive_embed()
        # self.wait()
        # self.play(V.actions[2].get_animations())
        # self.wait()


class TestVStack_2(Scene):
    def construct(self):
        A = x**2+3*x
        V = VStack(A,
            [
                div_(e**x),
                swap_children_(),
                substitute_({x:z}),
                add_((x+y)**3),
                swap_children_(preaddress="10"),
                substitute_({y+x:pi/5, z:-120}),
                swap_children_(preaddress="010"),
                swap_children_(),
                (
                    ([[0,1,2], [2,3,4], {"path_arc":PI}])
                ),
            ],
            color_dict={x:RED,y:BLUE,z:GREEN,e:GREEN_E,pi:PURPLE}    
        )
        V.play_actions(self)