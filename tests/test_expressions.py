"""
Most of the important functions are in the SmartExpression class,
but in order to make any reasonable SmartExpressions I first have
to make sure that the leaves and nodes work. So first I will test
most of its subclasses, then follow that up with testing each of the
methods in the main class.
"""

def test_SmartVariable():
    assert x == x
    assert x.is_identical_to(x)
    assert x != y
    assert str(x) == 'x'

def test_SmartInteger():
    four = SmZ(4)
    fourteen = SmZ(14)
    neg_eighteen = SmZ(-18)
    assert str(four) == "4"
    assert str(fourteen) == "14"
    assert str(neg_eighteen) == "-18"
    assert four.n == 4
    assert not four.is_negative()
    assert neg_eighteen.is_negative()
    assert SmartInteger.GCF(four, fourteen).n == 2
    assert SmartInteger.GCF(6,10,15).n == 1
    assert SmartInteger.LCM(four, fourteen).n == 28
    assert SmartInteger.LCM(6,10,15).n == 30

def test_SmartReal():
    assert str(pi) == "\\pi"
    assert pi.symbol == "\\pi"
    assert pi.__str__(decimal_places=5, use_decimal=True) == "3.14159\\ldots"
    assert pi.__float__() == 3.141592653589793
    assert pi.x == float(pi)
    assert not pi.is_negative()
    gold2 = SmartReal(-0.6180339887498949)
    assert gold2.is_negative()
    assert str(gold2) == "-0.6180\\ldots"

def test_SmartNegative():
    neg_four = -SmZ(4)
    neg_fourteen = -SmZ(14)
    neg_neg_eighteen = -SmZ(-18)
    neg_x = -x
    assert neg_four.is_negative()
    assert str(neg_four) == "-4"
    assert neg_fourteen.is_negative()
    assert str(neg_fourteen) == "-14"
    # -(-18) should count as a negative in the expression sense
    assert neg_neg_eighteen.is_negative()
    assert str(neg_x) == "-x"
    assert str(neg_neg_eighteen) == "-\\left(-18\\right)"
    assert neg_x.is_negative()




def test_get_glyph_indices():
    A = (x+y)**2-(-x)
    assert A.get_glyph_indices("") == [0,1,2,3,4,5,6,7,8,9,10]
    assert A.get_glyph_indices("0") == [0,1,2,3,4,5]
    assert A.get_glyph_indices("1") == [7,8,9,10]
    assert A.get_glyph_indices("_") == [6]
    assert A.get_glyph_indices("(") == []
    assert A.get_glyph_indices(")") == []
    assert A.get_glyph_indices("(_)") == [6]
    assert A.get_glyph_indices("(_())") == [6]
    assert A.get_glyph_indices("0()") == []
    assert A.get_glyph_indices("0_") == []
    assert A.get_glyph_indices("00()") == [0,4]
    assert A.get_glyph_indices("00_") == [2]
    assert A.get_glyph_indices("00(_") == [0,2]
    assert A.get_glyph_indices("000") == [1]
    assert A.get_glyph_indices("1(") == [7]
    assert A.get_glyph_indices("1)") == [10]
    assert A.get_glyph_indices("1_") == [8]
    assert A.get_glyph_indices("10") == [9]
    assert A.get_glyph_indices("1_0") == [8,9]
    assert A.get_glyph_indices("1_)0") == [8,9,10]
    assert A.get_glyph_indices("10()") == []
    # This is not really done but it'll work for now.


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manim import *
from manim_smart_algebra.expressions import *
from manim_smart_algebra.actions import *
from manim_smart_algebra.nicknames import *
test_get_glyph_indices()



