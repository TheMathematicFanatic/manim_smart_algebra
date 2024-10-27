import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manim import *
from manim_smart_algebra.expressions import *
from manim_smart_algebra.actions import *
from manim_smart_algebra.unifier.zipper import *


@pytest.fixture
def A():
    return 3*x+5

@pytest.fixture
def B():
    return (2*x+y)/(x-25*y**3)

@pytest.fixture
def Q():
    return (x/y)**2

@pytest.fixture
def s():
    return swap_children_()

@pytest.fixture
def t():
    return add_(5)

@pytest.fixture
def Z(Q, t):
    return Zipper((Q,t))


def test_rshift(A, B, Q, s, t, Z):
    assert A >> s == Zipper((A, s))
    assert s >> A == Zipper((None, s), (A, None))
    assert A >> B == Zipper((A, None), (B, None))
    assert s >> t == Zipper((None, s), (None, t))
    assert Z >> A == Zipper((Q, t), (A, None))
    assert A >> Z == Zipper((A, None), (Q, t))
    assert Z >> s == Zipper((Q, t), (None, s))
    assert s >> Z == Zipper((None, s), (Q, t))
    assert Z >> Z == Zipper((Q, t), (Q, t))
    assert A >> s >> Z == Zipper((A, s), (Q, t))
    assert A >> Z >> s == Zipper((A, None), (Q, t), (None, s))
    assert Z >> A >> s == Zipper((Q, t), (A, s))
