from .action_core import *


class ParallelAction(Action):
    def __init__(self, *actions, **kwargs):
        self.actions = actions
        super().__init__(**kwargs)
    
    def get_output_expression(self, input_expression=None):
        expr = input_expression
        for action in self.actions:
            expr = action.get_output_expression(expr)
        return expr
    
    def get_addressmap(self, input_expression=None):
        return sum([action.get_addressmap(input_expression) for action in self.actions], [])
    
    def __or__(self, other):
        if isinstance(other, ParallelAction):
            return ParallelAction(*self.actions, *other.actions)
        elif isinstance(other, Action):
            return ParallelAction(*self.actions, other)
        else:
            raise ValueError("Can only use | with other ParallelAction or Action")
    
    def __ror__(self, other):
        if isinstance(other, Action):
            return ParallelAction(other, *self.actions)
        else:
            return NotImplemented



class SequentialAction(Action):
    def __init__(self, *actions, **kwargs):
        self.actions = list(actions)
        super().__init__(**kwargs)
    
    def get_output_expression(self, input_expression=None):
        expr = input_expression
        for action in self.actions:
            expr = action.get_output_expression(expr)
        return expr

    def get_animations(self):
        return [action.get_animation() for action in self.actions]
    
    def get_animation(self, i):
        return self.actions[i].get_animation()
        
    def __rshift__(self, other):
        if isinstance(other, SequentialAction):
            return SequentialAction(*self.actions, *other.actions)
        elif isinstance(other, Action):
            return SequentialAction(*self.actions, other)
        else:
            return ValueError("Can only use >> with other SequentialAction or Action")
    
    def __rrshift__(self, other):
        if isinstance(other, SequentialAction):
            return SequentialAction(*other.actions, *self.actions)
        elif isinstance(other, Action):
            return SequentialAction(other, *self.actions)
        else:
            return ValueError("Can only use >> with other SequentialAction or Action")
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.actions[key]
        elif isinstance(key, slice):
            return SequentialAction(*self.actions[key])

