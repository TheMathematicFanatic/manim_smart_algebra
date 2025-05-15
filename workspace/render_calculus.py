import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


from manimlib import *
from manim_smart_algebra import *
from manim_smart_algebra.extra.calculus import *


ddx = SmartFunction("\\frac{d}{dx}", 4, 'strong')


class SeriesValue(Scene):
    def construct(self):
        S0 = Sum(n, 0, Infinity())
        S1 = Sum(n, 1, Infinity())
        T = ( AutoTimeline()
            >> S0(x**n) >> equals_(1/(1-x))
            >> mul_(ddx, side='left').both
            >> AddressMapAction(['00', '000'], ['0100', '000'], ['1', '1'])
            >> (S0(n*x**(n-1)) & 1/(1-x)**2)
            >> mul_(x, side='left').both
            >> GlyphMapAction(([0], [6], {'path_arc': -PI}), ([7], [6]), ([9,10], []), ([12,13], [9]))
            >> (S0(n*x**n) & x/(1-x)**2)
            >> mul_(ddx, side='left').both
            >> AddressMapAction(['00', '000'], ['0100', '000'], ['1', '1'])
            >> (S0(n**2*x**(n-1)) & (1+x)/(1-x)**3)
            >> mul_(x, side='left').both
            >> GlyphMapAction(([0], [7], {'path_arc': -PI}), ([8], [7]), ([10, 11], []), ([13], [10]), (Write, [11, 15]))
            >> (S0(n**2*x**n) & (x*(1+x))/(1-x)**3)
            >> substitute_({x: x/2})
            # >> distribute_(preaddress='0001')

        )
        self.add(T.mob)
        self.embed()
        T.play_all(self)



class SimpleTest(Scene):
    def construct(self):
        S = Sum(n,1,Infinity())
        A = S((x**n-9)/(x-3))
        self.add(A.mob)
        self.embed()
