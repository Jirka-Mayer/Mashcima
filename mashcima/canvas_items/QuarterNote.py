from mashcima.SymbolRepository import SymbolRepository
from mashcima.canvas_items.StemNote import StemNote
import random
import copy


class QuarterNote(StemNote):
    def get_note_generic_annotation(self) -> str:
        return "q"

    def select_sprites(self, repo: SymbolRepository):
        self.sprites = copy.deepcopy(random.choice(repo.QUARTER_NOTES))
        super().select_sprites(repo)
