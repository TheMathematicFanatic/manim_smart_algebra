from ..expressions import expression_core
from ..actions import action_core

_ = None

class Zipper(VGroup):
    def __init__(self, *exp_act_pairs, **kwargs):
        super().__init__(**kwargs)
        self.expressions = [pair[0] for pair in exp_act_pairs]
        self.actions = [pair[1] for pair in exp_act_pairs]

    def get_expression(self, i):
        expression = self.expressions[i]
        if expression is None:
            expression = self.expressions[i-1] >= self.actions[i-1]
            self.expressions[i] = expression
        return expression

    def get_action(self, i):
        action = self.actions[i]
        if action is None:
            action = self.actions[i-1] <= self.expressions[i-1]
            #hmmm what should this be?
            self.actions[i] = action
        return action

    def get_anim(self, i, **kwargs):
        expression = self.get_expression(i)
        action = self.get_action(i)
        if action is None:
            return ReplacementTransform(self.expressions[i], expression, **kwargs)
        return action.get_animation(expression, **kwargs)

    def add_pair(self, expression, action):
        self.expressions.append(expression)
        self.actions.append(action)

    def __rshift__(self, other):
        if isinstance(other, action_core.SmartAction):
            if self.actions[-1] is None:
                self.actions[-1] = other
            else:
                self.add_pair(None, other)
        elif isinstance(other, expression_core.SmartExpression):
            self.add_pair(other, None)
        elif isinstance(other, Zipper):
            return Zipper(*zip(self.expressions, self.actions), *zip(other.expressions, other.actions))
        else:
            raise ValueError("Can only use >> with other Zipper or SmartAction or SmartExpression")
        return self

    def __rrshift__(self, other):
        if isinstance(other, expression_core.SmartExpression):
            if self.expressions[-1] is None:
                self.expressions[-1] = other
            else:
                self.add_pair(other, None)
        elif isinstance(other, action_core.SmartAction):
            self.add_pair(None, other)
        elif isinstance(other, Zipper):
            return Zipper(*zip(other.expressions, other.actions), *zip(self.expressions, self.actions))
        else:
            raise ValueError("Can only use >> with other Zipper or SmartAction or SmartExpression")
        return self

    def get_animation(self, i, **kwargs):
        if i == -1:
            return Write(self.expressions[0])
        if i == len(self.expressions) - 1 and self.actions[-1] is None:
            return FadeOut(self.expressions[-1])
        action = self.get_action(i)
        action.input_expression = self.get_expression(i)
        action.output_expression = self.get_expression(i+1)
        return action.get_animation(**kwargs)

    def play_animations(self, scene, i_range, wait_time=1, **kwargs):
        for i in i_range:
            scene.play(self.get_animation(i, **kwargs))
            scene.clear()
            scene.add(self.get_expression(i+1))
            scene.wait(wait_time)