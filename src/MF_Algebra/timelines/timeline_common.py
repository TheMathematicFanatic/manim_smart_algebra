from .timeline_core import *
from .timeline_variants import *
from ..actions.action_common import evaluate_

class Evaluate(AutoTimeline):
    def __init__(self, first_expression=None, mode="one at a time", number_mode="float", **kwargs):
        self.mode = mode
        self.number_mode = number_mode
        super().__init__(**kwargs)
        if first_expression is not None:
            self.add_expression_to_start(first_expression)

    def decide_next_action(self, index: int):
        last_exp = self.get_expression(index)
        leaves = last_exp.get_all_leaf_addresses()
        if leaves == ['']:
            return None
        leaves.sort(key=len, reverse=True)
        for leaf in leaves:
            try:
                twig = leaf[:-1]
                action = evaluate_(preaddress=twig)
                action.get_output_expression(last_exp)
                return action
            except ValueError:
                # This should mean that a subexpression cannot be computed due to the presence of a variable.
                # Perhaps we should make a custom Exception class for this so as not to accidentally catch others.
                pass
        return None