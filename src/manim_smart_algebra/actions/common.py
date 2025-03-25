from .action_core import *
from .variants import *
from .combinations import *
from ..expressions.operations import *
from ..expressions.variables import *
from ..expressions.relations import *
from MF_Tools.dual_compatibility import PI, FadeIn


class swap_children_(SmartAction):
    def __init__(self, preaddress='', mode="arc", arc_size=0.75*PI, **kwargs):
        self.mode = mode
        self.arc_size = arc_size
        super().__init__(preaddress=preaddress,**kwargs)
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        assert len(input_expression.children) == 2, f"Cannot swap children of {input_expression}, must have two children."
        return type(input_expression)(input_expression.children[1], input_expression.children[0])

    @preaddressmap
    def get_addressmap(self, input_expression=None):
        if self.mode == "arc":
            return [
                ["0", "1", {"path_arc": self.arc_size}],
                ["1", "0", {"path_arc": self.arc_size}]
            ]
        elif self.mode == "straight":
            return [
                ["0", "1"],
                ["1", "0"]
            ]
        else:
            raise ValueError(f"Invalid mode: {self.mode}. Must be 'arc' or 'straight'.")


class apply_operation_(SmartAction):
    def __init__(self, OpClass, other, preaddress='', side="right", introducer=Write, **kwargs):
        self.OpClass = OpClass
        self.other = Smarten(other)
        self.side = side
        self.introducer = introducer
        super().__init__(preaddress=preaddress,**kwargs)
    
    @preaddressfunc
    def get_output_expression(self, input_expression):
        if self.side == "right":
            output_expression = self.OpClass(input_expression, self.other) # Putting a .copy() on the input expression fixes the problem. Try to understand this and then probably fold this into the decorator
        elif self.side == "left":
            output_expression = self.OpClass(self.other, input_expression)
        else:
            raise ValueError(f"Invalid side: {self.side}. Must be left or right.")
        return output_expression

    @preaddressmap
    def get_addressmap(self, input_expression):
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
    def __init__(self, other, *args, **kwargs):
        super().__init__(SmartAdd, other, *args, **kwargs)

class sub_(apply_operation_):
    def __init__(self, other, *args, **kwargs):
        super().__init__(SmartSub, other, *args, **kwargs)

class mul_(apply_operation_):
    def __init__(self, other, *args, **kwargs):
        super().__init__(SmartMul, other, *args, **kwargs)

class div_(apply_operation_):
    def __init__(self, other, *args, **kwargs):
        super().__init__(SmartDiv, other, *args, **kwargs)

class pow_(apply_operation_):
    def __init__(self, other, *args, **kwargs):
        super().__init__(SmartPow, other, *args, **kwargs)

class equals_(apply_operation_):
    def __init__(self, other, *args, **kwargs):
        super().__init__(SmartEquation, other, *args, **kwargs)


class substitute_(SmartAction):
    def __init__(self, sub_dict, preaddress='', mode="transform", arc_size=PI, fade_shift=DOWN*0.2, lag=0, **kwargs):
        self.sub_dict = sub_dict
        self.preaddress = preaddress
        self.mode = mode
        self.arc_size = arc_size
        self.fade_shift = fade_shift
        self.lag = lag #usually looks like shit but can be cool sometimes
        super().__init__(preaddress=preaddress,**kwargs)
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        return input_expression.substitute(self.sub_dict)

    @preaddressmap
    def get_addressmap(self, input_expression=None):
        target_addresses = []
        for var in self.sub_dict:
            target_addresses += input_expression.get_subex(self.preaddress).get_addresses_of_subex(var)
        addressmap = []
        if self.mode == "transform":
            for i,ad in enumerate(target_addresses):
                addressmap.append([ad, ad, {"delay": self.lag*i}])
            return addressmap
        elif self.mode == "swirl":
            for i,ad in enumerate(target_addresses):
                addressmap.append([ad, ad, {"path_arc": self.arc_size, "delay": self.lag*i}])
            return addressmap
        elif self.mode == "fade":
            for i,ad in enumerate(target_addresses):
                addressmap.append([ad, FadeOut, {"shift": self.fade_shift, "delay": self.lag*i}])
                addressmap.append([FadeIn, ad, {"shift": self.fade_shift, "delay": self.lag*i}])
            return addressmap


class substitute_into_(SmartAction):
    def __init__(self, outer_expression, substitution_variable=SmartVariable('x'), **kwargs):
        self.outer_expression = outer_expression
        self.substitution_variable = substitution_variable
        super().__init__(**kwargs)
    
    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        return self.outer_expression.substitute({self.substitution_variable: input_expression})
    
    @preaddressmap
    def get_addressmap(self, input_expression=None):
        addressmap = []
        sub_into_addresses = self.outer_expression.get_addresses_of_subex(self.substitution_variable)
        for ad in sub_into_addresses:
            if not input_expression.parentheses:
                ad = ad + "_"
            addressmap.append(['', ad])
        return addressmap
    
    def get_animation(self, *args, **kwargs):
        return super().get_animation(*args, auto_fade=True, auto_resolve_delay=0.75, **kwargs)


class evaluate_(SmartAction):
    def __init__(self, preaddress='', mode="random leaf", **kwargs):
        super().__init__(preaddress=preaddress,**kwargs)
        # if mode == "random leaf":
        #     leaf_addresses = input_expression.get_all_leaf_addresses()
        #     leaf_address = np.random.choice(leaves)
        #     self.preaddress = leaf_address

    @preaddressfunc
    def get_output_expression(self, input_expression=None):
        return input_expression.evaluate()
    
    @preaddressmap
    def get_addressmap(self, input_expression=None):
        return [
            ["", ""] #extension by preaddress is done by decorator!
        ]
    

class distribute_(SmartAction):
       # Not done yet, multilayer does not work... this is so necessary but rather nontrivial... hm...
    def __init__(self, preaddress='', mode="auto", multilayer=False, **kwargs):
        self.mode = mode #"auto", "left", "right"
        super().__init__(preaddress=preaddress,**kwargs)
    
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

    def determine_direction(self, input_expression=None):
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
    def get_addressmap(self, input_expression=None):
        return [
            ["", ""] #standin idk what the fuck im doing here
        ]






from .variants import AlgebraicAction
a = SmartVariable('a')
b = SmartVariable('b')
c = SmartVariable('c')

square_binomial_ = AlgebraicAction((a+b)**2, a**2 + 2*a*b + b**2)

