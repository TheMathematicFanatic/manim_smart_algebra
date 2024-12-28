import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from manim import *
from manim_smart_algebra.expressions import *
from manim_smart_algebra.actions import *


@pytest.fixture
def s():
    return swap_children_()

@pytest.fixture
def a():
    return add_(t)

@pytest.fixture
def A():
    return 3*x+5

@pytest.fixture
def B():
    return (2*x+y)/(x-25*y**3)

@pytest.fixture
def Q():
    return (x/y)**2


def test_swap_children_A(s,A):
    assert s.get_output_expression(A).is_identical_to(5+3*x)
    assert s.get_addressmap(A) == [
            ["0", "1", {"path_arc": 0.75*PI}],
            ["1", "0", {"path_arc": 0.75*PI}]
        ]
    assert s.get_glyphmap(A) == [
            [[0,1], [2,3], {"path_arc": 0.75*PI}],
            [[3], [0], {"path_arc": 0.75*PI}]
        ]
    s.preaddress = "0"
    assert s.get_output_expression(A).is_identical_to(x*3+5)
    assert s.get_addressmap(A) == [
            ["00", "01", {"path_arc": 0.75*PI}],
            ["01", "00", {"path_arc": 0.75*PI}]
        ]
    assert s.get_glyphmap(A) == [
            [[0], [1], {"path_arc": 0.75*PI}],
            [[1], [0], {"path_arc": 0.75*PI}]
        ]


def test_swap_children_Q(s,Q):
    assert s.get_output_expression(Q).is_identical_to(2**(x/y))
    assert s.get_output_expression(Q, preaddress="0").is_identical_to((y/x)**2)
    assert s.get_output_expression(Q).is_identical_to(2**(x/y))
    assert s.get_addressmap(Q) == [
            ["0", "1", {"path_arc": 0.75*PI}],
            ["1", "0", {"path_arc": 0.75*PI}]
        ]
    # assert s.get_glyphmap(Q) == [    # Fails due to parentheses
    #         [[0,1,2,3,4], [1,2,3], {"path_arc": 0.75*PI}],
    #         [[5], [0], {"path_arc": 0.75*PI}]
    #     ]
    s.preaddress = "0"
    assert s.get_output_expression(Q).is_identical_to((y/x)**2)
    assert s.get_addressmap(Q) == [
            ["00", "01", {"path_arc": 0.75*PI}],
            ["01", "00", {"path_arc": 0.75*PI}]
        ]
    # assert s.get_glyphmap(Q) == [    # Fails due to parentheses
    #         [[0], [2], {"path_arc": 0.75*PI}],
    #         [[2], [0], {"path_arc": 0.75*PI}]
    #     ]


def test_swap_children_B(s,B):
    assert s.get_output_expression(B).is_identical_to((x-25*y**3)/(2*x+y))
    assert s.get_output_expression(B, preaddress="0").is_identical_to((y+2*x)/(x-25*y**3))
    assert s.get_output_expression(B, preaddress="1").is_identical_to((2*x+y)/(25*y**3-x))
    assert s.get_output_expression(B, preaddress="00").is_identical_to((x*2+y)/(x-25*y**3))
    assert s.get_output_expression(B, preaddress="1").is_identical_to((2*x+y)/(25*y**3-x))
    assert s.get_output_expression(B, preaddress="11").is_identical_to((2*x+y)/(x-y**3*25))
    assert s.get_output_expression(B, preaddress="111").is_identical_to((2*x+y)/(x-25*3**y))
    assert s.get_addressmap(B) == [
            ["0", "1", {"path_arc": 0.75*PI}],
            ["1", "0", {"path_arc": 0.75*PI}]
        ]


def test_add_A(a,A):
    assert a.get_output_expression(A).is_identical_to(3*x+5+t)
    assert a.get_output_expression(A, preaddress="0").is_identical_to(3*x+t+5)
    assert a.get_output_expression(A, preaddress="1").is_identical_to(3*x+(5+t))
    assert a.get_output_expression(A, preaddress="00").is_identical_to((3+t)*x+5)
    assert a.get_output_expression(A, preaddress="01").is_identical_to(3*(x+t)+5)
    assert a.get_addressmap(A) == [
            ["", "0"],
            [a.introducer, "+", {"delay":0.5}],
            [a.introducer, "1", {"delay":0.6}]
        ]
    assert a.get_glyphmap(A) == [
            [[0,1,2,3], [0,1,2,3]],
            [a.introducer, [4], {"delay":0.5}],
            [a.introducer, [5], {"delay":0.6}]
            
    ]
    a.preaddress = "00"
    assert a.get_output_expression(A).is_identical_to((3+t)*x+5)
    assert a.get_addressmap(A) == [
            ["00", "000"],
            [a.introducer, "00+", {"delay":0.5}],
            [a.introducer, "001", {"delay":0.6}]
        ]
    # assert a.get_glyphmap() == [   # Doesn't work due to parentheses
    #         [[0,1,2,3], [0,1,2,3]]
    #         [a.introducer, [4], {"delay":0.5}],
    #         [a.introducer, [5], {"delay":0.6}]
    # ]    


def test_add_Q(a,Q):
    assert a.get_output_expression(Q).is_identical_to((x/y)**2 + t)
    assert a.get_output_expression(Q, preaddress="0").is_identical_to((x/y+t)**2)
    assert a.get_output_expression(Q, preaddress="1").is_identical_to((x/y)**(2+t))
    assert a.get_output_expression(Q, preaddress="00").is_identical_to(((x+t)/y)**2)
    assert a.get_output_expression(Q, preaddress="01").is_identical_to((x/(y+t))**2)
    assert a.get_output_expression(Q).is_identical_to((x/y)**2 + t)
    assert a.get_addressmap(Q) == [
            ["", "0"],
            [a.introducer, "+", {"delay":0.5}],
            [a.introducer, "1", {"delay":0.6}]
        ]
    assert a.get_glyphmap(Q) == [
            [[0,1,2,3,4,5], [0,1,2,3,4,5]],
            [a.introducer, [6], {"delay":0.5}],
            [a.introducer, [7], {"delay":0.6}]
    ]
    a.preaddress = "0"
    assert a.get_output_expression(Q).is_identical_to((x/y+t)**2)
    assert a.get_addressmap(Q) == [
            ["0", "00"],
            [a.introducer, "0+", {"delay":0.5}],
            [a.introducer, "01", {"delay":0.6}]
        ]
    assert a.get_glyphmap(Q) == [
            [[0,1,2,3,4,5], [0,1,2,3,6,7]],
            [a.introducer, [4], {"delay":0.5}],
            [a.introducer, [5], {"delay":0.6}]
    ]
    a.preaddress = "1"
    assert a.get_output_expression(Q).is_identical_to((x/y)**(2+t))
    assert a.get_addressmap(Q) == [
            ["1", "10"],
            [a.introducer, "1+", {"delay":0.5}],
            [a.introducer, "11", {"delay":0.6}]
        ]
    assert a.get_glyphmap(Q) == [
            [[0,1,2,3,4,5], [0,1,2,3,4,5]],
            [a.introducer, [6], {"delay":0.5}],
            [a.introducer, [7], {"delay":0.6}]
    ]
    a.preaddress = "00"
    assert a.get_output_expression(Q).is_identical_to(((x+t)/y)**2)
    assert a.get_addressmap(Q) == [
            ["00", "000"],
            [a.introducer, "00+", {"delay":0.5}],
            [a.introducer, "001", {"delay":0.6}]
        ]
    assert a.get_glyphmap(Q) == [
            [[0,1,2,3,4,5], [0,1,4,5,6,7]],
            [a.introducer, [2], {"delay":0.5}],
            [a.introducer, [3], {"delay":0.6}]
    ]
    a.preaddress = "01"
    assert a.get_output_expression(Q).is_identical_to((x/(y+t))**2)
    assert a.get_addressmap(Q) == [
            ["01", "010"],
            [a.introducer, "01+", {"delay":0.5}],
            [a.introducer, "011", {"delay":0.6}]
        ]
    assert a.get_glyphmap(Q) == [
            [[0,1,2,3,4,5], [0,1,2,3,6,7]],
            [a.introducer, [4], {"delay":0.5}],
            [a.introducer, [5], {"delay":0.6}]
    ]
    

def test_add_B(a,B):
    assert a.get_output_expression(B).is_identical_to((x-25*y**3)/(2*x+y) + t)
    
# s = swap_children_()
# Q = (x/y)**2
# test_swap_children_Q(s,Q)