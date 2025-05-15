from .action_core import *
from MF_Tools.dual_compatibility import AnimationGroup
from MF_Tools import TransformByGlyphMap


class AlgebraicAction(Action):
    def __init__(self, template1, template2, var_kwarg_dict={}, **kwargs):
        super().__init__(**kwargs)
        self.template1 = template1
        self.template2 = template2
        self.var_kwarg_dict = var_kwarg_dict #{a:{"path_arc":PI}}
    
    def get_output_expression(self, input_expression=None):
        var_dict = match_expressions(self.template1, input_expression)
        return self.template2.substitute(var_dict)
    
    def get_addressmap(self, input_expression=None):
        addressmap = []
        def get_var_ad_dict(template):
            template_leaves = {
                template.get_subex(ad)
                for ad in input_expression.get_all_leaf_addresses()
                }
            from ..expressions.variables import Variable
            variables = [var for var in template_leaves if isinstance(var, Variable)]
            return {var: template.get_addresses_of_subex(var) for var in variables}
        self.template1_address_dict = get_var_ad_dict(self.template1)
        self.template2_address_dict = get_var_ad_dict(self.template2)
        variables = self.template1_address_dict.keys() | self.template2_address_dict.keys()
        for var in variables:
            kwargs = self.var_kwarg_dict.get(var, {})
            if len(self.template1_address_dict[var]) == 1:
                addressmap += [[self.template1_address_dict[var][0], t2ad, kwargs] for t2ad in self.template2_address_dict[var]]
            elif len(self.template2_address_dict[var]) == 1:
                addressmap += [[t1ad, self.template2_address_dict[var][0], kwargs] for t1ad in self.template1_address_dict[var]]
            else:
                raise ValueError("I don't know what to do when a variable appears more than once on both sides. Please set addressmap manually.")
        return addressmap


class AddressMapAction(Action):
    def __init__(self, *address_map, extra_animations=[], **kwargs):
        super().__init__(**kwargs)
        self.address_map = address_map
        self.extra_animations = extra_animations
    
    def get_animation(self, **kwargs):
        def animation(input_exp, output_exp=None):
            if output_exp is None:
                output_exp = self.get_output_expression(input_exp)
            return AnimationGroup(
                TransformByAddressMap(
                    input_exp,
                    output_exp,
                    *self.address_map,
                    **kwargs
                ),
                *self.extra_animations
            )
        return animation


class GlyphMapAction(Action):
    def __init__(self, *glyph_map, extra_animations=[], show_indices=False, **kwargs):
        super().__init__(**kwargs)
        self.glyph_map = glyph_map
        self.extra_animations = extra_animations
        self.show_indices = show_indices
    
    def get_animation(self, **kwargs):
        def animation(input_exp, output_exp=None):
            if output_exp is None:
                output_exp = self.get_output_expression(input_exp)
            return AnimationGroup(
                TransformByGlyphMap(
                    input_exp.mob,
                    output_exp.mob,
                    *self.glyph_map,
                    show_indices = self.show_indices,
                    **kwargs
                ),
                *self.extra_animations
            )
        return animation


class AnimationAction(Action):
    def __init__(self, animation, **kwargs):
        super().__init__(**kwargs)
        self.animation = animation # callable on two mobjects
    
    def get_animation(self, **kwargs):
        def animation(self, input_exp, output_exp=None):
            if output_exp is None:
                output_exp = self.get_output_expression(input_exp)
            return self.animation(input_exp.mob, output_exp.mob, **kwargs)
        return animation
