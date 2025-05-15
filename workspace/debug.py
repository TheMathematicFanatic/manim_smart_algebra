import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from MF_Algebra import *

A = x**2 + y**2
B = A.substitute({x:z})
print(B)