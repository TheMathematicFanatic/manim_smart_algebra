# SmartAction.py
from manim import *
from SmartExpression import *
from Utilities import *
"""
Okay I have some ideas about how to make a class that sits above the SmartExpressions.
Without a mobject, they can be customized on how exactly they will transform
the hypothetical mobject, and they can be chained together with a method or
overloaded operation. I'm thinking @ or >>. But then when they receive a expression
as an input, they become an animation. So one could do, say

class SimplifyLinear(Scene):
    def construct(self):
        A = 3*(x+4) - 5*(3+x)
        total_transform = distribute("0") >> distribute("1") >> combine_like_terms()
        self.play(total_transform(A))

where distribute and combine_like_terms are members of this class. Here they have been
chained together, where the three members combine amongst themselves to make another member
of this class, and the compound object is applied to A which returns an aniamtion to give to play.

So they need to have methods to:
    - generate the target expression from the input, which only gets called when the
      mobject attribute is filled
    - generate the animation to be passed to play
    - combine into the compound version

and they need to have attributes for:
    - the input expression
    - the target expression
    - the address(es?) within the input at which to apply the transformation
    - the addressmap/glyphmap, timeline, patharc and other kwargs which control the animation.
      or, perhaps these should be generated by the generate animation method?
    - algebra? makes sense for transformations describable in terms of algebra, like A --> A/1.
      the algebra could in theory be used to generate the target expression and addressmap,
      but in many cases it would be better to devise the generate the target expression method by hand.

The animation is definitely the hardest part. For now I am just going to implement them as only being able to
act in discrete steps on expression objects.
It feels like some to all of these objects should be somehow "reversible"? Clearly so if described in algebra, but idk
how this could be done if described in some other programmatic way.
"""

class SmartAction:
    def __init__(self, input_expression=None, address="", algebra=None):
        self.input_expression = input_expression
        self.output_expression = None
        self.address = address
        self.algebra = algebra
        if input_expression is not None:
            self.accept_input(input_expression)

    def accept_input(self, input_expression):
        self.input_expression = input_expression
        self.output_expression = self.generate_output_expression(input_expression)
        #self.output_expression.replace(self.input_expression)

    def generate_output_expression(self):
        ... # should be defined in subclasses

    def generate_animation(self):
        # Combines the input expression with the
        assert self.input_expression is not None, "Cannot generate animation without input expression."
        address_map = self.generate_address_map()
        print(address_map)
        pre = self.address
        anims = []

        # Handling Active Areas
        active_in_glyphs=[]
        active_out_glyphs=[]
        for entry in address_map:
            if len(entry) == 3:
                kwargs = entry[2]
            elif len(entry) == 2:
                kwargs = {}
            else:
                assert len(entry) == 2, "address_map entry must have 2 or 3 elements"
            if type(entry[0]) == type and issubclass(entry[0], Animation):
                # Example: [Write, "10"]
                target_out_glyphs = self.output_expression.get_vgroup_from_address(pre+entry[1], copy_if_in_list=active_out_glyphs)
                anims.append(entry[0](target_out_glyphs, **kwargs))
                active_out_glyphs += self.output_expression.get_glyph_indices_at_address(pre+entry[1], return_mode=list)
            elif type(entry[1]) == type and issubclass(entry[1], Animation):
                # Example: ["1", FadeOut, {"shift":DOWN}]
                target_in_glyphs = self.input_expression.get_vgroup_from_address(pre+entry[0], copy_if_in_list=active_in_glyphs)
                anims.append(entry[1](target_in_glyphs, **kwargs))
                active_in_glyphs += self.input_expression.get_glyph_indices_at_address(pre+entry[0], return_mode=list)
            else:
                # Example: ["0", "02", {"path_arc":PI/2}]
                target_in_glyphs = self.input_expression.get_vgroup_from_address(pre+entry[0], copy_if_in_list=active_in_glyphs)
                target_out_glyphs = self.output_expression.get_vgroup_from_address(pre+entry[1], copy_if_in_list=active_out_glyphs)
                anims.append(Transform(target_in_glyphs, target_out_glyphs, **kwargs))
                active_in_glyphs += self.input_expression.get_glyph_indices_at_address(pre+entry[0], return_mode=list)
                active_out_glyphs += self.output_expression.get_glyph_indices_at_address(pre+entry[1], return_mode=list)

        # Removing duplicates from active glyphs
        active_in_glyphs = list(set(active_in_glyphs))
        active_out_glyphs = list(set(active_out_glyphs))
        # Creating lists of inactive glyphs
        inactive_in_glyphs = [g for g in range(len(self.input_expression)) if g not in active_in_glyphs]
        inactive_out_glyphs = [g for g in range(len(self.output_expression)) if g not in active_out_glyphs]
        #debug print all four glyph lists
        print("Active in glyphs:", active_in_glyphs)
        print("Active out glyphs:", active_out_glyphs)
        print("Inactive in glyphs:", inactive_in_glyphs)
        print("Inactive out glyphs:", inactive_out_glyphs)
        if len(inactive_in_glyphs) == len(inactive_out_glyphs):
            for x, y in zip(inactive_in_glyphs, inactive_out_glyphs):
                anims.append(Transform(self.input_expression[0][x], self.output_expression[0][y]))
        else:
            print("WARNING: Inactive areas not handled correctly!")
            anims.append(TransformMatchingShapes(
                VGroup(*[self.input_expression[0][i] for i in inactive_in_glyphs]),
                VGroup(*[self.output_expression[0][i] for i in inactive_out_glyphs])
            ))
        print(anims)
        return anims

    def generate_address_map(self):
        ... # should be defined in subclasses

    def __call__(self, input_expression, **kwargs):
        assert isinstance(input_expression, SmartExpression)
        self.accept_input(input_expression)
        animations = self.generate_animation()
        return AnimationGroup(*animations, **kwargs)

    def __rshift__(self, other):
        return SequentialAction(self, other)

    def __rrshift__(self, other):
        if isinstance(other, SmartAction):
            return SequentialAction(other, self)
        elif isinstance(other, SmartExpression):
            self.accept_input(other)
            return self.output_expression

    def __add__(self, other):
        return ParallelAction(self, other)

    def __radd__(self, other):
        return ParallelAction(other, self)


class SequentialAction(SmartAction):
    def __init__(self, *children, **kwargs):
        assert all(isinstance(child, SmartAction) for child in children)
        self.children = []
        for child in children:
            if isinstance(child, SequentialAction):
                for grandchild in child.children:
                    self.children.append(grandchild)
            else:
                self.children.append(child)
        super().__init__(**kwargs)
        if self.children[0].input_expression is not None:
            self.accept_input(self.children[0].input_expression)

    def generate_output_expression(self, expression):
        # Don't need to set self.output_expression here, it's done in accept_input
        for child in self.children:
            child.accept_input(expression)
            expression = child.output_expression
        return expression

    def generate_address_map(self):
        pass # Yeah this is the hard part

class ParallelAction(SmartAction):
    def __init__(self, *children, **kwargs):
        assert all(isinstance(child, SmartAction) for child in children)
        self.children = children
        super().__init__(**kwargs)
        if any(child.input_expression is not None for child in children):
            self.accept_input(self.children[0].input_expression)

    def generate_output_expression(self):
        # Don't need to set self.output_expression here, it's done in accept_input
        expression = self.input_expression
        for child in self.children:
            child.accept_input(expression)
            expression = child.output_expression
        return expression

    def generate_address_map(self):
        pass

class ApplyOperation(SmartAction):
    def __init__(self, OpClass, other, mode="fade", side="right", **kwargs):
        self.OpClass = OpClass
        self.other = Smarten(other)
        self.mode = mode
        self.side = side
        super().__init__(**kwargs)

    @preaddress
    def generate_output_expression(self, input_expression):
        if self.side == "right":
            output_expression = self.OpClass(input_expression, self.other)
        elif self.side == "left":
            output_expression = self.OpClass(self.other, input_expression)
        else:
            raise ValueError(f"Invalid side: {self.side}. Must be left or right.")
        return output_expression

    def generate_address_map(self):
        new_side = "1" if self.mode == "right" else "0"
        if self.mode=="fade":
            address_map = (
                [FadeIn, "_"],
                [FadeIn, new_side]
            )
        elif self.mode=="shift":
            address_map = (
                [FadeIn, "_", {"shift":DOWN}],
                [FadeIn, new_side, {"shift":DOWN}]
            )
        elif self.mode=="write":
            address_map = (
                [Write, "_"],
                [Write, new_side]
            )
        return address_map

class add_(ApplyOperation):
    def __init__(self, other, **kwargs):
        super().__init__(SmartAdd, other, **kwargs)

class sub_(ApplyOperation):
    def __init__(self, other, **kwargs):
        super().__init__(SmartSub, other, **kwargs)

class mul_(ApplyOperation):
    def __init__(self, other, **kwargs):
        super().__init__(SmartMul, other, **kwargs)

class div_(ApplyOperation):
    def __init__(self, other, **kwargs):
        super().__init__(SmartDiv, other, **kwargs)

class pow_(ApplyOperation):
    def __init__(self, other, **kwargs):
        super().__init__(SmartPow, other, **kwargs)


class substitute_(SmartAction):
    def __init__(self, expression_dict, mode="dial", **kwargs):
        self.expression_dict = expression_dict
        self.mode = mode
        super().__init__(**kwargs)

    @preaddress
    def generate_output_expression(self, input_expression):
        return input_expression.substitute_expressions(self.expression_dict)

    def generate_address_map(self):
        address_map = ()
        for old_subex, new_subex in self.expression_dict.items():
            addresses = self.input_expression.get_addresses_of_subex(old_subex)
            for address in addresses:
                if self.mode == "dial":
                    address_map += (
                        [address, FadeOut, {"shift":DOWN}],
                        [FadeIn, address, {"shift":DOWN}],
                    )
                elif self.mode == "transform":
                    address_map += (
                        [address, address],
                    )
        return address_map

class distribute_(SmartAction):
    def __init__(self, side="left", mode="copy_arc", arc_size=PI/2, **kwargs):
        self.side = side
        assert side in ["left", "right"], f"Invalid side: {side}. Must be left or right."
        self.mode = mode
        self.arc_size = arc_size
        super().__init__(**kwargs)

    def generate_output_expression(self, input_expression):
        parent_type = type(input_expression)
        if self.side == "left":
            child_type = type(input_expression.children[1])
            assert parent_type in [SmartMul] and child_type in [SmartAdd, SmartSub], f"{parent_type} cannot be left-distributed over {child_type} in object {input_expression}"
            num_children = len(input_expression.children[1].children)
            return child_type(*[parent_type(input_expression.children[0],input_expression.children[1].children[i]) for i in range(num_children)])
        elif self.side == "right":
            child_type = type(input_expression.children[0])
            assert (parent_type in [SmartMul, SmartDiv] and child_type in [SmartAdd, SmartSub]) or (parent_type in [SmartPow] and child_type in [SmartMul, SmartDiv]), f"{parent_type} cannot be right-distributed over {child_type} in object {input_expression}"
            num_children = len(input_expression.children[0].children)
            return child_type(*[parent_type(input_expression.children[0].children[i],input_expression.children[1]) for i in range(num_children)])

    def generate_address_map(self):
        mul_side, sum_side = ("0", "1") if self.side == "left" else ("1", "0")
        address_map = ()
        for i in range(len(self.input_expression.children[int(sum_side)].children)):
            address_map += (
                [mul_side, str(i)+mul_side, {"path_arc": self.arc_size}],
                #["_", str(i)+"_"]
            )
        return address_map


class swap_children_(SmartAction):
    def __init__(self, mode="arc", arc_size=0.75*PI, **kwargs):
        self.mode = mode
        self.arc_size = arc_size
        super().__init__(**kwargs)

    @preaddress
    def generate_output_expression(self, input_expression: SmartExpression):
        return type(input_expression)(input_expression.children[1], input_expression.children[0])

    def generate_address_map(self):
        if self.mode == "arc":
            return (
                ["0", "1", {"path_arc": self.arc_size}],
                ["1", "0", {"path_arc": self.arc_size}]
            )
        else:
            raise ValueError(f"Invalid mode: {self.mode}.")


class evaluate_(SmartAction):
    def __init__(self, mode="transform", **kwargs):
        self.mode = mode
        super().__init__(**kwargs)

    @preaddress
    def generate_output_expression(self, input_expression: SmartExpression):
        if isinstance(input_expression, SmartNumber):
            return input_expression
        elif all(isinstance(child, SmartInteger) for child in input_expression.children):
            if isinstance(input_expression, SmartOperation):
                result = input_expression.children[0].n
                for i in range(1, len(input_expression.children)):
                    result = input_expression.eval_op(result, input_expression.children[i].n)
                return Smarten(result)
            elif isinstance(input_expression, SmartNegative):
                return Smarten(-input_expression.children[0].n)
            else:
                raise NotImplementedError


    def generate_address_map(self):
        if self.mode == "transform":
            return (["", ""])
        else:
            raise ValueError(f"Invalid mode: {self.mode}.")
