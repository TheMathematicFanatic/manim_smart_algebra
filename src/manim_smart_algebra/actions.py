# actions.py
from manim import *
from .expressions import *
from .utils import *
from MF_Tools import TransformByGlyphMap


class SmartAction:
    """
        Transforms SmartExpressions into other SmartExpressions,
        both as static objects and also with an animation.

        An action is defined by two main things:
        the get_output_expression method, which controls how it acts on static expressions,
        and the get_addressmap method, which controls how it acts as an animation.
        Both set attributes of the corresponding name and return them.

        It may also have a preaddress parameter/attribute which will determine the subexpression
        address at which the action is applied, and a few other attributes which may adjust some
        specifics.

        self.input_expression is set to None during __init__. It is critical that actions
        can exist prior to being given expressions, so that they can be combined together.
        When an input expression is received, this attribute is set, and the method
        .get_output_expression is called, setting self.output_expression.
        This is all that is required for static actions, no animations.

        Now, to create the animation between these expressions:

        get_addressmap is also unique to each action, and returns something like
        [
            ["00", "01"],
            ["01", "00", {"path_arc":PI/2}],
            [FadeIn, "1"],
            ["1", FadeOut]
        ]
        which contains all the expression-agnostic information about the animation.
        Often this will simply define and return this list with no computation.

        get_glyphmap combines the input_expression, output_expression, and addressmap
        to create a list like
        [
            ([0,1,2], [5,6]),
            ([3,4,5], [1,2,3], {"path_arc":PI/2}),
            (FadeIn, [8,9]),
            ([6], FadeOut)
        ]
        which tells which glyphs of the mobjects to send to which others, and how.

        get_animation then simply parses this glyphmap list to create a list of
        animations, probably to be passed to AnimationGroup, like
        [
            ReplacementTransform(A[0][0,1,2], B[0][5,6]),
            ReplacementTransform(A[0][3,4,5], B[0][1,2,3], path_arc=PI/2),
            FadeIn(B[0][8,9]),
            FadeOut(A[0][6]),
            ...
        ]
        or something like that, the syntax is partially made up. The ... is
        ReplacementTransforms of all the individual glyphs not mentioned in the glyphmap,
        whose lengths have to exactly match.

        Broadly speaking, that's that!
    """
    def __init__(self,
        input_expression=None,
        output_expression=None,
        addressmap=None,
        glyphmap=None,
        animations=None,
        preaddress="",
        introducer=Write,
        remover=FadeOut,
        **kwargs
    ):
        self.input_expression = input_expression
        self.output_expression = output_expression
        self.addressmap = addressmap
        self.glyphmap = glyphmap
        self.animations = animations
        self.preaddress = preaddress
        self.introducer = introducer
        self.remover = remover
        self.kwargs = kwargs

    def get_output_expression(self, input_expression):
        pass # define in subclasses
        # always decorate with @preaddressfunc to allow preaddressing and set attribute
        # just return the output_expression

    def get_addressmap(self):
        pass # define in subclasses
        # always decorate with @preaddressfunc to allow preaddressing and set attribute
        # just return the addressmap

    def get_glyphmap(self):
        assert self.input_expression is not None
        if self.output_expression is None:
            self.get_output_expression()
        if self.addressmap is None:
            self.get_addressmap()
        A = self.input_expression
        B = self.output_expression
        glyphmap = []
        for entry in self.addressmap:
            assert len(entry) in [2, 3], f"Invalid addressmap entry: {entry}"
            glyphmap_entry = [
                A.get_glyphs(entry[0]) if isinstance(entry[0], (str, list)) else entry[0],
                B.get_glyphs(entry[1]) if isinstance(entry[1], (str, list)) else entry[1]
            ]
            if len(entry) == 3:
                glyphmap_entry.append(entry[2])
            glyphmap.append(glyphmap_entry)
            # Good idea but turning off for now, need to rethink
            # if isinstance(entry[0], (str, list)) and isinstance(entry[1], (str, list)):
            #     if A.get_subex(entry[0]).parentheses and not B.get_subex(entry[1]).parentheses:
            #         glyphmap.append([A.get_glyphs(entry[0]+"()"), self.remover, {"rate_func":rate_functions.rush_from}])
            #     elif not A.get_subex(entry[0]).parentheses and B.get_subex(entry[1]).parentheses:
            #         glyphmap.append([self.introducer, B.get_glyphs(entry[1]+"()"), {"rate_func":rate_functions.rush_from}])
        self.glyphmap = glyphmap
        return glyphmap
    
    def get_animation(self, **kwargs):
        if self.glyphmap is None:
            self.get_glyphmap()
        return TransformByGlyphMap(
            self.input_expression,
            self.output_expression,
            *self.glyphmap,
            default_introducer=self.introducer,
            default_remover=self.remover,
            **(self.kwargs|kwargs)
            )

    def __rshift__(self, other):
        if isinstance(other, SequentialAction):
            return SequentialAction(self, *other.actions)
        elif isinstance(other, SmartAction):
            return SequentialAction(self, other)
        else:
            return ValueError("Can only use >> with other SequentialAction or SmartAction")

    def __or__(self, other):
        if isinstance(other, ParallelAction):
            return ParallelAction(self, *other.actions)
        elif isinstance(other, SmartAction):
            return ParallelAction(self, other)
        else:
            return ValueError("Can only use | with other ParallelAction or SmartAction")
    
    def __ror__(self, other):
        if isinstance(other, ParallelAction):
            return ParallelAction(*other.actions, self)
        elif isinstance(other, SmartAction):
            return ParallelAction(other, self)
        else:
            return ValueError("Can only use | with other ParallelAction or SmartAction")

    def __lt__(self, other):
        self.input_expression = Smarten(other)
    
    def __le__(self, other):
        return self.get_output_expression(Smarten(other))


def preaddressfunc(func):
	def wrapper(action, expr=None, *args, **kwargs):
		address = action.preaddress
		if expr is None: expr = action.input_expression.copy()
		if len(address)==0:
			action.output_expression = func(action, expr, *args, **kwargs)
		else:
			active_part = expr.get_subex(address)
			result = func(action, active_part, *args, **kwargs)
			result_in_context = expr.substitute_at_address(result, address)
			action.output_expression = result_in_context
		return action.output_expression
	return wrapper

def preaddressmap(getmap):
	def wrapper(action, *args, **kwargs):
		addressmap = getmap(action, *args, **kwargs)
		if action.preaddress:
			for entry in addressmap:
				for i, ad in enumerate(entry):
					if isinstance(ad, (str, list)):
						entry[i] = action.preaddress + ad
		action.addressmap = addressmap
		return action.addressmap
	return wrapper



class AlgebraicAction(SmartAction):
    def __init__(self, template1, template2, var_kwarg_dict={}, **kwargs):
        super().__init__(**kwargs)
        self.template1 = template1
        self.template2 = template2
        self.var_kwarg_dict = var_kwarg_dict #{a:{"path_arc":PI}}
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        var_dict = match_expressions(self.template1, input_expression)
        return self.template2.substitute(var_dict)
    
    @preaddressmap
    def get_addressmap(self):
        addressmap = []
        def get_var_ad_dict(template):
            template_leaves = {
                template.get_subex(ad)
                for ad in self.input_expression.get_all_leaf_addresses()
                }
            variables = [var for var in template_leaves if isinstance(var, SmartVariable)]
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



class ParallelAction(SmartAction):
    def __init__(self, *actions, **kwargs):
        self.actions = actions
        super().__init__(**kwargs)
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        expr = input_expression
        for action in self.actions:
            expr = action.get_output_expression(expr)
        return expr
    
    @preaddressmap
    def get_addressmap(self):
        return sum([action.get_addressmap() for action in self.actions], [])
    
    def __or__(self, other):
        if isinstance(other, ParallelAction):
            return ParallelAction(*self.actions, *other.actions)
        elif isinstance(other, SmartAction):
            return ParallelAction(*self.actions, other)
        else:
            return ValueError("Can only use | with other ParallelAction or SmartAction")
    
    def __ror__(self, other):
        if isinstance(other, ParallelAction):
            return ParallelAction(*other.actions, *self.actions)
        elif isinstance(other, SmartAction):
            return ParallelAction(other, *self.actions)
        else:
            return ValueError("Can only use | with other ParallelAction or SmartAction")



class SequentialAction(SmartAction):
    def __init__(self, *actions, **kwargs):
        self.actions = list(actions)
        super().__init__(**kwargs)
    
    @preaddressfunc
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
        elif isinstance(other, SmartAction):
            return SequentialAction(*self.actions, other)
        else:
            return ValueError("Can only use >> with other SequentialAction or SmartAction")
    
    def __rrshift__(self, other):
        if isinstance(other, SequentialAction):
            return SequentialAction(*other.actions, *self.actions)
        elif isinstance(other, SmartAction):
            return SequentialAction(other, *self.actions)
        else:
            return ValueError("Can only use >> with other SequentialAction or SmartAction")
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.actions[key]
        elif isinstance(key, slice):
            return SequentialAction(*self.actions[key])

  



class swap_children_(SmartAction):
    def __init__(self, mode="arc", arc_size=0.75*PI, **kwargs):
        self.mode = mode
        self.arc_size = arc_size
        super().__init__(**kwargs)
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        assert len(input_expression.children) == 2, f"Cannot swap children of {input_expression}, must have two children."
        return type(input_expression)(input_expression.children[1], input_expression.children[0])

    @preaddressmap
    def get_addressmap(self):
        return [
            ["0", "1", {"path_arc": self.arc_size}],
            ["1", "0", {"path_arc": self.arc_size}]
        ]


class apply_operation_(SmartAction):
    def __init__(self, OpClass, other, side="right", introducer=Write, **kwargs):
        self.OpClass = OpClass
        self.other = Smarten(other)
        self.introducer = introducer
        self.side = side
        super().__init__(**kwargs)
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        if self.side == "right":
            output_expression = self.OpClass(input_expression, self.other)
        elif self.side == "left":
            output_expression = self.OpClass(self.other, input_expression)
        else:
            raise ValueError(f"Invalid side: {self.side}. Must be left or right.")
        return output_expression

    @preaddressmap
    def get_addressmap(self):
        if self.side == "right":
            return [
                ["", "0"],
                [self.introducer, "+", {"delay":0.5}],
                [self.introducer, "1", {"delay":0.6}]
            ]
        elif self.side == "left":
            return [
                ["", "1"],
                [self.introducer, "0", {"delay":0.5}],
                [self.introducer, "+", {"delay":0.6}]
            ]
        else:
            raise ValueError(f"Invalid side: {self.side}. Must be left or right.")

class add_(apply_operation_):
    def __init__(self, other, introducer=Write, **kwargs):
        super().__init__(SmartAdd, other, introducer=introducer, **kwargs)

class sub_(apply_operation_):
    def __init__(self, other, introducer=Write, **kwargs):
        super().__init__(SmartSub, other, introducer=introducer, **kwargs)

class mul_(apply_operation_):
    def __init__(self, other, introducer=Write, **kwargs):
        super().__init__(SmartMul, other, introducer=introducer, **kwargs)

class div_(apply_operation_):
    def __init__(self, other, introducer=Write, **kwargs):
        super().__init__(SmartDiv, other, introducer=introducer, **kwargs)

class pow_(apply_operation_):
    def __init__(self, other, introducer=Write, **kwargs):
        super().__init__(SmartPow, other, introducer=introducer, **kwargs)


class substitute_(SmartAction):
    def __init__(self, sub_dict, mode="transform", fade_shift=DOWN*0.2, lag=0, **kwargs):
        self.sub_dict = sub_dict
        self.mode = mode
        self.fade_shift = fade_shift
        self.lag = lag #usually looks like shit but can be cool sometimes
        super().__init__(**kwargs)
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        return input_expression.substitute(self.sub_dict)

    @preaddressmap
    def get_addressmap(self):
        target_addresses = []
        for var in self.sub_dict:
            target_addresses += self.input_expression.get_subex(self.preaddress).get_addresses_of_subex(var)
        addressmap = []
        if self.mode == "transform":
            for i,ad in enumerate(target_addresses):
                addressmap.append([ad, ad, {"delay": self.lag*i} | self.kwargs])
            return addressmap
        elif self.mode == "fade":
            for i,ad in enumerate(target_addresses):
                addressmap.append([ad, FadeOut, {"shift": self.fade_shift, "delay": self.lag*i} | self.kwargs])
                addressmap.append([FadeIn, ad, {"shift": self.fade_shift, "delay": self.lag*i} | self.kwargs])
            return addressmap


class evaluate_(SmartAction):
    def __init__(self, mode="random leaf", **kwargs):
        super().__init__(**kwargs)
        # if mode == "random leaf":
        #     leaf_addresses = input_expression.get_all_leaf_addresses()
        #     leaf_address = np.random.choice(leaves)
        #     self.preaddress = leaf_address

    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        return input_expression.evaluate()
    
    @preaddressmap
    def get_addressmap(self):
        return [
            ["", ""] #extension by preaddress is done by decorator!
        ]


class distribute_(SmartAction):
    # Not done yet, multilayer does not work... this is so necessary but rather nontrivial... hm...
    def __init__(self, mode="auto", multilayer=False, **kwargs):
        self.mode = mode #"auto", "left", "right"
        super().__init__(**kwargs)
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        if self.mode == "auto":
            self.determine_direction(input_expression)
        if self.mode == "left":
            new_children = [
                type(input_expression)(input_expression.children[0], child)
                for child in input_expression.children[-1].children
                ]
            return type(input_expression.children[-1])(*new_children)
        elif self.mode == "right":
            new_children = [
                type(input_expression)(child, input_expression.children[-1])
                for child in input_expression.children[0].children
                ]
            return type(input_expression.children[0])(*new_children)

    def determine_direction(self, input_expression):
        if self.mode == "auto":
            if isinstance(input_expression, SmartMul):
                left_distributable = isinstance(input_expression.children[-1], (SmartAdd, SmartSub))
                right_distributable = isinstance(input_expression.children[0], (SmartAdd, SmartSub))
                if left_distributable and right_distributable:
                    raise ValueError("Cannot auto-distribute if both sides are distributable, please set mode manually.")
                elif left_distributable:
                    self.mode = "left"
                elif right_distributable:
                    self.mode = "right"
                else:
                    raise ValueError("Cannot distribute, neither side is distributable.")
            elif isinstance(input_expression, SmartDiv):
                right_distributable = isinstance(input_expression.children[0], (SmartAdd, SmartSub))
                if right_distributable:
                    self.mode = "right"
                else:
                    raise ValueError("Cannot distribute, right side is not distributable.")
            elif isinstance(input_expression, SmartPow):
                right_distributable = isinstance(input_expression.children[0], (SmartMul, SmartDiv))
                if right_distributable:
                    self.mode = "right"
                else:
                    raise ValueError("Cannot distribute, right side is not distributable.")
            else:
                raise ValueError("Cannot auto-distribute, must be a multiplication or division.")

    @preaddressmap
    def get_addressmap(self):
        return [
            ["", ""] #standin idk what the fuck im doing here
        ]