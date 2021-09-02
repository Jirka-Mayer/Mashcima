from mashcima import Mashcima
from mashcima.canvas_items.Note import Note
import random
import copy


class WholeNote(Note):
    def get_note_generic_annotation(self) -> str:
        return "w"
    
    def select_sprites(self, mc: Mashcima):
        self.sprites = copy.deepcopy(random.choice(mc.WHOLE_NOTES))
        super().select_sprites(mc)
