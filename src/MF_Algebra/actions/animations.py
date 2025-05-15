from MF_Tools.transforms import TransformByGlyphMap



class TransformByAddressMap(TransformByGlyphMap):
    def __init__(self, expA, expB, *addressmap, **kwargs):
        glyphmap = self.addressmap_to_glyphmap(expA, expB, addressmap)
        super().__init__(expA.mob, expB.mob, *glyphmap, **kwargs)
    
    def addressmap_to_glyphmap(self, expA, expB, addressmap):
        glyphmap = [
            (
                expA.get_glyphs(entry[0]) if isinstance(entry[0], str) else entry[0],
                expB.get_glyphs(entry[1]) if isinstance(entry[1], str) else entry[1],
                entry[2] if len(entry) > 2 else {}
            )
            for entry in addressmap
        ]
        return glyphmap




