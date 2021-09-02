from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
from mashcima.Sprite import Sprite
import random
import copy
from typing import Dict, List


class KeySignature(CanvasItem):
    def __init__(self, types: List[str], pitches: List[int], **kwargs):
        super().__init__(**kwargs)

        assert len(types) == len(pitches)
        for t in types:
            assert t in ["#", "b", "N"]

        self.types = types
        self.pitches = pitches
        self.item_sprites: List[Sprite] = []

    def get_annotation_tokens(self):
        tokens = []
        for i in range(len(self.pitches)):
            tokens.append(self.types[i] + str(self.pitches[i]))
        return tokens

    def select_sprites(self, mc: Mashcima):
        for i, t in enumerate(self.types):
            s = None
            if t == "#":
                s = copy.deepcopy(random.choice(mc.SHARPS))
            if t == "b":
                s = copy.deepcopy(random.choice(mc.FLATS))
            if t == "N":
                s = copy.deepcopy(random.choice(mc.NATURALS))
            assert s is not None
            self.sprites.add("item_" + str(i), s)
            self.item_sprites.append(s)
        super().select_sprites(mc)

    def place_item(self, head: int, pitch_positions: Dict[int, int]) -> int:
        self.sprites.position_x = head
        self.sprites.position_y = 0
        local_head = 0
        for i, s in enumerate(self.item_sprites):
            s.x += s.width // 2 + local_head
            s.y += pitch_positions[self.pitches[i]]
            local_head += s.width
            if i < len(self.item_sprites) - 1:
                local_head += random.randint(0, 5)  # padding between items
        self.sprites.recalculate_bounding_box()
        return local_head
