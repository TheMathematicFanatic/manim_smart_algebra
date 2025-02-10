from ..expressions.expression_core import *
from ..actions.action_core import *


class Zipper:
	def __init__(self, *exp_act_pairs, **kwargs):
		self.exp_act_pairs = list(exp_act_pairs)
		self.kwargs = kwargs

	@property
	def expressions(self):
		return [pair[0] for pair in self.exp_act_pairs]

	@property
	def actions(self):
		return [pair[1] for pair in self.exp_act_pairs]

	def get_expression(self, i):
		try: expression = self.expressions[i]
		except: expression = None
		if expression is None:
			expression = self.actions[i-1].get_output_expression(self.get_expression(i-1))
			if i == len(self.expressions):
				return expression
			self.expressions[i] = expression
		return expression

	def get_action(self, i):
		try: action = self.actions[i]
		except: action = None
		if action is None:
			from ..actions.variants import AnimationAction
			action = AnimationAction(lambda m1, m2: TransformMatchingTex(m1, m2))
			self.actions[i] = action
		return action

	def get_anim(self, i, **kwargs):
		if i == -1:
			return self.kwargs.get('introducer', Write)(self.expressions[0].mob)
		if i == len(self.expressions) - 1 and self.actions[-1] is None:
			return self.kwargs.get('remover', FadeOut)(self.expressions[-1].mob)
		from_expression = self.get_expression(i)
		to_expression = self.get_expression(i+1)
		action = self.get_action(i)
		return action.get_animation(**kwargs)(from_expression, to_expression)

	def play_animations(self, scene, i_range=None, wait_time=1, **kwargs):
		if i_range is None:
			i_range = range(len(self.actions))
		for i in i_range:
			scene.play(self.get_anim(i, **kwargs))
			scene.clear()
			scene.add(self.get_expression(i+1).mob)
			scene.wait(wait_time)

	def add_pair(self, expression, action):
		self.exp_act_pairs.append((expression, action))
	
	def __le__(self, other):
		from ..expressions.expression_core import SmartExpression
		if isinstance(other, SmartExpression):
			exp = other
			for action in self.actions:
				exp = action.get_output_expression(exp)
			return exp
		elif isinstance(other, Zipper):
			return other.expressions[-1] >= self
		else:
			return NotImplemented

	def __rshift__(self, other):
		other = Smarten(other)
		from ..expressions.expression_core import SmartExpression
		from ..actions.action_core import SmartAction
		if isinstance(other, SmartExpression):
			return Zipper(
				*self.exp_act_pairs,
				(other, None),
				**self.kwargs
			)
		elif isinstance(other, SmartAction):
			if self.actions[-1]:
				return Zipper(
					*self.exp_act_pairs,
					(None, other),
					**self.kwargs
				)
			else:
				return Zipper(
					*self.exp_act_pairs[:-1],
					(self.expressions[-1], other),
					**self.kwargs
				)
		elif isinstance(other, Zipper):
			if self.actions[-1] is None and other.expressions[0] is None:
				return Zipper(
					*self.exp_act_pairs[:-1],
					(self.expressions[-1], other.actions[0]),
					*other.exp_act_pairs[1:],
					**(other.kwargs | self.kwargs)
				)
			else:
				return Zipper(
					*self.exp_act_pairs,
					*other.exp_act_pairs,
					**(other.kwargs | self.kwargs)
				)
		else:
			return NotImplemented

	def __rrshift__(self, other):
		return Smarten(other).__rshift__(self)
	
	def __repr__(self):
		return f"Zipper({self.exp_act_pairs})"
	
	def __eq__(self, other):
		if isinstance(other, Zipper):
			return self.exp_act_pairs == other.exp_act_pairs and self.kwargs == other.kwargs
		else:
			return NotImplemented

