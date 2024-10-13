from .expression_core import *


class SmartRelation(SmartCombiner):
	def __init__(self, symbol, symbol_glyph_length, *children, **kwargs):
		super().__init__(symbol, symbol_glyph_length, *children, **kwargs)
	
	def compute(self):
		return all([self.eval_op(self.children[i], self.children[i+1]) for i in range(len(self.children)-1)])

class SmartEquation(SmartRelation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda X,Y: X.exactly_equals(Y)
		super().__init__("=", 1, *children, **kwargs)

	def auto_parentheses(self):
		for child in self.children:
			child.auto_parentheses()
