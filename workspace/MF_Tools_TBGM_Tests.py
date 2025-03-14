import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from manimlib import *
from manim_smart_algebra.actions.animations import *



class Demo_TransformByGlyphMap0(Scene):
    def construct(self):
        exp1 = Tex("f(x) = 4x^2 + 5x + 6").scale(2)
        exp2 = Tex("f(-3) = 4(-3)^2 + 5(-3) + 6").scale(2)
        self.add(exp1)
        self.wait()
        self.play(TransformByGlyphMap(exp1, exp2))
        self.wait()
        self.embed()


class Demo_TransformByGlyphMap1(Scene):
    def construct(self):
        exp1 = Tex("f(x) = 4x^2 + 5x + 6").scale(2)
        exp2 = Tex("f(-3) = 4(-3)^2 + 5(-3) + 6").scale(2)
        self.add(exp1)
        self.wait()
        self.play(TransformByGlyphMap(exp1, exp2,
            ([2], [2,3]),
            ([6], [7,8,9,10]),
            ([10], [14,15,16,17])
        ))
        self.wait()
        self.embed()


class Demo_TransformByGlyphMap2(Scene):
    def construct(self):
        exp1 = Tex("ax^2 + bx + c = 0").scale(2)
        exp2 = Tex("x^2 + \\frac{b}{a}x + \\frac{c}{a} = 0").scale(2)
        self.add(exp1)
        self.wait()
        self.play(TransformByGlyphMap(exp1, exp2,
            ([0], [5], {"path_arc":2/3*PI}),
            ([0], [10], {"path_arc":1/2*PI}),
            ([], [4,9], {"delay":0.25}),
            run_time=2
        ))
        self.wait()
        self.embed()


class Demo_TransformByGlyphMap3(Scene):
    def construct(self):
        exp1 = Tex("\\frac{x^2y^3}{w^4z^{-8}}").scale(2)
        exp2 = Tex("\\frac{x^2y^3z^8}{w^4}").scale(2)
        self.add(exp1)
        self.wait()
        self.play(TransformByGlyphMap(exp1, exp2,
            ([7,9], [4,5]),
            ([8], [], {"shift":exp2[5].get_center() - exp1[9].get_center()}),
        ))
        self.wait()
        self.embed()


class Demo_TransformByGlyphMap4(Scene):
    def construct(self):
        exp1 = Tex("{ 3x+2y \\over 2x+y } + 12z").scale(1.8)
        exp2 = Tex("\\left( { 2x+y \\over 3x+2y } \\right) ^ {-1} + 12z").scale(1.8)
        self.add(exp1)
        self.wait()
        self.play(TransformByGlyphMap(exp1, exp2,
            ([0,1,2,3,4], [6,7,8,9,10], {"path_arc": PI}),
            ([6,7,8,9], [1,2,3,4], {"path_arc": PI}),
            ([], [0], {"delay":0.5}),
            ([], [11], {"delay":0.5}),
            ([], [12,13], {"delay":0.5}),
            default_introducer=Write
        ))
        self.wait()
        self.embed()


class Demo_TransformByGlyphMap5(Scene):
    def construct(self):
        exp1 = Tex("1 \\over 3r+\\theta").scale(2)
        exp2 = Tex("\\left( 3r+\\theta \\right) ^ {-1}").scale(2)
        self.add(exp1)
        self.wait()
        self.play(TransformByGlyphMap(exp1, exp2,
            ([2,3,4,5], [1,2,3,4], {"path_arc": -2/3*PI}),
            ([0,1], FadeOut, {"run_time": 0.5}),
            (GrowFromCenter, [0,5,6,7], {"delay":0.25}),
            introduce_individually=True,
        ))
        self.wait()
        self.embed()


class Demo_TransformByGlyphMap6(Scene):
    def construct(self):
        exp1 = Tex("4x^2 - x^2 + 5x + 3x - 7")
        exp2 = Tex("3x^2 + 8x - 7")
        VGroup(exp1, exp2).arrange(DOWN, buff=1).scale(2)
        self.add(exp1)
        self.wait()
        self.play(TransformByGlyphMap(exp1, exp2,
            ([0,3], [0]),
            ([1,2], [1,2]),
            ([4,5], [1,2]),
            ([7,8,9,10,11], [4,5]),
            from_copy=True
        ))
        self.wait()
        self.embed()


class Demo_TransformByGlyphMap7(Scene):
    def construct(self):
        exp1 = Tex("1 \\over x").scale(1.8)
        exp2 = Tex("{ { 1 \\over x } - { 1 \\over x } } + 10").scale(1.8)
        self.add(exp1)
        self.wait()
        self.play(TransformByGlyphMap(exp1, exp2,
            ([0,1,2], [0,1,2]),
            ([0,1,2], [4,5,6]),
            default_introducer=Write,
            auto_fade=True
        ))
        self.wait()
        self.embed()


