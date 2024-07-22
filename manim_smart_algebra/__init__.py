__version__ = '0.0.1'
__author__ = 'John Connell - The Mathematic Fanatic'
__description__ = 'Manim plugin which subclasses MathTex to make it much easier to animate algebra.'

from .expressions import *
from .actions import *

"""
.utils not imported because they are intended for internal use only
.nicknames not imported, they are intended to be imported with * by the user

from manim import *
import manim_smart_algebra as msa
from manim_smart_algebra.nicknames import *

or something like that depending on preferences
"""
