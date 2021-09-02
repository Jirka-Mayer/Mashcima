from mashcima.SymbolRepository import SymbolRepository
from mashcima.canvas_items.Note import Note
import random
import copy


class WholeNote(Note):
    def get_note_generic_annotation(self) -> str:
        return "w"
    
    def select_sprites(self, repo: SymbolRepository):
        self.sprites = copy.deepcopy(random.choice(repo.WHOLE_NOTES))
        super().select_sprites(repo)
