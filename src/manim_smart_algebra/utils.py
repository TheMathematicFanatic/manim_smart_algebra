# Utilities.py
from manim import *
import copy


def tex(func):
	def wrapper(expr, *args, **kwargs):
		pretex = func(expr, *args, **kwargs)
		if expr.parentheses:
			pretex = r" \left( " + pretex + r" \right)"
		return pretex
	return wrapper


def preaddress(func):
	def wrapper(action, expr, *args, **kwargs):
		address = action.address
		#print("action:", action)
		#print("expr:", expr)
		#print("args:", args)
		#print("address:", address)
		#print("kwargs:", kwargs)
		active_part = expr.copy().get_subex(address)
		#print("active_part:", active_part)
		result = func(action, active_part, *args, **kwargs)
		#print("result:", result)
		result_in_context = expr.substitute_at_address(result, address)
		#print("result_in_context:", result_in_context)
		return result_in_context
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
