from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
import copy
import random
from typing import Dict


class Clef(CanvasItem):
    def __init__(self, pitch: int, clef: str, **kwargs):
        super().__init__(**kwargs)

        self.clef = clef
        assert clef in ["G", "F", "C"]

        # placement of the clef
        self.pitch = pitch

        if clef == "G":
            assert pitch in [-4, -2]
        if clef == "F":
            assert pitch in [0, 2, 3]
        if clef == "C":
            assert pitch in [-4, -2, 0, 2, 4]

    def get_item_annotation_token(self) -> str:
        return "clef." + self.clef + str(self.pitch)

    def select_sprites(self, mc: Mashcima):
        if self.clef == "G":
            self.sprites = copy.deepcopy(random.choice(mc.G_CLEFS))
        if self.clef == "F":
            self.sprites = copy.deepcopy(random.choice(mc.F_CLEFS))
        if self.clef == "C":
            self.sprites = copy.deepcopy(random.choice(mc.C_CLEFS))
        super().select_sprites(mc)

    def place_item(self, head: int, pitch_positions: Dict[int, int]) -> int:
        out = super().place_item(head, pitch_positions)
        self.sprites.position_y = pitch_positions[self.pitch]
        return out
