__version__ = '0.3.2'
__author__ = 'John Connell - The Mathematic Fanatic'
__description__ = 'Manim plugin which subclasses MathTex to make it much easier to animate algebra.'

from .expressions import *
#from .actions import *

"""
.expressions contains the main mobject classes of the entire plugin
.actions contains the animation classes, not currently imported because they are not ready yet
.utils not imported because they are intended for internal use only
.nicknames not imported, they are intended to be optionally imported with * if desired.


from manim import *
import manim_smart_algebra as msa
from manim_smart_algebra.nicknames import * #optional

or something like that depending on preferences. I personally will do

from manim import *
from manim_smart_algebra import *
from manim_smart_algebra.nicknames import *
"""
