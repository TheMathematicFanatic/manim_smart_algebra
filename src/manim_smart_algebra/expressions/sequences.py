from .expression_core import *


class SmartSequence(SmartCombiner):
	def __init__(self, *children, generator=None, **kwargs):
		self.generator = generator
		super().__init__(",", 1, *children, **kwargs)
	
	def auto_parentheses(self):
		for child in self.children:
			child.auto_parentheses()
