# SmartExpression.py
from manim import *
from .utils import *
import random


algebra_config = {
		"auto_parentheses": True,
		"multiplication_mode": "juxtapose",
		"division_mode": "fraction",
		"decimal_precision": 4,
		"always_color": {}
	}


# Main Class
class SmartExpression(MathTex):
	def __init__(self, parentheses=False, **kwargs):
		self.parentheses = parentheses
		if algebra_config["auto_parentheses"]:
			self.auto_parentheses()
		string = add_spaces_around_brackets(str(self))
		super().__init__(string, **kwargs)
		# if algebra_config["always_color"]:
		# 	self.set_color_by_subex(algebra_config["always_color"])
		# Does not work currently, causes infinite recursion for expressions with parentheses
		# due to instantiating new expressions as part of .get_paren_length().
		# Oh jeez it also runs on every single subexpression as the main expression is being constructed, very wasteful.
		# Not sure the better way to do it, leaving this alone for now. 

	def __getitem__(self, key):
		if isinstance(key, (int, slice)): # index of mobject glyphs
			return super().__getitem__(key)
		elif isinstance(key, str): # address of subexpressions, should return the glyphs corresponding to that subexpression
			return self.get_vgroup_from_address(key)

	def get_all_addresses(self):
		# Returns the addresses of all subexpressions
		addresses = [""]
		for n in range(len(self.children)):
			for child_address in self.children[n].get_all_addresses():
				addresses.append(str(n)+child_address)
		return addresses

	def get_subex(self, address_string):
		# Returns the SmartTex object corresponding to the subexpression at the given address.
		# Note that this is not a submobject of self! It is a different mobject probably not on screen,
		# it was just created to help create self.
		if address_string == "":
			return self
		elif int(address_string[0]) < len(self.children):
			return self.children[int(address_string[0])].get_subex(address_string[1:])
		else:
			raise IndexError(f"No subexpression of {self} at address {address_string} .")

	def get_vgroup_from_address(self, address, copy_if_in_list=[]):
		return VGroup(*[
			self[0][g].copy() if g in copy_if_in_list else self[0][g]
			for g in self.get_glyph_indices(address, return_mode=list)
		])

	def is_identical_to(self, other):
		# Checks if they are equal as expressions. Implemented separately in leaves.
		# NOT the same as __eq__ which is used by Manim to check if two mobjects are identical
		# Different instances of the same expression are different mobjects
		return type(self) == type(other) and len(self.children) == len(other.children) \
			and all(self.children[i].is_identical_to(other.children[i]) for i in range(len(self.children)))

	def get_addresses_of_subex(self, subex):
		subex = Smarten(subex)
		addresses = []
		for ad in self.get_all_addresses():
			if self.get_subex(ad).is_identical_to(subex):
				addresses.append(ad)
		return addresses

	def get_glyph_indices(self, address, return_mode=slice):
		# Returns the slice or list of glyph indices corresponding to the subexpression at the given address
		if len(address) > 0 and address[-1] == "_": # gives glyphs for operations.
			return self.get_subex(address[:-1]).get_parent_glyph_indices()
		start = 0
		parent = self
		for n,a in enumerate(address):
			parent = self.get_subex(address[:n])
			paren_length = int( parent.parentheses and parent.paren_length() )
			if isinstance(parent, SmartOperation):
				start += paren_length
				for i in range(int(a)):
					sibling = parent.children[i]
					start += len(sibling)
					start += parent.op_glyph_length
			elif isinstance(parent, SmartNegative):
				start += paren_length
				start += 1
			elif isinstance(parent, SmartFunction):
				start += paren_length
				start += len(parent.symbol)
				start += int(parent.func_parentheses)
			else:
				raise ValueError(f"Something has gone wrong here. Parent: {type(parent)}, {parent}, address string: {address}, n: {n}, a: {a}.")
		end = start + len(self.get_subex(address))

		if return_mode == slice:
			return slice(start, end)
		elif return_mode == list:
			return list(range(start, end))
		else:
			raise ValueError(f"Invalid return_mode: {return_mode}. Must be slice or list.")

	def get_parent_glyphs(self, address=""):
		return self[0][self.get_parent_glyph_index(address=address)]

	def get_parent_glyph_index(self, address=""):
		pass #define in subclasses

	def __len__(self):
		return len(self.submobjects[0].submobjects)

	def __neg__(self):
		return SmartNegative(self)

	def __add__(self, other):
		return SmartAdd(self, other)

	def __sub__(self, other):
		return SmartSub(self, other)

	def __mul__(self, other):
		return SmartMul(self, other)

	def __truediv__(self, other):
		return SmartDiv(self, other)

	def __pow__(self, other):
		return SmartPow(self, other)

	def __radd__(self, other):
		return SmartAdd(other, self)

	def __rsub__(self, other):
		return SmartSub(other, self)

	def __rmul__(self, other):
		return SmartMul(other, self)

	def __rtruediv__(self, other):
		return SmartDiv(other, self)

	def __rpow__(self, other):
		return SmartPow(other, self)

	def __iadd__(self, other):
		return self.__add__(other)

	def __isub__(self, other):
		return self.__sub__(other)

	def __imul__(self, other):
		return self.__mul__(other)

	def __itruediv__(self, other):
		return self.__truediv__(other)

	def __ipow__(self, other):
		return self.__pow__(other)

	def __matmul__(self, expression_dict):
		return self.substitute_expressions(expression_dict)

	def __floordiv__(self):
		return SmartEquation(self, other)
	
	def __rfloordiv__(self, other):
		return SmartEquation(other, self)

	def is_negative(self):
		return False # catchall if not defined in subclasses

	def give_parentheses(self, parentheses=True):
		SmartExpression.__init__(self, parentheses=parentheses)
		return self

	def clear_all_parentheses(self):
		for c in self.children:
			c.clear_all_parentheses()
		self.give_parentheses(False)
		return self

	def auto_parentheses(self):
		pass # Implement in subclasses

	def paren_length(self):
		# Returns the number of glyphs taken up by the expression's potential parentheses.
		# Usually 1 but can be larger for larger parentheses.
		yes_paren = SmartExpression.__init__(self.copy(), parentheses=True, color_dict = {})
		no_paren = SmartExpression.__init__(self.copy(), parentheses=False, color_dict = {})
		num_paren_glyphs = len(yes_paren) - len(no_paren)
		assert num_paren_glyphs > 0 and num_paren_glyphs % 2 == 0
		return num_paren_glyphs // 2

	#Man these guys do not work correctly yet
	def nest(self, direction="right"):
		if len(self.children) <= 2:
			return self
		else:
			if direction == "right":
				return type(self)(self.children[0], type(self)(*self.children[1:]))
			elif direction == "left":
				return type(self)(type(self)(*self.children[:-1]), self.children[-1])
			else:
				raise ValueError(f"Invalid direction: {direction}. Must be right or left.")

	def denest(self, denest_all = False, match_type = None):
		if len(self.children) <= 1:
			return self
		if match_type is None:
			match_type = type(self)
		new_children = []
		for child in self.children:
			if type(child) == match_type:
				for grandchild in child.children:
					new_children.append(grandchild.denest(denest_all, match_type))
			elif denest_all:
				new_children.append(child.denest(True, match_type))
			else:
				new_children.append(child)
		return type(self)(*new_children)

	def substitute_at_address(self, subex, address):
		subex = Smarten(subex).copy() #?
		if len(address) == 0:
			return subex
		new_child = self.children[int(address[0])].substitute_at_address(subex, address[1:])
		new_children = self.children[:int(address[0])] + [new_child] + self.children[int(address[0])+1:]
		return type(self)(*new_children)

	def substitute_at_addresses(self, subex, addresses):
		result = self.copy()
		for address in addresses:
			result = result.substitute_at_address(subex, address)
		return result

	def substitute_expressions(self, expression_dict):
		result = self.copy()
		for from_subex, to_subex in expression_dict.items():
			result = result.substitute_at_addresses(to_subex, result.get_addresses_of_subex(from_subex))
		return result
	
	# to do: add argument include_parentheses to determine whether the parentheses around the subexpressions,
	# if they exist, should also be recolored or left alone.
	def set_color_by_subex(self, subex_color_dict):
		for subex, color in subex_color_dict.items():
			for ad in self.get_addresses_of_subex(Smarten(subex)):
				self[ad].set_color(color)

# Operation Classes
class SmartNegative(SmartExpression):
	def __init__(self, child, **kwargs):
		self.children = [Smarten(child)]
		super().__init__(**kwargs)

	@tex
	def __str__(self, *args, **kwargs):
		return "-" + str(self.children[0])

	def auto_parentheses(self):
		if isinstance(self.children[0], (SmartAdd, SmartSub)) or self.children[0].is_negative():
			self.children[0].give_parentheses()
		self.children[0].auto_parentheses()

	def is_negative(self):
		return True

class SmartOperation(SmartExpression):
	def __init__(self, *children, **kwargs):
		self.children = list(map(Smarten,children))
		super().__init__(**kwargs)

	@tex
	def __str__(self, spacing="", *args, **kwargs):
		joiner = spacing + self.op_string + spacing
		result = joiner.join(["{" + str(child) + "}" for child in self.children])
		return result

	def get_parent_glyph_indices(self, address=""):
		indices = []
		for i in range(len(self.children)):
			for j in range(self.op_glyph_length):
				indices.append()
		return indices


	def compute(self):
		result = self.children[0].compute()
		for child in self.children[1:]:
			result = self.eval_op(result, child.compute())
		return Smarten(result)

class SmartAdd(SmartOperation):
	def __init__(self, *children, **kwargs):
		self.op_string = "+"
		self.op_glyph_length = 1
		self.eval_op = lambda x,y: x+y
		super().__init__(*children, **kwargs)

	def auto_parentheses(self):
		for child in self.children:
			child.auto_parentheses()

	def is_negative(self):
		return self.children[0].is_negative()

class SmartSub(SmartOperation):
	def __init__(self, *children, **kwargs):
		self.op_string = "-"
		self.op_glyph_length = 1
		self.eval_op = lambda x,y: x-y
		super().__init__(*children, **kwargs)

	def auto_parentheses(self):
		self.children[0].auto_parentheses()
		for child in self.children[1:]:
			if isinstance(child, (SmartAdd, SmartSub)) or child.is_negative():
				child.give_parentheses()
			child.auto_parentheses()

	def is_negative(self):
		return self.children[0].is_negative()

class SmartMul(SmartOperation):
	def __init__(self, *children, mode=algebra_config["multiplication_mode"], **kwargs):
		if mode=="dot":
			self.op_string = r"\cdot"
			self.op_glyph_length = 1
		elif mode == "juxtapose":
			if any([isinstance(child, SmartFunction) for child in children]):
				self.op_string = r"\,"
			else:
				self.op_string = ""
			self.op_glyph_length = 0
		else:
			raise ValueError("multiplication mode must be dot or juxtapose")
		self.eval_op = lambda x,y: x*y
		super().__init__(*children, **kwargs)

	def auto_parentheses(self):
		for child in self.children:
			if isinstance(child, (SmartAdd, SmartSub)) or child.is_negative():
				child.give_parentheses()
			child.auto_parentheses()

	def is_negative(self):
		return self.children[0].is_negative()

class SmartDiv(SmartOperation):
	def __init__(self, *children, mode=algebra_config["division_mode"], **kwargs):
		if mode == "fraction":
			self.op_string = r"\over"
			self.op_glyph_length = 1
		elif mode == "inline":
			self.op_string = r"\div"
			self.op_glyph_length = 1
		self.eval_op = lambda x,y: x/y
		super().__init__(*children, **kwargs)

	def auto_parentheses(self):
		for child in self.children:
			if (isinstance(child, (SmartAdd, SmartSub, SmartMul, SmartDiv)) or child.is_negative()) and algebra_config["division_mode"] == "inline":
				child.give_parentheses()
			child.auto_parentheses()

	def is_negative(self):
		return self.children[0].is_negative() or self.children[1].is_negative()

class SmartPow(SmartOperation):
	def __init__(self, *children, **kwargs):
		self.op_string = "^"
		self.op_glyph_length = 0
		self.eval_op = lambda x,y: x**y
		super().__init__(*children, **kwargs)

	def auto_parentheses(self):
		assert len(self.children) == 2 #idc how to auto paren power towers
		if isinstance(self.children[0], SmartOperation) or self.children[0].is_negative():
			self.children[0].give_parentheses()
		for child in self.children:
			child.auto_parentheses()

	def is_negative(self):
		return False

# Number Classes
class SmartNumber(SmartExpression):
	def __init__(self, **kwargs):
		self.children = []
		super().__init__(**kwargs)

	def compute(self):
		return float(self)

class SmartInteger(SmartNumber):
	def __init__(self, n, **kwargs):
		self.n = n
		super().__init__(**kwargs)

	@tex
	def __str__(self, *args, **kwargs):
		return str(self.n)

	def __float__(self):
		return float(self.n)

	def is_identical_to(self, other):
		return type(self) == type(other) and self.n == other.n

	def is_negative(self):
		return self.n < 0

	@staticmethod
	def GCF(*smartnums):
		smartnums = list(map(Smarten, smartnums))
		nums = list(map(lambda N: N.n, smartnums))
		return Smarten(int(np.gcd.reduce(nums)))

	@staticmethod
	def LCM(*smartnums):
		smartnums = list(map(Smarten, smartnums))
		nums = list(map(lambda N: N.n, smartnums))
		return Smarten(int(np.lcm.reduce(nums)))

	def prime_factorization(self):
		...

class SmartRational(SmartNumber): #multiclassing SmartDiv is not worth the trouble
	def __init__(self, a, b, **kwargs):
		for n in [a, b]:
			if not isinstance(n, (SmartInteger, int)):
				raise TypeError (f"Unsupported type {type(n)}")
		self.a = Smarten(a)
		self.b = Smarten(b)
		self.children = [self.a, self.b]
		super().__init__(**kwargs)

	@tex
	def __str__(self, **kwargs):
		return "{" + str(self.a) + r" \over " + str(self.b) + "}"

	def __float__(self):
		return float(self.a) / float(self.b)

	def is_identical_to(self, other):
		return type(self) == type(other) and self.a.is_identical_to(other.a) and self.b.is_identical_to(other.b)

	def is_negative(self):
		return self.a.is_negative() or self.b.is_negative()

	def convert_to_smartdiv(self):
		return SmartDiv(self.a, self.b)

class SmartReal(SmartNumber):
	def __init__(self, x, symbol=None, **kwargs):
		self.x = x
		self.symbol = symbol
		super().__init__(**kwargs)

	@tex
	def __str__(self, decimal_places=4, use_decimal=False, **kwargs):
		if self.symbol and not use_decimal:
			return self.symbol
		rounded = round(self.x, decimal_places)
		if rounded == self.x:
			return str(rounded)
		else:
			return f"{self.x:.{decimal_places}f}" + r"\ldots"

	def __float__(self):
		return float(self.x)

	def is_identical_to(self, other):
		return type(self) == type(other) and self.x == other.x

	def is_negative(self):
		return self.x < 0

# Odds and Ends
class SmartVariable(SmartExpression):
	def __init__(self, symbol, **kwargs):
		self.symbol = symbol
		self.children = []
		super().__init__(**kwargs)

	@tex
	def __str__(self, **kwargs):
		return self.symbol

	def is_identical_to(self, other):
		return type(self) == type(other) and self.symbol == other.symbol

	def compute(self):
		raise ValueError(f"Expression contains a variable {self.symbol}.")

class SmartRelation(SmartExpression):
	def __init__(self, symbol, *inputs, **kwargs):
		self.symbol = symbol
		self.children = list(map(Smarten,inputs))
		super().__init__(**kwargs)

	@tex
	def __str__(self, spacing="", *args, **kwargs):
		joiner = spacing + self.symbol + spacing
		result = joiner.join(["{" + str(child) + "}" for child in self.children])
		return result

class SmartEquation(SmartRelation):
	def __init__(self, *inputs, **kwargs):
		super().__init__("=", *inputs, **kwargs)

class SmartFunction(SmartExpression):
	def __init__(self, symbol, *inputs, rule=None, algebra_rule=None, func_parentheses=True, **kwargs):
		self.symbol = symbol #string
		self.rule = rule #lambda function
		self.algebra_rule = algebra_rule #SmEq version of rule?
		self.children = list(map(Smarten,inputs))
		self.func_parentheses = func_parentheses
		super().__init__(**kwargs)

	@tex
	def __str__(self, **kwargs):
		children_tex = ", ".join(["{" + str(child) + "}" for child in self.children])
		if self.func_parentheses:
			return self.symbol + r"\!" + r"\left("*self.func_parentheses + children_tex + r"\right)"*self.func_parentheses
		else:
			return self.symbol + children_tex

	def __call__(self, *inputs, **kwargs):
		assert len(self.children) == 0, f"Function {self.symbol} cannot be called because it already has children."
		return type(self)(self.symbol, *inputs, **kwargs)

	def is_identical_to(self, other):
		return type(self) == type(other) and self.symbol == other.symbol

	def compute(self, *args, **kwargs):
		return self.rule.compute(*args, **kwargs)

def Smarten(input):
	if isinstance(input, SmartExpression):
		return input
	elif isinstance(input, int):
		return SmartInteger(input)
	elif isinstance(input, float):
		return SmartReal(input)
	else:
		raise NotImplementedError(f"Unsupported type {type(input)}")

def random_number_expression(leaves=range(-5, 10), max_depth=3, max_children_per_node=2, **kwargs):
	nodes = [SmartAdd, SmartSub, SmartMul, SmartPow]
	node = random.choice(nodes)
	def generate_child(current_depth):
		if np.random.random() < 1 / (current_depth + 1):
			return SmartInteger(random.choice(leaves))
		else:
			return random_number_expression(leaves, max_depth - 1)
	def generate_children(current_depth, number_of_children):
		return [generate_child(current_depth) for _ in range(number_of_children)]
	if node == SmartAdd or node == SmartMul:
		children = generate_children(max_depth, random.choice(list(range(2,max_children_per_node))))
	elif node == SmartNegative:
		children = generate_children(max_depth, 1)
	else:
		children = generate_children(max_depth, 2)
	return node(*children, **kwargs)

def create_graph(expr, node_size=0.5, horizontal_buff=1, vertical_buff=1.5, printing=False):
	def create_node(address):
		type_to_symbol_dict = {
			SmartInteger: lambda expr: str(expr.n),
			SmartVariable: lambda expr: expr.symbol,
			SmartAdd: lambda expr: "+",
			SmartSub: lambda expr: "-",
			SmartMul: lambda expr: "\\times",
			SmartDiv: lambda expr: "\\div",
			SmartPow: lambda expr: "\\hat{} }",
			SmartNegative: lambda expr: "-",
			SmartFunction: lambda expr: expr.symbol,
			SmartRelation: lambda expr: expr.symbol,
			SmartReal: lambda expr: str(expr.x),
		}
		subex = expr.get_subex(address)
		symbol = type_to_symbol_dict[type(subex)](subex)
		tex = MathTex(symbol)
		# if tex.width > tex.height:
		# 	tex.scale_to_fit_width(node_size)
		# else:
		# 	tex.scale_to_fit_height(node_size)
		return tex
	addresses = expr.get_all_addresses()
	if printing: print(addresses)
	max_length = max(len(address) for address in addresses)
	layered_addresses = [
		[ad for ad in addresses if len(ad) == i]
		for i in range(max_length + 1)
	]
	if printing: print(layered_addresses)
	max_index = max(range(len(layered_addresses)), key=lambda i: len(layered_addresses[i]))
	max_layer = layered_addresses[max_index]
	max_width = len(max_layer)
	if printing: print(max_index, max_width, max_layer)
	Nodes = VDict({ad: create_node(ad) for ad in addresses})
	Max_layer = VGroup(*[Nodes[ad] for ad in max_layer]).arrange(RIGHT,buff=horizontal_buff)
	def position_children(parent_address):
		parent = Nodes[parent_address]
		child_addresses = [ad for ad in layered_addresses[len(parent_address)+1] if ad[:-1] == parent_address]
		if printing: print(child_addresses)
		child_Nodes = VGroup(*[Nodes[ad] for ad in child_addresses]).arrange(RIGHT,buff=1)
		child_Nodes.move_to(parent.get_center()+DOWN*vertical_buff)
	for i in range(max_index, max_length):
		for ad in layered_addresses[i]:
			position_children(ad)
	def position_parent(child_address):
		sibling_Nodes = VGroup(*[Nodes[ad] for ad in layered_addresses[len(child_address)] if ad[:-1] == child_address[:-1]])
		parent_Node = Nodes[child_address[:-1]]
		parent_Node.move_to(sibling_Nodes.get_center()+UP*vertical_buff)
	for i in range(max_index, 0, -1):
		for ad in layered_addresses[i]:
			position_parent(ad)
	Edges = VGroup(*[
		Line(
			Nodes[ad[:-1]].get_critical_point(DOWN),
			Nodes[ad].get_critical_point(UP),
			buff=0.2, stroke_opacity=0.4
			)
		for ad in addresses if len(ad) > 0
		])
	return VGroup(Nodes, Edges)
