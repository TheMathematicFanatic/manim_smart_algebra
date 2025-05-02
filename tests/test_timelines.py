import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manimlib import *
from manim_smart_algebra.expressions import *
from manim_smart_algebra.actions import *
from manim_smart_algebra.timelines import *


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
def a():
    return add_(5)

@pytest.fixture
def T(Q, a):
    return SmartTimeline().add_expression(Q).add_action(a)


def test_create_with_rshift(A, B, Q, s, a):
    assert (A >> s).exp_act_pairs == [[A, s]]
    assert (s >> A).exp_act_pairs == [[None, s], [A, None]]
    assert (A >> B).exp_act_pairs == [[A, None], [B, None]]
    assert (s >> a).exp_act_pairs == [[None, s], [None, a]]
    assert (A >> B >> Q).exp_act_pairs == [[A, None], [B, None], [Q, None]]
    assert (Q >> a >> A).exp_act_pairs == [[Q, a], [A, None]]
    assert (A >> Q >> a).exp_act_pairs == [[A, None], [Q, a]]
    assert (s >> Q >> A).exp_act_pairs == [[None, s], [Q, None], [A, None]]
    assert (Q >> a >> s).exp_act_pairs == [[Q, a], [None, s]]
    assert (s >> Q >> a).exp_act_pairs == [[None, s], [Q, a]]
    assert (a >> s >> Q).exp_act_pairs == [[None, a], [None, s], [Q, None]]
    assert (a >> s >> a).exp_act_pairs == [[None, a], [None, s], [None, a]]



