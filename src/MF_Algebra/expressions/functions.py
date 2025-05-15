from .expression_core import *
from .sequences import Sequence


class Function(Expression):
	def __init__(self, symbol, symbol_glyph_length, rule=None, algebra_rule=None, parentheses_mode="always", **kwargs):
		self.symbol = symbol #string
		self.symbol_glyph_length = symbol_glyph_length #int
		self.rule = rule #callable
		self.children = [Sequence()] # First child is always a sequence of arguments, further children are parameters like subscripts or indices
		self.algebra_rule = algebra_rule #SmE version of rule?
		self.parentheses_mode = parentheses_mode
		self.spacing = ""
		super().__init__(**kwargs)

	@tex
	def __str__(self):
		return self.symbol + self.spacing + (str(self.children[0]) if len(self.children) > 0 else "")

	def __call__(self, *inputs, **kwargs):
		assert len(self.children[0].children) == 0, f"Function {self.symbol} cannot be called because it already has children."
		new_func = self.copy()
		new_func.children[0].children = list(map(Smarten, inputs))
		# have to reinitialize Expression and MathTex after setting children for correct indexing and auto_paren.
		Expression.__init__(self, parentheses = self.parentheses)
		return new_func
	
	@property
	def arguments(self):
		return self.children[0].children
	
	def set_spacing(self, spacing):
		self.spacing = spacing
		return self
	
	def auto_parentheses(self):
		if len(self.children) == 0:
			return
		child = self.children[0] #sequence
		if len(child.children) == 0:
			return
		if self.parentheses_mode == "always":
			child.give_parentheses(True)
		elif self.parentheses_mode in ["weak", "strong"]:
			from ..expressions.operations import Operation, Add, Sub
			if len(child.children) > 1:
				child.give_parentheses(True)
			elif isinstance(child.children[0], (Add, Sub)):
				child.give_parentheses(True)
			else:
				if self.parentheses_mode == "strong":
					if isinstance(child.children[0], Operation):
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

