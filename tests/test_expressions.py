"""
Most of the important functions are in the SmartExpression class,
but in order to make any reasonable SmartExpressions I first have
to make sure that the leaves and nodes work. So first I will test
most of its subclasses, then follow that up with testing each of the
methods in the main class.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manimlib import *
from manim_smart_algebra.expressions import *

@pytest.fixture
def Q(): #simple rational exp
    Q = (x/y)**2
    return Q

@pytest.fixture
def B(): #big parentheses at "0" with 3 glyphs each
    B = (2*x+y)/(x-25*y**3)
    B = B**2
    B = B/B
    return B**2

@pytest.fixture
def S():
    S = SmartAdd(3, (x**2).give_parentheses(), (-2)**x, 3/(x-2))
    S = (3+e**x)/S
    return S

@pytest.fixture
def F():
    sin = SmartFunction("\\sin", 3, rule=np.sin, parentheses_mode="weak")
    theta = SmartVariable("\\theta")
    F = f(x,y,y**2-x**2)
    F = F / sin(theta)
    return F


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


def test_glyph_indices_small(Q):
    assert len(Q) == 6
    assert Q.get_glyphs_at_address("") == [0,1,2,3,4,5]
    assert Q.get_left_paren_glyphs("") == []
    assert Q.get_right_paren_glyphs("") == []
    assert Q.get_exp_glyphs_without_parentheses("") == [0,1,2,3,4,5]
    assert Q.get_op_glyphs("") == []
    assert Q.get_glyphs_at_address("0") == [0,1,2,3,4]
    assert Q.get_left_paren_glyphs("0") == [0]
    assert Q.get_right_paren_glyphs("0") == [4]
    assert Q.get_exp_glyphs_without_parentheses("0") == [1,2,3]
    assert Q.get_op_glyphs("0") == [2]
    assert Q.get_glyphs_at_address("1") == [5]
    assert Q.get_left_paren_glyphs("1") == []
    assert Q.get_right_paren_glyphs("1") == []
    assert Q.get_exp_glyphs_without_parentheses("1") == [5]
    assert Q.get_op_glyphs("1") == []
    # ~~~ now with shortened syntax ~~~
    assert Q.get_glyphs("") == [0,1,2,3,4,5]
    assert Q.get_glyphs("(") == []
    assert Q.get_glyphs(")") == []
    assert Q.get_glyphs("_") == [0,1,2,3,4,5]
    assert Q.get_glyphs("+") == []
    assert Q.get_glyphs("0") == [0,1,2,3,4]
    assert Q.get_glyphs("0(") == [0]
    assert Q.get_glyphs("0)") == [4]
    assert Q.get_glyphs("0_") == [1,2,3]
    assert Q.get_glyphs("0+") == [2]
    assert Q.get_glyphs("1") == [5]
    assert Q.get_glyphs("1(") == []
    assert Q.get_glyphs("1)") == []
    assert Q.get_glyphs("1_") == [5]
    assert Q.get_glyphs("1+") == []
    assert Q.get_glyphs("0(+)") == [0,2,4]

def test_glyph_indices_large(B):
    assert len(B) == 36
    assert B.get_glyphs_at_address("") == list(range(36))
    assert B.get_left_paren_glyphs("") == []
    assert B.get_right_paren_glyphs("") == []
    assert B.get_exp_glyphs_without_parentheses("") == list(range(36))
    assert B.get_op_glyphs("") == []
    assert B.get_glyphs_at_address("0") == list(range(35))
    assert B.get_left_paren_glyphs("0") == [0,1,2]
    assert B.get_right_paren_glyphs("0") == [32,33,34]
    assert B.get_exp_glyphs_without_parentheses("0") == list(range(3,32))
    assert B.get_op_glyphs("0") == [17]
    assert B.get_glyphs_at_address("1") == [35]
    assert B.get_left_paren_glyphs("1") == []
    assert B.get_right_paren_glyphs("1") == []
    assert B.get_exp_glyphs_without_parentheses("1") == [35]
    assert B.get_op_glyphs("1") == []
    assert B.get_glyphs_at_address("00") == list(range(3,17))
    assert B.get_left_paren_glyphs("00") == []
    assert B.get_right_paren_glyphs("00") == []
    assert B.get_exp_glyphs_without_parentheses("00") == list(range(3,17))
    assert B.get_op_glyphs("00") == []
    assert B.get_glyphs_at_address("000") == list(range(3,16))
    assert B.get_left_paren_glyphs("000") == [3]
    assert B.get_right_paren_glyphs("000") == [15]
    assert B.get_exp_glyphs_without_parentheses("000") == list(range(4,15))
    assert B.get_op_glyphs("000") == [8]
    assert B.get_glyphs_at_address("0000") == [4,5,6,7]
    assert B.get_left_paren_glyphs("0000") == []
    assert B.get_right_paren_glyphs("0000") == []
    assert B.get_exp_glyphs_without_parentheses("0000") == [4,5,6,7]
    assert B.get_op_glyphs("0000") == [6]
    # ~~~ now with shortened syntax ~~~
    assert B.get_glyphs("") == list(range(36))
    assert B.get_glyphs("(") == []
    assert B.get_glyphs(")") == []
    assert B.get_glyphs("_") == list(range(36))
    assert B.get_glyphs("+") == []
    assert B.get_glyphs("0") == list(range(35))
    assert B.get_glyphs("0(") == [0,1,2]
    assert B.get_glyphs("0)") == [32,33,34]
    assert B.get_glyphs("0_") == list(range(3,32))
    assert B.get_glyphs("0+") == [17]
    assert B.get_glyphs("1") == [35]
    assert B.get_glyphs("1(") == []
    assert B.get_glyphs("1)") == []
    assert B.get_glyphs("1_") == [35]
    assert B.get_glyphs("1+") == []
    assert B.get_glyphs("00") == list(range(3,17))
    assert B.get_glyphs("00(") == []
    assert B.get_glyphs("00)") == []
    assert B.get_glyphs("00_") == list(range(3,17))
    assert B.get_glyphs("00+") == []
    assert B.get_glyphs("000") == list(range(3,16))
    assert B.get_glyphs("000(") == [3]
    assert B.get_glyphs("000)") == [15]
    assert B.get_glyphs("000_") == list(range(4,15))
    assert B.get_glyphs("000+") == [8]
    assert B.get_glyphs("0000") == [4,5,6,7]
    assert B.get_glyphs("0000(") == []
    assert B.get_glyphs("0000)") == []
    assert B.get_glyphs("0000_") == [4,5,6,7]
    assert B.get_glyphs("0000+") == [6]
    assert B.get_glyphs("0()") == [0,1,2,32,33,34]
    assert B.get_glyphs("000()/") == [3,8,15]

def test_glyph_indices_multi_children(S):
    assert len(S) == 23
    assert S.get_glyphs_at_address("") == list(range(23))
    assert S.get_left_paren_glyphs("") == []
    assert S.get_right_paren_glyphs("") == []
    assert S.get_exp_glyphs_without_parentheses("") == list(range(23))
    assert S.get_op_glyphs("") == [4]
    assert S.get_glyphs_at_address("0") == [0,1,2,3]
    assert S.get_left_paren_glyphs("0") == []
    assert S.get_right_paren_glyphs("0") == []
    assert S.get_exp_glyphs_without_parentheses("0") == [0,1,2,3]
    assert S.get_op_glyphs("0") == [1]
    assert S.get_glyphs_at_address("1") == list(range(5,23))
    assert S.get_left_paren_glyphs("1") == []
    assert S.get_right_paren_glyphs("1") == []
    assert S.get_exp_glyphs_without_parentheses("1") == list(range(5,23))
    assert S.get_op_glyphs("1") == [6,11,17]
    # ~~~ now with shortened syntax ~~~
    assert S.get_glyphs("") == list(range(23))
    assert S.get_glyphs("(") == []
    assert S.get_glyphs(")") == []
    assert S.get_glyphs("_") == list(range(23))
    assert S.get_glyphs("+") == [4]
    assert S.get_glyphs("0") == [0,1,2,3]
    assert S.get_glyphs("0(") == []
    assert S.get_glyphs("0)") == []
    assert S.get_glyphs("0_") == [0,1,2,3]
    assert S.get_glyphs("0+") == [1]
    assert S.get_glyphs("1") == list(range(5,23))
    assert S.get_glyphs("1(") == []
    assert S.get_glyphs("1)") == []
    assert S.get_glyphs("1_") == list(range(5,23))
    assert S.get_glyphs("1+") == [6,11,17]
    assert S.get_glyphs("1()+*_") == list(range(5,23))

def test_glyph_indices_function(F):
    assert len(F) == 17
    assert F.get_glyphs("") == [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    assert F.get_glyphs("()") == []
    assert F.get_glyphs("_") == [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    assert F.get_glyphs("/") == [12]
    assert F.get_glyphs("0") == [0,1,2,3,4,5,6,7,8,9,10,11]
    assert F.get_glyphs("0()") == []
    assert F.get_glyphs("0_") == [0,1,2,3,4,5,6,7,8,9,10,11]
    assert F.get_glyphs("0/") == [0]
    assert F.get_glyphs("00") == [1,2,3,4,5,6,7,8,9,10,11]
    assert F.get_glyphs("00()") == [1,11]
    assert F.get_glyphs("00_") == [2,3,4,5,6,7,8,9,10]
    assert F.get_glyphs("00,") == [3,5]
    assert F.get_glyphs("002") == [6,7,8,9,10]
    assert F.get_glyphs("002-") == [8]
    assert F.get_glyphs("1") == [13,14,15,16]
    assert F.get_glyphs("1()") == []
    assert F.get_glyphs("1_") == [13,14,15,16]
    assert F.get_glyphs("1*") == [13,14,15]
    assert F.get_glyphs("10") == [16]
    assert F.get_glyphs("100") == [16]

def test_substitute(Q,B):
    assert Q.substitute_at_address(B, "1").is_identical_to((x/y)**B)
    assert Q.substitute_at_address(B, "01").is_identical_to((x/B)**2)
    assert Q.substitute_at_addresses(B, ["0", "1"]).is_identical_to(B**B)
    assert Q.substitute({x:0, y:0}).is_identical_to((SmZ(0)/SmZ(0))**2)
    assert ((e**x - 1)/(3*e**x + 1)).substitute({e**x:x-2}).is_identical_to(((x-2) - 1)/(3*(x-2) + 1))
    
def _disable_test_nest():
    Nl, Nr = SmZ(1), SmZ(1)
    for i in range(2,9):
        Nl = Nl + i
        Nr = i + Nr
    D = SmartAdd(*list(range(1,9)))
    
    assert D.copy().nest("left").is_identical_to(Nl)
    assert D.copy().nest("right").is_identical_to(Nr)

    assert SmartMul(a,b,c,d).nest("left").is_identical_to(a*b*c*d)
    assert SmartMul(a,b,c,d).nest("right").is_identical_to(a*(b*(c*d)))

    assert SmartMul(a,b,c,d).nest("left", recurse=False).is_identical_to(SmartMul(a,b,c)*d)
    assert SmartMul(a,b,c,d).nest("right", recurse=False).is_identical_to(a*SmartMul(b,c,d))






