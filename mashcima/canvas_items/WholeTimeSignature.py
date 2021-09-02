from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
import random
import copy
from typing import Dict
import numpy as np
import cv2


class WholeTimeSignature(CanvasItem):
    def __init__(self, crossed: bool = False, **kwargs):
        super().__init__(**kwargs)

        self.crossed = crossed

    def get_item_annotation_token(self):
        if self.crossed:
            return "time.C/"
        else:
            return "time.C"

    def select_sprites(self, mc: Mashcima):
        self.sprites = copy.deepcopy(random.choice(mc.TIME_MARKS["time_c"]))
        super().select_sprites(mc)

    def place_item(self, head: int, pitch_positions: Dict[int, int]) -> int:
        out = super().place_item(head, pitch_positions)
        self.sprites.position_y = pitch_positions[0]
        return out

    def render(self, img: np.ndarray):
        super().render(img)
        sprite = self.sprites.sprite("symbol")
        if self.crossed:
            cv2.line(
                img,
                (
                    self.sprites.position_x + random.randint(-5, 5) + 5,
                    self.sprites.position_y - int(sprite.height * 0.7)
                ),
                (
                    self.sprites.position_x + random.randint(-5, 5) - 5,
                    self.sprites.position_y + int(sprite.height * 0.7)
                ),
                thickness=3,
                color=1
            )
