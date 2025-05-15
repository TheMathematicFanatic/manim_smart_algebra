from ..expressions import *
from ..actions import *
from MF_Tools.dual_compatibility import TransformMatchingShapes, UP, smooth


class Timeline:
    """
    A class that represents a timeline of expressions and actions.
    """
    def __init__(
        self,
        auto_color = {},
        auto_propagate = True,
        show_past_steps = False,
        past_steps_opacity = 0.4,
        past_steps_direction = UP,
        past_steps_buff = 1,
        past_steps_shift_run_time = 1,
        past_steps_shift_rate_func = smooth
    ):
        self.steps = [] # Elements of this list are of the form [expression, action]
        self.current_exp_index = 0
        self.auto_color = auto_color
        self.auto_propagate = auto_propagate
        self.show_past_steps = show_past_steps
        if self.show_past_steps:
            self.past_steps_vgroup = VGroup()
            self.past_steps_opacity = past_steps_opacity
            self.past_steps_direction = past_steps_direction
            self.past_steps_buff = past_steps_buff
            self.shift_run_time = past_steps_shift_run_time
            self.shift_rate_func = past_steps_shift_rate_func

    def get_expression(self, index: int) -> Expression:
        try:
            return self.steps[index][0]
        except IndexError:
            return None
    
    def set_expression(self, index: int, expression: Expression):
        if self.auto_color:
            expression.set_color_by_subex(self.auto_color)
        if index == len(self.steps):
            self.add_expression_to_end(expression)
        self.steps[index][0] = expression
        if self.auto_propagate:
            self.propagate(start_at=index)

    def add_expression_to_start(self, expression: Expression):
        if len(self.steps) == 0 or self.steps[0][0] is not None:
            self.steps.insert(0, [None, None])
        self.set_expression(0, expression)
        return self

    def add_expression_to_end(self, expression: Expression):
        self.steps.append([None, None])
        self.set_expression(-1, expression)
        return self
    
    def get_action(self, index: int) -> Action:
        try:
            return self.steps[index][1]
        except IndexError:
            return None

    def set_action(self, index: int, action: Action):
        self.steps[index][1] = action
        if self.auto_propagate:
            self.propagate(start_at=index)
    
    def add_action_to_start(self, action: Action):
        self.set_action(0, action)
        return self
    
    def add_action_to_end(self, action: Action):
        if len(self.steps) == 0 or self.steps[-1][1] is not None:
            self.steps.append([None, None])
        self.set_action(-1,action)
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
        if self.show_past_steps:
            self.shift_past_steps(scene, expA, expB)
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
    
    def shift_past_steps(self, scene, expA, expB):
        mobA_radius = expA.mob.get_critical_point(self.past_steps_direction) - expA.mob.get_center()
        mobB_radius = expB.mob.get_center() - expB.mob.get_critical_point(-self.past_steps_direction)
        shift_distance = np.linalg.norm(mobA_radius) + np.linalg.norm(mobB_radius) + self.past_steps_buff
        self.past_steps_vgroup.add(
            self.mob.copy().set_opacity(0.25)
        )
        scene.add(self.past_steps_vgroup)
        scene.play(
            self.past_steps_vgroup.animate.shift(shift_distance * self.past_steps_direction),
            run_time = self.shift_run_time,
            rate_func = self.shift_rate_func
        )
    
    def __rshift__(self, other):
        if isinstance(other, Expression):
            self.add_expression_to_end(other)
            return self
        elif isinstance(other, Action):
            self.add_action_to_end(other)
            return self
        elif isinstance(other, Timeline):
            raise NotImplementedError("TODO")
        else:
            raise ValueError('Timeline can only be combined via >> with a Expression, Action, or another Timeline')
    
    def __rrshift__(self, other):
        if isinstance(other, Expression):
            return self.add_expression_to_start(other)
        elif isinstance(other, Action):
            return self.add_action_to_start(other)
        elif isinstance(other, Timeline):
            raise NotImplementedError("TODO")
        else:
            raise ValueError('Timeline can only be combined via >> with a Expression, Action, or another Timeline')
        
    def __repr__(self):
        return f"Timeline({self.steps})"

    def get_vgroup(self, **kwargs):
        return VGroup(*[self.steps[i][0].mob for i in range(len(self.steps))])
    
    @property
    def mob(self):
        return self.steps[self.current_exp_index][0].mob
    


