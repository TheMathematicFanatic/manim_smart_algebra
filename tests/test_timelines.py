import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manimlib import *
from MF_Algebra.expressions import *
from MF_Algebra.actions import *
from MF_Algebra.timelines import *


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
    return Timeline(auto_propagate=False).add_expression_to_end(Q).add_action_to_end(a)


def test_create_with_rshift(A, B, Q, s, a):
    assert (A >> s).steps == [[A, s]]
    assert (s >> A).steps == [[None, s], [A, None]]
    assert (A >> B).steps == [[A, None], [B, None]]
    assert (s >> a).steps == [[None, s], [None, a]]
    assert (A >> B >> Q).steps == [[A, None], [B, None], [Q, None]]
    assert (Q >> a >> A).steps == [[Q, a], [A, None]]
    assert (A >> Q >> a).steps == [[A, None], [Q, a]]
    assert (s >> Q >> A).steps == [[None, s], [Q, None], [A, None]]
    assert (Q >> a >> s).steps == [[Q, a], [None, s]]
    assert (s >> Q >> a).steps == [[None, s], [Q, a]]
    assert (a >> s >> Q).steps == [[None, a], [None, s], [Q, None]]
    assert (a >> s >> a).steps == [[None, a], [None, s], [None, a]]



