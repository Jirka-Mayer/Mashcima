from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
import random
import copy
from typing import Dict


class TimeSignature(CanvasItem):
    def __init__(self, top: int, bottom: int, **kwargs):
        super().__init__(**kwargs)

        self.top = top
        self.bottom = bottom

    def get_annotation_tokens(self):
        return [
            "time." + str(self.top),
            "time." + str(self.bottom)
        ]

    def select_sprites(self, mc: Mashcima):
        top_sprite = copy.deepcopy(
            random.choice(mc.TIME_MARKS["time_" + str(self.top)]).sprite("symbol")
        )
        bottom_sprite = copy.deepcopy(
            random.choice(mc.TIME_MARKS["time_" + str(self.bottom)]).sprite("symbol")
        )
        top_sprite.y -= top_sprite.height // 2 + random.randint(5, 10)
        bottom_sprite.y += bottom_sprite.height // 2 + random.randint(5, 10)
        self.sprites.add("top", top_sprite)
        self.sprites.add("bottom", bottom_sprite)
        super().select_sprites(mc)

    def place_item(self, head: int, pitch_positions: Dict[int, int]) -> int:
        out = super().place_item(head, pitch_positions)
        self.sprites.position_y = pitch_positions[0]
        return out
