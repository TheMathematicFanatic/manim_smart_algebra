import sys
import os
# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Tools.dual_compatibility import *
from manim_smart_algebra import *



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
        self.wait()
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
        T.add_expression(A)
        T.add_action(s).add_action(s0).add_action(s1).add_action(s).add_action(d).add_action(s).add_action(d0).add_action(s0)
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

