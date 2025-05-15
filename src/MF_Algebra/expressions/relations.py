from .expression_core import *


class Relation(Combiner):
	def __init__(self, symbol, symbol_glyph_length, *children, **kwargs):
		super().__init__(symbol, symbol_glyph_length, *children, **kwargs)
	
	def compute(self):
		return all([self.eval_op(self.children[i], self.children[i+1]) for i in range(len(self.children)-1)])


class Equation(Relation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda X,Y: X.exactly_equals(Y)
		super().__init__("=", 1, *children, **kwargs)

class LessThan(Relation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda X,Y: X < Y
		super().__init__("<", 1, *children, **kwargs)

class GreaterThan(Relation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda X,Y: X > Y
		super().__init__(">", 1, *children, **kwargs)

class LessThanOrEqualTo(Relation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda X,Y: X <= Y
		super().__init__("\\leq", 1, *children, **kwargs)

class GreaterThanOrEqualTo(Relation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda X,Y: X >= Y
		super().__init__("\\geq", 1, *children, **kwargs)

