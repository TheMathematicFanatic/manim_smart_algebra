# expressions.py
from MF_Tools.dual_compatibility import dc_Tex as Tex, MANIM_TYPE, VGroup
from ..utils import Smarten, tex, add_spaces_around_brackets
from copy import deepcopy


algebra_config = {
		"auto_parentheses": True,
		"multiplication_mode": "juxtapose",
		"division_mode": "fraction",
		"decimal_precision": 4,
		"always_color": {}
	}

class SmartExpression:
	def __init__(self, parentheses=False, **kwargs):
		self.parentheses = parentheses
		if algebra_config["auto_parentheses"]:
			self.auto_parentheses()
		self._mob = None

	@property
	def mob(self):
		if self._mob is None:
			self.init_mob()
		return self._mob

	def init_mob(self, **kwargs):
		string = add_spaces_around_brackets(str(self))
		self._mob = Tex(string, **kwargs)
		self.set_color_by_subex(algebra_config["always_color"])
	
	def copy(self):
		return deepcopy(self)

	def __getitem__(self, key):
		if isinstance(key, str): # address of subexpressions, should return the glyphs corresponding to that subexpression
			if MANIM_TYPE == 'GL':
				return VGroup(*[self.mob[g] for g in self.get_glyphs(key)])
			elif MANIM_TYPE == 'CE':
				return VGroup(*[self.mob[0][g] for g in self.get_glyphs(key)])
			else:
				raise Exception(f"Unknown manim type: {MANIM_TYPE}")
		else: # preserve behavior of Tex indexing
			return self.mob.__getitem__(key)

	def get_all_addresses(self):
		# Returns the addresses of all subexpressions
		addresses = [""]
		for n in range(len(self.children)):
			for child_address in self.children[n].get_all_addresses():
				addresses.append(str(n)+child_address)
		return addresses
	
	def get_all_nonleaf_addresses(self):
		return sorted(list({a[:-1] for a in self.get_all_addresses() if a != ""}))
	
	def get_all_leaf_addresses(self):
		return sorted(list(set(self.get_all_addresses()) - set(self.get_all_nonleaf_addresses())))

	def get_subex(self, address_string):
		# Returns the SmartExpression object corresponding to the subexpression at the given address.
		# Note that this is not a submobject of self! It is a different mobject probably not on screen,
		# it was just created to help create self.
		if address_string == "":
			return self
		elif int(address_string[0]) < len(self.children):
			return self.children[int(address_string[0])].get_subex(address_string[1:])
		else:
			raise IndexError(f"No subexpression of {self} at address {address_string} .")

	def is_identical_to(self, other):
		# Checks if they are equal as expressions. Implemented separately in leaves.
		return type(self) == type(other) and len(self.children) == len(other.children) \
			and all(self.children[i].is_identical_to(other.children[i]) for i in range(len(self.children)))

	def get_addresses_of_subex(self, subex):
		subex = Smarten(subex)
		addresses = []
		for ad in self.get_all_addresses():
			if self.get_subex(ad).is_identical_to(subex):
				addresses.append(ad)
		return addresses

	def get_glyphs_at_address(self, address):
		from .operations import SmartNegative
		from .functions import SmartFunction
		start = 0
		for n,a in enumerate(address):
			parent = self.get_subex(address[:n])
			if parent.parentheses:
				start += parent.paren_length()
			if isinstance(parent, SmartCombiner):
				for i in range(int(a)):
					sibling = parent.children[i]
					start += len(sibling)
					start += parent.symbol_glyph_length
			elif isinstance(parent, SmartNegative):
				start += 1
			elif isinstance(parent, SmartFunction):
				start += parent.symbol_glyph_length
			else:
				raise ValueError(f"Invalid parent type: {type(parent)}. n={n}, a={a}.")
		end = start + len(self.get_subex(address))
		return list(range(start, end))

	def get_left_paren_glyphs(self, address):
		subex = self.get_subex(address)
		if not subex.parentheses:
			return []
		subex_glyphs = self.get_glyphs_at_address(address)
		start = subex_glyphs[0]
		end = start + subex.paren_length()
		return list(range(start, end))

	def get_right_paren_glyphs(self, address):
		subex = self.get_subex(address)
		if not subex.parentheses:
			return []
		subex_glyphs = self.get_glyphs_at_address(address)
		end = subex_glyphs[-1]
		start = end - subex.paren_length()
		return list(range(start+1, end+1))
	
	def get_exp_glyphs_without_parentheses(self, address):
		subex = self.get_subex(address)
		subex_glyphs = self.get_glyphs_at_address(address)
		if not subex.parentheses:
			return subex_glyphs
		else:
			paren_length = subex.paren_length()
			return subex_glyphs[paren_length:-paren_length]
	
	def get_op_glyphs(self, address):
		from .functions import SmartFunction
		subex = self.get_subex(address)
		if not isinstance(subex, (SmartCombiner, SmartFunction)) or subex.symbol_glyph_length==0:
			return []
		subex_glyphs = self.get_glyphs_at_address(address)
		results = []
		turtle = subex_glyphs[0]
		if subex.parentheses:
			turtle += subex.paren_length()
		if isinstance(subex, SmartFunction):
			results += list(range(turtle, turtle + subex.symbol_glyph_length))
		elif isinstance(subex, SmartCombiner):
			for child in subex.children[:-1]:
				turtle += len(child)
				results += list(range(turtle, turtle + subex.symbol_glyph_length))
				turtle += subex.symbol_glyph_length
		return results
	
	def get_glyphs(self, psuedoaddress):
		# Returns the list of glyph indices corresponding to the subexpression at the given address.
		# Can accept special characters at the end to trigger one of the special methods above.
		special_chars = "()_+-*/^,"
		found_special_chars = [(i,c) for (i,c) in enumerate(psuedoaddress) if c in special_chars]
		if len(found_special_chars) == 0:
			return self.get_glyphs_at_address(psuedoaddress)
		else:
			address = psuedoaddress[:found_special_chars[0][0]]
			results = []
			for i,c in found_special_chars:
				if c == "(":
					results += self.get_left_paren_glyphs(address)
				elif c == ")":
					results += self.get_right_paren_glyphs(address)
				elif c == "_":
					results += self.get_exp_glyphs_without_parentheses(address)
				elif c in "+-*/^,":
					results += self.get_op_glyphs(address)
			return sorted(set(results))

	def __len__(self):
		if MANIM_TYPE == 'GL':
			return len(self.mob)
		elif MANIM_TYPE == 'CE':
			return len(self.mob[0])
		else:
			raise Exception(f"Unknown manim type: {MANIM_TYPE}")

	def __neg__(self):
		from .operations import SmartNegative
		return SmartNegative(self)

	def __add__(self, other):
		from .operations import SmartAdd
		return SmartAdd(self, other)

	def __sub__(self, other):
		from .operations import SmartSub
		return SmartSub(self, other)

	def __mul__(self, other):
		from .operations import SmartMul
		return SmartMul(self, other)

	def __truediv__(self, other):
		from .operations import SmartDiv
		return SmartDiv(self, other)

	def __pow__(self, other):
		from .operations import SmartPow
		return SmartPow(self, other)

	def __radd__(self, other):
		from .operations import SmartAdd
		return SmartAdd(other, self)

	def __rsub__(self, other):
		from .operations import SmartSub
		return SmartSub(other, self)

	def __rmul__(self, other):
		from .operations import SmartMul
		return SmartMul(other, self)

	def __rtruediv__(self, other):
		from .operations import SmartDiv
		return SmartDiv(other, self)

	def __rpow__(self, other):
		from .operations import SmartPow
		return SmartPow(other, self)

	def __matmul__(self, expression_dict):
		return self.substitute(expression_dict)

	def __and__(self, other):
		from .relations import SmartEquation
		return SmartEquation(self, other)
	
	def __rand__(self, other):
		from .relations import SmartEquation
		return SmartEquation(other, self)

	def __rshift__(self, other):
		other = Smarten(other)
		from ..actions.action_core import SmartAction
		from ..unifier.zipper import Zipper
		if isinstance(other, SmartExpression):
			return Zipper(
				(self, None),
				(other, None)
			)
		elif isinstance(other, SmartAction):
			return Zipper(
				(self, other)
			)
		elif isinstance(other, Zipper):
			if other.expressions[0]:
				return Zipper(
					(self, None),
					*other.exp_act_pairs,
					**other.kwargs
				)
			else:
				return Zipper(
					(self, other.actions[0]),
					*other.exp_act_pairs[1:],
					**other.kwargs
				)
		else:
			return NotImplemented

	def __rrshift__(self, other):
		return Smarten(other).__rshift__(self)

	def is_negative(self):
		return False # catchall if not defined in subclasses

	def give_parentheses(self, parentheses=True):
		self.parentheses = parentheses
		self._mob = None # Don't init mob just yet, just mark it as needing to be reinitialized
		return self

	def clear_all_parentheses(self):
		for c in self.children:
			c.clear_all_parentheses()
		self.give_parentheses(False)
		return self

	def auto_parentheses(self):
		for child in self.children:
			child.auto_parentheses()
		return self
	
	def reset_parentheses(self):
		self.clear_all_parentheses()
		self.auto_parentheses()
		return self

	def paren_length(self):
		# Returns the number of glyphs taken up by the expression's potential parentheses.
		# Usually 1 but can be larger for larger parentheses.
		yes_paren = self.copy().give_parentheses(True)
		no_paren = self.copy().give_parentheses(False)
		num_paren_glyphs = len(yes_paren) - len(no_paren)
		assert num_paren_glyphs > 0 and num_paren_glyphs % 2 == 0
		return num_paren_glyphs // 2

	#Man these guys do not work correctly yet
	def nest(self, direction="right", recurse=True):
		if len(self.children) <= 2:
			return self
		else:
			if direction == "right":
				return type(self)(self.children[0], type(self)(*self.children[1:]).nest(direction, recurse))
			elif direction == "left":
				return type(self)(type(self)(*self.children[:-1]).nest(direction, recurse), self.children[-1])
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
		from .functions import SmartFunction
		subex = Smarten(subex).copy() #?
		if len(address) == 0:
			return subex
		new_child = self.children[int(address[0])].substitute_at_address(subex, address[1:])
		new_children = self.children[:int(address[0])] + [new_child] + self.children[int(address[0])+1:]
		if isinstance(self, SmartCombiner):
			return type(self)(*new_children)
		elif isinstance(self, SmartFunction):
			SmartFunction(self.symbol, self.symbol_glyph_length, self.rule, self.algebra_rule, self.parentheses_mode)(*new_children)

	def substitute_at_addresses(self, subex, addresses):
		result = self.copy()
		for address in addresses:
			result = result.substitute_at_address(subex, address)
		return result

	def substitute(self, expression_dict):
		result = self.copy()
		dict_with_numbers = list(enumerate(expression_dict.items()))
		from .variables import SmartVariable
		for i, (from_subex, to_subex) in dict_with_numbers:
			result = result.substitute_at_addresses(SmartVariable(f"T_{i}"), result.get_addresses_of_subex(from_subex))
		for i, (from_subex, to_subex) in dict_with_numbers:
			result = result.substitute_at_addresses(to_subex, result.get_addresses_of_subex(SmartVariable(f"T_{i}")))
		return result

	def set_color_by_subex(self, subex_color_dict):
		for subex, color in subex_color_dict.items():
			for ad in self.get_addresses_of_subex(subex):
				self[ad].set_color(color)
				if self.get_subex(ad).parentheses and not subex.parentheses:
					self[ad+"()"].set_color(self.color)
		return self

	def evaluate(self):
		return Smarten(self.compute())

	def __repr__(self):
		return type(self).__name__ + "(" + str(self) + ")"


class SmartCombiner(SmartExpression):
	def __init__(self, symbol, symbol_glyph_length, *children, **kwargs):
		self.symbol = symbol
		self.symbol_glyph_length = symbol_glyph_length
		self.children = list(map(Smarten,children))
		self.left_spacing = ""
		self.right_spacing = ""
		super().__init__(**kwargs)
	
	@tex
	def __str__(self, *args, **kwargs):
		joiner = self.left_spacing + self.symbol + self.right_spacing
		result = joiner.join(["{" + str(child) + "}" for child in self.children])
		return result
	
	def set_spacing(self, left_spacing, right_spacing):
		self.left_spacing = left_spacing
		self.right_spacing = right_spacing

