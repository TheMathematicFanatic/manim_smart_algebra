__version__ = '0.4.0'
__author__ = 'John Connell - The Mathematic Fanatic'
__description__ = 'ManimGL plugin for intelligent animating of algebraic expressions'

from .expressions import *
from .actions import *
from .unifier.zipper import *

"""
.expressions contains the main mobject classes of the entire plugin
.actions contains the animation classes, still pretty under construction but good enough for now
"""
