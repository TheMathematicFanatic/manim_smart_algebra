from MF_Tools.dual_compatibility import VGroup



class VStack(VGroup):
    def __init__(self, *exp_act_pairs, **kwargs):
        self.expressions = [pair[0] for pair in exp_act_pairs]
        self.actions = [pair[1] for pair in exp_act_pairs]
        super().__init__(**kwargs)
        if self.expressions[0] is not None:
            self.add(self.expressions[0])

    def play_anim(self)
