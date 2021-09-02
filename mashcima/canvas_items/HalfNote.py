from mashcima import Mashcima
from mashcima.canvas_items.StemNote import StemNote
import random
import copy


class HalfNote(StemNote):
    def get_note_generic_annotation(self) -> str:
        return "h"

    def select_sprites(self, mc: Mashcima):
        self.sprites = copy.deepcopy(random.choice(mc.HALF_NOTES))
        super().select_sprites(mc)
