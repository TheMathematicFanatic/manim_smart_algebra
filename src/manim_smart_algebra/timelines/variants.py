from .timeline_core import *


class AutoTimeline(SmartTimeline):
    def __init__(self, auto_fill=True, **kwargs):
        super().__init__(**kwargs)
        self.auto_fill = auto_fill
    
    def set_expression(self, index: int, expression: SmartExpression):
        super().set_expression(index, expression)
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


from MF_Tools.dual_compatibility import UP, smooth
class ShowStepsTimeline(SmartTimeline):
    def __init__(self, past_steps_shift_vector=1.5*UP, past_steps_opacity=0.4, shift_run_time=0.75, shift_rate_func=smooth, **kwargs):
        super().__init__(**kwargs)
        self.past_steps_vgroup = VGroup()
        self.past_steps_shift_vector = past_steps_shift_vector
        self.past_steps_opacity = past_steps_opacity
        self.shift_run_time = shift_run_time
        self.shift_rate_func = shift_rate_func
    
    def play_animation(self, scene, index, **kwargs):
        self.past_steps_vgroup.add(
            self.mob.copy().set_opacity(0.25)
        )
        scene.add(self.past_steps_vgroup)
        scene.play(
            self.past_steps_vgroup.animate.shift(self.past_steps_shift_vector),
            run_time = self.shift_run_time,
            rate_func = self.shift_rate_func
        )
        super().play_animation(scene, index, **kwargs)


        


