from MF_Tools import *

class Test(Scene):
    def construct(self):
        A = Tex('a^2 + b^2 \\over c^2')
        B = Tex('5^2 + 12^2 \\over 13^2')
        TBGM = TransformByGlyphMap(A, B, ([3], [3,4]), ([6], [7,8]))
        self.add(A)
        self.embed()