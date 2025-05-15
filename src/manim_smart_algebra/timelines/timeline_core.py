from ..expressions import *
from ..actions import *
from MF_Tools.dual_compatibility import TransformMatchingShapes


class SmartTimeline:
    """
    A class that represents a timeline of expressions and actions.
    """
    def __init__(self, **kwargs):
        self.steps = [] # Elements of this list are of the form [expression, action]
        self.current_exp_index = 0
        self.auto_fill = False
    
    def get_expression(self, index: int) -> SmartExpression:
        try:
            return self.steps[index][0]
        except IndexError:
            return None
    
    def set_expression(self, index: int, expression: SmartExpression):
        if index == len(self.steps):
            self.add_expression_to_end(expression)
        self.steps[index][0] = expression

    def add_expression_to_start(self, expression: SmartExpression):
        if len(self.steps) == 0 or self.steps[0][0] is not None:
            self.steps.insert(0, [None, None])
        self.set_expression(0, expression)
        if self.auto_fill:
            self.propagate()
        return self

    def add_expression_to_end(self, expression: SmartExpression):
        self.steps.append([None, None])
        self.set_expression(-1, expression)
        return self
    
    def get_action(self, index: int) -> SmartAction:
        try:
            return self.steps[index][1]
        except IndexError:
            return None

    def set_action(self, index: int, action: SmartAction):
        self.steps[index][1] = action
    
    def add_action_to_start(self, action: SmartAction):
        self.set_action(0, action)
        return self
    
    def add_action_to_end(self, action: SmartAction):
        if len(self.steps) == 0 or self.steps[-1][1] is not None:
            self.steps.append([None, None])
        self.set_action(-1,action)
        if self.auto_fill:
            self.propagate()
        return self
    
    def propagate(self, start_at=0):
        for i in range(start_at, len(self.steps) - 1):
            exp, act = self.steps[i]
            next_exp = self.steps[i+1][0]
            if exp != None and act != None and next_exp == None:
                self.set_expression(i+1, act.get_output_expression(exp))
        exp, act = self.steps[-1]
        if exp != None and act != None:
            try:
                self.add_expression_to_end(act.get_output_expression(exp))
            except NotImplementedError:
                pass
    
    def play_animation(self, scene, index, **kwargs):
        action = self.get_action(index)
        expA = self.get_expression(index)
        expB = self.get_expression(index+1)
        if action:
            animation = action.get_animation()(expA, expB, **kwargs)
        else:
            animation = TransformMatchingShapes(expA.mob, expB.mob, **kwargs)
        scene.play(animation)
        self.current_exp_index = index+1
    
    def play_next(self, scene):
        self.play_animation(scene, index=self.current_exp_index)

    def play_range(self, scene, start_index, end_index, wait_between=1, **kwargs):
        for i in range(start_index, end_index):
            self.play_animation(scene, index=i, **kwargs)
            self.wait(wait_between)
    
    def play_all(self, scene):
        self.current_exp_index = 0
        while self.current_exp_index < len(self.steps)-1:
            self.play_next(scene=scene)
    
    def __rshift__(self, other):
        if isinstance(other, SmartExpression):
            self.add_expression_to_end(other)
            return self
        elif isinstance(other, SmartAction):
            self.add_action_to_end(other)
            return self
        elif isinstance(other, SmartTimeline):
            raise NotImplementedError("TODO")
        else:
            raise ValueError('SmartTimeline can only be combined via >> with a SmartExpression, SmartAction, or another SmartTimeline')
    
    def __rrshift__(self, other):
        if isinstance(other, SmartExpression):
            return self.add_expression_to_start(other)
        elif isinstance(other, SmartAction):
            return self.add_action_to_start(other)
        elif isinstance(other, SmartTimeline):
            raise NotImplementedError("TODO")
        else:
            raise ValueError('SmartTimeline can only be combined via >> with a SmartExpression, SmartAction, or another SmartTimeline')
        
    def __repr__(self):
        return f"SmartTimeline({self.steps})"

    def get_vgroup(self, **kwargs):
        return VGroup(*[self.steps[i][0].mob for i in range(len(self.steps))])
    
    @property
    def mob(self):
        return self.steps[self.current_exp_index][0].mob
    


class AutoTimeline(SmartTimeline):
    def __init__(self, auto_fill=True, auto_color={}, **kwargs):
        super().__init__(**kwargs)
        self.auto_fill = auto_fill
        self.auto_color = auto_color
    
    def set_expression(self, index: int, expression: SmartExpression):
        super().set_expression(index, expression)
        expression.set_color_by_subex(self.auto_color)
        if self.auto_fill and self.get_action(index) is None:
            next_action = self.decide_next_action(index)
            if next_action is not None:
                self.set_action(index, next_action)
        return self
    
    def set_action(self, index: int, action: SmartAction):
        super().set_action(index, action)
        if self.auto_fill and self.get_expression(index+1) is None:
            next_expression = action.get_output_expression(self.get_expression(index))
            self.set_expression(index+1, next_expression)
        return self
    
    def decide_next_action(self, index: int) -> SmartAction:
        # Implement in subclasses. Return None if finished.
        return None
    
    
    
    


