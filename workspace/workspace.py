import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from MF_Algebra import *



class Interactive(Scene):
    def construct(self):
        A = x**2 + y**2
        s = swap_children_()
        s0 = swap_children_(preaddress="0")
        s1 = swap_children_(preaddress="1")
        d = div_(z)
        d0 = div_(z, preaddress="0")
        d1 = div_(z, preaddress="1")
        self.add(A.mob)
        self.embed()


class TimelineTest(Scene):
    def construct(self):
        A = x**2 + y**2
        s = swap_children_()
        s0 = swap_children_(preaddress="0")
        s1 = swap_children_(preaddress="1")
        d = div_(z)
        d0 = div_(z, preaddress="0")
        d1 = div_(z, preaddress="1")
        self.add(A.mob)
        T = SmartTimeline()
        T.add_expression_to_end(A)
        T.add_action_to_end(s).add_action_to_end(s0).add_action_to_end(s1).add_action_to_end(s).add_action_to_end(d).add_action_to_end(s).add_action_to_end(d0).add_action_to_end(s0)
        T.propagate()
        self.embed()



class Theorem(Scene):
    def construct(self):
        A = Tex("x^2-4")
        B = Tex("(x-2)(x+2)")
        self.embed()



class CombineAnimations(Scene):
    def construct(self):
        A = Square()
        B = Circle()
        C = Text("Hello")

        AtoB = ReplacementTransform(A,B)
        BtoC = ReplacementTransform(B,C)
        AtoC = Succession(AtoB, BtoC)
        self.add(A)
        #self.play(AtoB)
        #self.play(BtoC)
        self.play(AtoC)
        self.embed()


class KeepGoin(Scene):
    def construct(self):
        A = x**2 + y**2
        self.add(A.mob)
        self.exp = A
        self.embed()


    def action_sequence(self):
        while True:
            action_name = input("Perform action: (or quit)\n>>> ")
            if 'quit' in action_name: break
            temp_locals = {}
            exec('action = ' + action_name, globals(), temp_locals)
            action = temp_locals['action']
            B = self.exp >= action
            self.play(action(self.exp, B))
            self.exp = B


class TreeTest(Scene):
    def construct(self):
        A = x**2 + y**2
        G = create_graph(A)
        A.mob.to_edge(LEFT)
        G.to_edge(RIGHT)
        self.add(A.mob,G)
        self.embed()


class EvaluateTest(Scene):
    def construct(self):
        A = x**2 + y**2
        A = A / (A**3 - A**2 + A)
        B = A >= substitute_({x:-3, y:4})
        E = Evaluate(B)
        self.add(E[0])
        for i in range(len(E)-1):
            self.play(E.actions[i](E.expressions[i], E.expressions[i+1]))
            self.wait()
        self.embed()


class TimelineTest2(Scene):
    def construct(self):
        T = SmartTimeline()
        a**2 + b**2 >> T
        T >> div_(c**2)
        T >> add_(c**2, '1')
        T >> substitute_({a:15, b:8, c:17})
        T >> ( evaluate_('00') | evaluate_('01') | evaluate_('10') | evaluate_('11') )
        T >> ( evaluate_('0') | evaluate_('1') )
        T >> evaluate_()
        B = (1+x)/(1-x**2)
        T >> substitute_into_(B)
        T >> evaluate_('11')
        T >> ( evaluate_('0') | evaluate_('1') )
        T >> evaluate_()

        T.propagate()
        T.get_vgroup().scale(2.5)
        self.add(T.mob)
        T.play_all(self)


class TimelineTest3(Scene):
    def construct(self):
        T = SmartTimeline()
        A = a**2 + b**2
        T >> substitute_({a:SmZ(4)-3, b:SmZ(5)-8})
        T >> evaluate_('00') >> evaluate_('10')
        T >> evaluate_('0') >> evaluate_('1')
        T >> evaluate_()

        self.add(A.mob)
        A >> T
        T.propagate()

        self.embed()
        


class TimelineTest4(Scene):
    def construct(self):
        T = AutoTimeline(auto_color={a:RED, b:GREEN, c:BLUE})
        A = a**2 + b**2
        A >> T
        T >> div_(c**2) >> add_((a/b)**2)
        T.propagate()
        self.add(A.mob)
        self.embed()



class FunctionSubstituteTest(Scene):
    def construct(self):
        F = f(x)
        A = y & x**2-5
        T = A >> ( substitute_into_(F, preaddress='0') | substitute_into_(F, preaddress='1') )
        T.propagate()
        self.add(T.mob)
        #self.embed()


class EvaluateTimelineTest(Scene):
    def construct(self):
        A = (a+b)/2 + (x+y)/25
        A = A.substitute({a:5, b:15, y:20})
        E = Evaluate(A, show_past_steps=True)
        self.add(E.mob)
        self.embed()


class ShowStepsTimelineTest(Scene):
    def construct(self):
        A = x**2 - y**2
        T = Evaluate(
            show_past_steps = True,
            auto_color = {x:RED, y:BLUE, e:GREEN, 3:YELLOW, -15:PURPLE}
        )
        A >> T >> div_(e**x-2+2) >> add_((x+y)**3) >> substitute_({x:1}) >> substitute_({y:4})
        self.play(Write(T.mob))
        T.play_all(self)
        self.play(self.camera.frame.animate.rotate(PI/3, RIGHT), run_time=3)
        self.wait()



class AlgebraicActionTest(Scene):
    def construct(self):
        A = x**2 + y**2
        T = SmartTimeline()
        A >> T
        T >> AlgebraicAction(a+b, a/b)
        T >> AlgebraicAction(a/b, b/a)
        T >> AlgebraicAction(a/b, (b/a)**-1)
        T.propagate()
        self.add(T.mob)
        self.embed()


class EvaluateTimelineTest2(Scene):
    def construct(self):
        E = Evaluate(show_past_steps=True, auto_color={a:RED, b:GREEN, c:BLUE})
        a**2 + b**2 >> E
        E >> div_(c**2+3**a)
        E >> substitute_({a:3, b:4})
        E >> sub_(100, side='left')
        E >> substitute_({c:3})

        self.add(E.mob)
        self.embed()
        E.play_all(self)