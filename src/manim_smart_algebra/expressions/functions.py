from .expression_core import *
from .sequences import SmartSequence


class SmartFunction(SmartExpression):
	def __init__(self, symbol, symbol_glyph_length, rule=None, algebra_rule=None, parentheses_mode="always", **kwargs):
		self.symbol = symbol #string
		self.symbol_glyph_length = symbol_glyph_length #int
		self.rule = rule #callable
		self.children = [] # may be given one child, a sequence which could have multiple children
		self.algebra_rule = algebra_rule #SmE version of rule?
		self.parentheses_mode = parentheses_mode
		self.spacing = ""
		super().__init__(**kwargs)

	@tex
	def __str__(self):
		return self.symbol + self.spacing + (str(self.children[0]) if len(self.children) > 0 else "")

	def __call__(self, *inputs, **kwargs):
		assert len(self.children) == 0, f"Function {self.symbol} cannot be called because it already has children."
		new_func = SmartFunction(self.symbol, self.symbol_glyph_length, self.rule, self.algebra_rule, self.parentheses_mode, **kwargs)
		new_func.children = [SmartSequence(*list(map(Smarten, inputs)), **kwargs)]
		# have to reinitialize SmartExpression and MathTex after setting children for correct indexing and auto_paren.
		super(SmartFunction, new_func).__init__(**kwargs)
		return new_func
	
	def set_spacing(self, spacing):
		self.spacing = spacing
		return self
	
	def auto_parentheses(self):
		if len(self.children) == 0:
			return
		child = self.children[0] #sequence
		if self.parentheses_mode == "always":
			child.give_parentheses(True)
		elif self.parentheses_mode in ["weak", "strong"]:
			from ..expressions.operations import SmartOperation, SmartAdd, SmartSub
			if len(child.children) > 1:
				child.give_parentheses(True)
			elif isinstance(child.children[0], (SmartAdd, SmartSub)):
				child.give_parentheses(True)
			else:
				if self.parentheses_mode == "strong":
					if isinstance(child.children[0], SmartOperation):
						child.give_parentheses(True)
		elif self.parentheses_mode == "never":
			child.give_parentheses(False)
		else:
			raise ValueError(f"Unsupported parentheses mode {self.parentheses_mode}.")
		
	def compute(self, *args):
		if len(args) == 0:
			return self.rule(*map(lambda exp: exp.compute(), self.children[0].children))
		else:
			return self.rule(*args)
	
    #def __pow__(self, other):
    # Gotta do something about sin^2 etc   

