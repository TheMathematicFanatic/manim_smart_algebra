# actions.py
from manim import *
from .expressions import *
from .utils import *


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

    get_animations then simply parses this glyphmap list to create a list of
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
        preaddress="",
        introducer=Write,
        remover=FadeOut,
    ):
        self.input_expression = None
        self.output_expression = None
        self.addressmap = None
        self.glyphmap = None
        self.animations = None
        self.preaddress = preaddress
        self.introducer = introducer
        self.remover = remover

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
                A.get_glyph_indices(entry[0]) if isinstance(entry[0], (str, list)) else entry[0],
                B.get_glyph_indices(entry[1]) if isinstance(entry[1], (str, list)) else entry[1]
            ]
            if len(entry) == 3:
                glyphmap_entry.append(entry[2])
            glyphmap.append(glyphmap_entry)
            if A.get_subex(entry[0]).parentheses and not B.get_subex(entry[1]).parentheses:
                glyphmap.append([A.get_glyph_indices(entry[0]+"()"), self.remover, {"rate_func":rate_functions.rush_from}])
            elif not A.get_subex(entry[0]).parentheses and B.get_subex(entry[1]).parentheses:
                glyphmap.append([self.introducer, B.get_glyph_indices(entry[1]+"()"), {"rate_func":rate_functions.rush_from}])
        self.glyphmap = glyphmap
        return glyphmap
    
    def get_animations(self):
        if self.glyphmap is None:
            self.get_glyphmap()
        A = self.input_expression
        B = self.output_expression
        animations = []
        active_in_glyphs = set()
        active_out_glyphs = set()
        def A_vgroup(glyph_list):
            V = VGroup()
            for g in glyph_list:
                if g in active_in_glyphs: V.add(A[0][g].copy())
                else: V.add(A[0][g])
            return V
        def B_vgroup(glyph_list):
            V = VGroup()
            for g in glyph_list:
                V.add(B[0][g])
            return V
        for entry in self.glyphmap:
            if len(entry) == 3: anim_kwargs = entry[2]
            else: anim_kwargs = {}
            if isinstance(entry[0], list) and isinstance(entry[1], list):
                animations.append(
                    ReplacementTransform(A_vgroup(entry[0]), B_vgroup(entry[1]), **anim_kwargs)
                )
                active_in_glyphs.update(entry[0])
                active_out_glyphs.update(entry[1])
            elif isinstance(entry[0], list) and isinstance(entry[1], Animation):
                animations.append(
                    entry[1](A_vgroup(entry[0]), **anim_kwargs)
                )
                active_in_glyphs.update(entry[0])
            elif isinstance(entry[0], Animation) and isinstance(entry[1], list):
                animations.append(
                    entry[0](B_vgroup(entry[1]), **anim_kwargs)
                )
                active_out_glyphs.update(entry[1])
            else:
                assert False, f"Invalid glyphmap entry: {entry}"
        inactive_in_glyphs = set(range(len(A))) - active_in_glyphs
        inactive_out_glyphs = set(range(len(B))) - active_out_glyphs
        assert len(inactive_in_glyphs) == len(inactive_out_glyphs), f"Inactive glyphs have mismatched lengths. \n {inactive_in_glyphs} \n {inactive_out_glyphs}"
        for i,j in zip(inactive_in_glyphs, inactive_out_glyphs):
            animations.append(
                ReplacementTransform(A[0][i], B[0][j])
            )
        self.animations = animations
        return animations


def preaddressfunc(func):
	def wrapper(action, expr=None, *args, **kwargs):
		address = action.preaddress
		if expr is None: expr = action.input_expression
		if len(address)==0:
			action.output_expression = func(action, expr, *args, **kwargs)
		else:
			active_part = expr.copy().get_subex(address)
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
            







class SwapChildren(SmartAction):
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


