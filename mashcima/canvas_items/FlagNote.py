from mashcima import Mashcima
from mashcima.canvas_items.StemNote import StemNote
import random
import copy
import numpy as np


class FlagNote(StemNote):
    def __init__(self, flag_kind: str, **kwargs):
        super().__init__(**kwargs)

        assert flag_kind in ["e", "s"]
        self.kind = flag_kind

    def get_note_generic_annotation(self) -> str:
        return self.kind

    def select_sprites(self, mc: Mashcima):
        if self.kind == "e":
            self.sprites = copy.deepcopy(random.choice(mc.EIGHTH_NOTES))
        if self.kind == "s":
            self.sprites = copy.deepcopy(random.choice(mc.SIXTEENTH_NOTES))
        super().select_sprites(mc)

    def place_sprites(self):
        super().place_sprites()

        if self.flipped:
            f = self.sprites.sprite("flag_8")
            f.mask = np.flip(f.mask, axis=1)
            f.x += f.width

            if self.kind == "s":
                f = self.sprites.sprite("flag_16")
                f.mask = np.flip(f.mask, axis=1)
                f.x += f.width
