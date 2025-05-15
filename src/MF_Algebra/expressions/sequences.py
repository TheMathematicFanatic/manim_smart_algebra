from .expression_core import *


class Sequence(Combiner):
	def __init__(self, *children, generator=None, **kwargs):
		self.generator = generator
		super().__init__(",", 1, *children, **kwargs)
