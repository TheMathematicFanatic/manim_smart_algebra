from ..expressions.expression_core import *
from ..actions.action_core import *


"""
A VStack is going to be a VGroup of SmartExpressions.
It will have its usual list of submobjects which will all be SmartExpressions.
It will also have a list of SmartActions which will be the transitions between them.
So for example, you could start it off with a single expression, and give it a bunch of
actions to apply, and it will then generate the entire list of expressions based on that.
Let's say the action list can also contain just Animations between the corresponding expressions,
or even glyphmaps.
"""

class VStack(VGroup):
    def __init__(self, expression, actions, color_dict={}, scale=1.5, **kwargs):
        if isinstance(expression, SmartExpression):
            expressions = [expression]
        elif isinstance(expressions, (list, tuple)):
            expressions = list(expression)

        if isinstance(actions, SmartAction):
            actions = [actions]
        elif isinstance(actions, (list, tuple)):
            actions = list(actions)
        
        super().__init__(*expressions, **kwargs)
        self.actions = actions
        self.generate_expressions()
        for exp in self.submobjects:
            exp.scale(scale)
            exp.set_color_by_subex(color_dict)

    def generate_expressions(self):
        for i in range(len(self.submobjects) - 1, len(self.actions)):
            self.actions[i].input_expression = self.submobjects[i]
            self.add(self.actions[i].get_output_expression(self.submobjects[i]))
    
    def get_anim(self, i, **kwargs):
        if isinstance(self.actions[i], SmartAction):
            return self.actions[i].get_animation(**kwargs)
        elif isinstance(self.actions[i], Animation):
            return self.actions[i]
        elif isinstance(self.actions[i], (list, tuple)):
            return TransformByGlyphMap(
                self.submobjects[i], self.submobjects[i+1],
                *self.actions[i],
                **kwargs
            )
        else:
            raise ValueError(f"Action {i}: is not a SmartAction or Animation or glyphmap (list, tuple): {self.actions[i]}")
    
    def play_actions(self, scene):
        scene.play(Write(self.submobjects[0]))
        scene.wait()
        for i in range(len(self.actions)):
            scene.play(self.get_anim(i))
            scene.clear()
            scene.add(self.submobjects[i+1])
            scene.wait()
        scene.wait()
    
    