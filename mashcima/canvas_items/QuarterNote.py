from mashcima import Mashcima
from mashcima.canvas_items.StemNote import StemNote
import random
import copy


class QuarterNote(StemNote):
    def get_note_generic_annotation(self) -> str:
        return "q"

    def select_sprites(self, mc: Mashcima):
        self.sprites = copy.deepcopy(random.choice(mc.QUARTER_NOTES))
        super().select_sprites(mc)
