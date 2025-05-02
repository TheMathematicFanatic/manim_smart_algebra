import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from manimlib import *
from manim_smart_algebra.expressions import *
from manim_smart_algebra.actions import *
from manim_smart_algebra.timelines import *



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
        d = SmVar('d')
        E = a/b+(c-4)/d**2
        tree_addresses = E.get_all_nonleaf_addresses()
        for ad in tree_addresses:
            E_ = E.copy()
            SC = swap_children_(preaddress=ad)
            self.add(E_.mob)
            self.wait()
            self.play(SC.get_animation()(E_))
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
        algebra_config["multiplication_mode"] = "x" # Does this work? Yes!
        self.add(VGroup(
            SmartAdd(1,2,3,4,5),
            SmartSub(1,2,3,4,5),
            SmartMul(1,2,3,4,5),
            SmartDiv(1,2,3,4,5),
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



class TestVStack_3(Scene):
    def construct(self):
        A = x**2 + y**2
        V = VStack(A,
            [
                div_(e**x),
                swap_children_(),
                substitute_({x:z}),
                add_((x+y)**3),
                swap_children_(preaddress="10"),
                substitute_({y+x:pi/5, z:-120}, lag_ratio=0.02),
                swap_children_(preaddress="010"),
                swap_children_(),
                
                # (
                #     ([[0,1,2], [2,3,4], {"path_arc":PI}])
                # ),
            ],
            color_dict={x:RED,y:BLUE,z:GREEN,e:GREEN_E,pi:PURPLE}    
        )
        V.play_actions(self)


class TestVStack_4(Scene):
    def construct(self):
        A = x**2 + y/2
        V = VStack(A,
            [
                add_(A),
                swap_children_(),
                substitute_({x:z}),
                swap_children_(preaddress="10"),
                substitute_({y:A}, preaddress="1"),
                swap_children_(preaddress="1"),
                substitute_({x:1, y:2, z:3}),
                evaluate_(preaddress="0"),
                swap_children_(),
                evaluate_(preaddress="0"),
                evaluate_(),
                add_(SmQ(2,3)),
                #evaluate_(preaddress="1"),
                evaluate_()
            ],
            color_dict={x:RED,y:BLUE,z:GREEN,e:GREEN_E,pi:PURPLE},
            scale=2
        )
        V.play_actions(self)


#TestVStack_4().render()


class DemoSub(Scene):
    def construct(self):
        A = a**2 + b**2

        B = A / (3 - e**x)

        C = B @ {a:3, b:-4, e**x:z}

        self.add(VGroup(A,B,C).arrange(DOWN, buff=0.8).scale_to_fit_height(7.5))



class TestAlgebraicAction_1(Scene):
    def construct(self):
        A = x/3
        s = AlgebraicAction(a/b, b/a, {a:{"path_arc":PI, "delay":0.3}, b:{"path_arc":PI}})
        V = VStack(A, [s], scale=3)
        self.add(V[0])
        V.play_actions(self)


class TestAlgebraicAction_2(Scene):
    def construct(self):
        A = (a**2 + b**2) / (3 - e**x)
        pow_reciprocal_ = AlgebraicAction(
            a/b, (b/a)**-1, {a:{"path_arc":PI}, b:{"path_arc":PI}}
        )
        V = VStack(A, [pow_reciprocal_])
        self.add(V[0])
        V.play_actions(self)


class TestZipper(Scene):
    def construct(self):
        a = 6
        b = 1
        p = 3
        q = 9

        x = SmVar("x")
        factor1 = x+p
        factor2 = x+q
        expanded = x**2 + (p+q)*x + (p*q)
        numerator = a*x+b
        A, B = SmVar("A"), SmVar("B")

        Z = Zipper(

            (
                SmEq(numerator / expanded, A/factor1 + B/factor2),
                
                    AddressMapAction(("01", "01"))
            ),
            (
                SmEq(numerator / (factor1 * factor2), A/factor1 + B/factor2),
                
                    AddressMapAction(("01", "11", {"path_arc":-PI}), (Write, "11()", {"delay":0.8}))
            ),
            (
                SmEq(numerator, (A/factor1 + B/factor2)*(factor1*factor2)),
                
                    distribute_(preaddress="1", mode="right")
            ),
            (
                _,
                
                    _
            ),
            (
                SmEq(numerator, A*factor2 + B*factor1),
                
                    _
            ),
        )


class TestAddOverride(Scene):
    def construct(self):
        A = x**2 + y**2
        self.add(A, Square())


class TestAddOverride2(Scene):
    def construct(self):
        A = x**2 + y**2
        V = VGroup(A, Square())
        self.add(V)

from manim_smart_algebra.extra.trigonometry.common import *
class TestAlwaysColor(Scene):
    def __init__(self, *args, **kwargs):
        # config.background_color = WHITE
        # MathTex.set_default(color=BLACK)
        super().__init__(*args, **kwargs)
    
    def construct(self):
        algebra_config["always_color"] = {x:RED, y:BLUE, r:YELLOW_D, theta:GREEN_E}
        V = VGroup(
            x & r*cos(theta),
            y & r*sin(theta),
            r**2 & x**2 + y**2,
            tan(theta) & y/x,
        ).arrange_in_grid(2,2,buff=1).to_edge(UP)
        self.add(V)

        NP = NumberPlane(
            x_range=[-1.5,1.5,0.5],
            y_range=[-1.5,1.5,0.5],
            x_length=4, 
            y_length=4,
            background_line_style={"stroke_color":GREY, "stroke_opacity":0.5},
        ).to_edge(DOWN)
        circle = NP.plot_implicit_curve(lambda x,y: x**2 + y**2 - 1)
        from MF_Tools import VT
        th = VT(0.01)
        r_line = always_redraw(lambda:
            Line(NP.coords_to_point(0,0,0), NP.c2p(np.cos(~th), np.sin(~th), 0)).set_color(algebra_config["always_color"][r])
        )
        x_line = always_redraw(lambda:
            Line(NP.c2p(0,0,0), NP.c2p(np.cos(~th),0,0)).set_color(algebra_config["always_color"][x])
        )
        y_line = always_redraw(lambda:
            Line(NP.c2p(np.cos(~th),0,0), NP.c2p(np.cos(~th), np.sin(~th), 0)).set_color(algebra_config["always_color"][y])
        )
        theta_arc = always_redraw(lambda:
            Arc(angle=~th, radius=0.3, arc_center=NP.c2p(0,0,0)).set_color(algebra_config["always_color"][theta])
        )
        self.add(NP, circle, r_line, x_line, y_line, theta_arc)
        self.play(th@TAU, run_time=10, rate_func=linear)


class TestDotAction(Scene):
    def construct(self):
        A = x+8
        B = A.swap_children_()
        self.add(VGroup(A,B).arrange(DOWN))
#TestDotAction().render()


class TestDotAnimate(Scene):
    def construct(self):
        A = x/y
        self.add(A)
        self.wait()
        self.play(A.animate.swap_children_())
        self.wait()


class ViewPolar(Scene):
    def construct(self):
        from MF_Tools import indexx_labels
        PP = PolarPlane()
        self.add(PP, )#indexx_labels(PP, label_height=0.2))
        for i,c in enumerate([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE][:len(PP)]):
            self.play(Indicate(PP[i], color=c))
        for i in range(len(PP[1])):
            self.play(Indicate(PP[1][i], color=ORANGE))


class FunctionIteration(Scene):
    def construct(self):
        A = SmZ(1)
        f = 1/(1+x)
        s = substitute_into_(f)

        self.add(A.mob)

        for i in range(6):
            B = A >= s
            self.play(s.get_animation()(A,B))
            A = B
            self.wait()

        self.wait()

#FunctionIteration().render()


class SuccTest(Scene):
    def construct(self):
        A = Square()
        B = MathTex("a^2 + b^2").scale(2)
        C = MathTex("5^2 + (-8)^2").scale(2)

        T1 = ReplacementTransform(A,B)
        T2 = AnimationGroup(
            ReplacementTransform(B[0][0:3], C[0][0:3]),
            ReplacementTransform(B[0][3], C[0][3:7]),
            ReplacementTransform(B[0][4], C[0][7])
        )

        self.add(A)
        self.play(T1)
        self.play(T2)
        # self.play(Succession(T1,T2))
        self.wait()
        self.play(Indicate(C))


class EvaluateTest(Scene):
    def construct(self):
        P = a**2 + b**2
        s = substitute_({a:1, b:2})
        e1 = evaluate_(preaddress='0')
        e2 = evaluate_(preaddress='1')
        e3 = evaluate_()

        self.add(P.mob)
        self.wait()
        self.play(s.get_animation()(P))
        self.wait()
        self.play(e1.get_animation()(P))
        self.wait()
        self.play(e2.get_animation()(P))
        self.wait()
        self.play(e3.get_animation()(P))
        self.wait()



class BlankEmbed(Scene):
    def construct(self):
        self.embed()


class TBGM_Testing(Scene):
    def construct(self):
        A = x**2 + y**2
        B = A @ {x:3, y:-4}
        C = B >= evaluate_(preaddress='0')
        D = C >= evaluate_(preaddress='1')
        E = D >= evaluate_()
        self.add(A.mob)
        self.wait()
        self.play(
            TransformByGlyphMap(A.mob, B.mob,
                ([0], [0]),
                ([3], [3,4,5,6])
            ),
        )
        self.wait()
        self.play(
            TransformByGlyphMap(B.mob, C.mob,
                ([0,1], [0]),
            ),
        )
        self.wait()
        self.play(
            TransformByGlyphMap(C.mob, D.mob,
                ([2,3,4,5,6], [2,3]),
            ),
        )
        self.wait()
        self.play(
            TransformByGlyphMap(D.mob, E.mob,
                ([0,1,2,3], [0,1]),
            ),
        )
        self.embed()