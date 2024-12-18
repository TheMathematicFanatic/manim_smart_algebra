from manimlib import (
    Animation,
    AnimationGroup,
    Scene,
    Succession,
    VGroup, Mobject,
    ReplacementTransform,
    FadeIn, FadeOut,
    index_labels,
    RED_D, BLUE_D,
    ORIGIN, DOWN,
    ShowCreation,
    )

class Wait(Animation):
    def __init__(self, duration=1, **kwargs):
        super().__init__(mobject=Mobject(), run_time=duration, **kwargs)

    def interpolate_mobject(self, alpha):
        # No actual change to mobjects; just serves as a time delay
        pass


class TransformByGlyphMap(AnimationGroup):
    def __init__(
        self,
        mobA,
        mobB,
        *glyph_map,
        from_copy=False,
        mobA_submobject_index=[],
        mobB_submobject_index=[],
        default_introducer=FadeIn,
        default_remover=FadeOut,
        introduce_individually=False,
        remove_individually=False,
        #shift_fades=True,
        show_indices=False,
        A_index_labels_color=RED_D,
        B_index_labels_color=BLUE_D,
        index_label_height=0.18,
        printing=False,
        **kwargs
        ):

        A = mobA.copy() if from_copy else mobA
        for i in mobA_submobject_index:
            A = A[i]
        self.mobject = A
        B = mobB
        for i in mobB_submobject_index:
            B = B[i]
        self.target_mobject = B
        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []

        def VG(mob, index_list):
            return VGroup(*[mob[i] for i in index_list])
        
        def remove_keys(dict, keys=["delay"]):
            return {key: value for key, value in dict.items() if key not in keys}
        
        if len(glyph_map)==0: show_indices=True

        for entry in glyph_map:
            if printing:
                print("Glyph map entry: ", entry)
            assert len(entry) in [2, 3], "Invalid glyph_map entry: " + str(entry)
            entry_kwargs = {} if len(entry) == 2 else entry[2]

            if not entry[0] and not entry[1]:
                print("Empty glyph_map entry: " + str(entry))
                show_indices = True
            elif (not entry[0]) or (isinstance(entry[0], type) and issubclass(entry[0], Animation)):
                Introducer = entry[0] if entry[0] else default_introducer
                introduced_mobs = [B[i] for i in entry[1]] if introduce_individually else [VG(B,entry[1])]
                for mob in introduced_mobs:
                    animations.append(Introducer(
                        mob,
                        **{
                            **kwargs,
                            #**{"shift":B.get_center() - A.get_center() if shift_fades else ORIGIN},
                            **remove_keys(entry_kwargs)
                        }
                        ))
                    if "delay" in entry_kwargs:
                        animations[-1] = Succession(Wait(entry_kwargs["delay"]), animations[-1])
                mentioned_to_indices += entry[1]
            elif not entry[1] or (isinstance(entry[1], type) and issubclass(entry[1], Animation)):
                Remover = entry[1] if entry[1] else default_remover
                removed_mobs = [A[i] for i in entry[0]] if remove_individually else [VG(A,entry[0])]
                for mob in removed_mobs:
                    animations.append(Remover(
                        mob,
                        **{
                            **kwargs,
                            #**{"shift":B.get_center() - A.get_center() if shift_fades else ORIGIN},
                            **remove_keys(entry_kwargs)
                        }
                        ))
                    if "delay" in entry_kwargs:
                        animations[-1] = Succession(Wait(entry_kwargs["delay"]), animations[-1])
                mentioned_from_indices += entry[0]
            elif len(entry[0]) > 0 and len(entry[1]) > 0:
                animations.append(ReplacementTransform(
                    VGroup(*[A[i].copy() if i in mentioned_from_indices else A[i] for i in entry[0]]),
                    VG(B,entry[1]),
                    **{
                        **kwargs,
                        **remove_keys(entry_kwargs)
                        }
                    ))
                if "delay" in entry_kwargs:
                    animations[-1] = Succession(Wait(entry_kwargs["delay"]), animations[-1])
                mentioned_from_indices += entry[0]
                mentioned_to_indices += entry[1]
            else:
                raise ValueError("Invalid glyph_map entry: " + str(entry))
        
        if printing:
            print("All mentioned from indices: ", mentioned_from_indices)
            print("All mentioned to indices: ", mentioned_to_indices)
        
        remaining_from_indices = [i for i in range(len(A)) if i not in mentioned_from_indices]
        remaining_to_indices = [i for i in range(len(B)) if i not in mentioned_to_indices]
        
        if not len(remaining_from_indices) == len(remaining_to_indices):
            print("Error: lengths of unmentioned indices do not match.")
            print(f"Remaining from indices (length {len(remaining_from_indices)}): ", remaining_from_indices)
            print(f"Remaining to indices (length {len(remaining_to_indices)}): ", remaining_to_indices)
            show_indices = True
        elif printing:
            print("Remaining from indices: ", remaining_from_indices)
            print("Remaining to indices: ", remaining_to_indices)
        
        if show_indices:
            print("Showing indices...")
            super().__init__(
                ShowCreation(index_labels(A, label_height=index_label_height).set_fill(color=A_index_labels_color)),
                FadeIn(B.next_to(A, DOWN), shift=DOWN),
                ShowCreation(index_labels(B, label_height=index_label_height).set_fill(color=B_index_labels_color)),
                Wait(5),
                lag_ratio=0.5
            )
        else:
            for i,j in zip(remaining_from_indices, remaining_to_indices):
                animations.append(ReplacementTransform(A[i], B[j], **kwargs))
            super().__init__(*animations, **kwargs)

    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)
        scene.remove(self.mobject)
        scene.add(self.target_mobject)
    
    # def create_target(self):
    #     self.target_mobject = self.B
    #     return self.target_mobject


class TransformByAddressMap(TransformByGlyphMap):
    pass