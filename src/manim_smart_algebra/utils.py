# utils.py
from manim import *
#from .expressions import SmartVariable


def tex(func):
	def wrapper(expr, *args, **kwargs):
		pretex = func(expr, *args, **kwargs)
		if expr.parentheses:
			pretex = r"\left(" + pretex + r"\right)"
		return pretex
	return wrapper


def add_spaces_around_brackets(input_string): #GPT
	result = []
	i = 0
	length = len(input_string)

	while i < length:
		if input_string[i] == '{' or input_string[i] == '}':
			if i > 0 and input_string[i - 1] != ' ':
				result.append(' ')
			result.append(input_string[i])
			if i < length - 1 and input_string[i + 1] != ' ':
				result.append(' ')
		else:
			result.append(input_string[i])
		i += 1

	# Join the list into a single string and remove any extra spaces
	spaced_string = ''.join(result).split()
	return ' '.join(spaced_string)


def debug_smarttex(scene, smarttex, show_indices=True, show_addresses=True, show_submobjects=True):
	print("Debugging SmartExpression:")
	print(smarttex)
	print("Length: ", len(smarttex))
	print("Type: ", type(smarttex))
	print("Number of children: ", len(smarttex.children))
	if show_indices:
		for index in range(len(smarttex)):
			index_text = Text(str(index), color=GREEN).next_to(smarttex, DOWN)
			scene.add(index_text)
			scene.play(Indicate(smarttex[0][index], color=GREEN))
			scene.remove(index_text)
	if show_addresses:
		for ad in smarttex.get_all_addresses():
			ad_text = Text(ad, color=ORANGE).next_to(smarttex, DOWN)
			subex_type = Text(type(smarttex.get_subex(ad)).__name__, color=ORANGE).next_to(ad_text, DOWN)
			scene.add(ad_text, subex_type)
			scene.play(Indicate(smarttex[ad], color=ORANGE))
			scene.remove(ad_text, subex_type)
	if show_addresses:
		for i, subm in enumerate(smarttex.submobjects[0]):
			subm_number = Text(str(i), color=BLUE).next_to(subm, DOWN)
			scene.add(subm_number)
			scene.play(Indicate(subm, color=BLUE))
			scene.remove(subm_number)


def match_expressions(template, expression):
	"""
	This function will either return a ValueError if the expression
	simply does not match the structure of the template, such as a missing
	operand or a plus in place of a times, or if they do match it will return
	a dictionary of who's who. For example,
	
	template:      (a*b)**n
	expression:    (4*x)**(3+y)
	return value:  {a:4, b:x, n:3+y}

	template:      n + x**5
	expression:    12 + x**3
	return value:  ValueError("Structures do not match at address 11, 5 vs 3")
	
	template:      x**n*x**m
	expression:    2**2*3**3
	return value:  ValueError("Conflicting matches for x: 2 and 3")

	Obviously this has to be recursive, but gee I am feeling a bit challenged atm...
	...
	Ok I think I've done it! Ugly af type check in the base case but I can't just use
	SmartVariable itself because it leads to a circular import. Surely there is a better way?
	"""

	# Leaf case
	if not template.children:
		#if isinstance(template, SmartVariable):
		if template.__class__.__name__ == 'SmartVariable':
			return {template: expression}
		elif template.is_identical_to(expression):
			return {}
		else:
			raise ValueError("Expressions do not match")
	
	# Node case
	var_dict = {}
	if not isinstance(expression, type(template)):
		raise ValueError("Expressions do not match type")
	if not len(template.children) == len(expression.children):
		raise ValueError("Expressions do not match children length")
	for tc,ec in zip(template.children, expression.children):
		child_dict = match_expressions(tc,ec)
		matching_keys = child_dict.keys() & var_dict.keys()
		if any(not child_dict[key].is_identical_to(var_dict[key]) for key in matching_keys):
			raise ValueError("Conflicting matches for " + str(matching_keys))
		var_dict.update(child_dict)

	return var_dict


				
		

