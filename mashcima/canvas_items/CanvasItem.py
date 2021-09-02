from mashcima import Mashcima
import numpy as np
import cv2
from typing import List, Dict
from mashcima.SpriteGroup import SpriteGroup
from mashcima.debug import draw_cross
from mashcima.CanvasOptions import CanvasOptions


class CanvasItem:
    def __init__(self, **kwargs):
        self.sprites: SpriteGroup = SpriteGroup()

        self.canvas_options: CanvasOptions = None

        self.DEBUG_RENDER = False

    def set_canvas_options(self, options: CanvasOptions):
        """Called by the canvas when added into the canvas"""
        self.canvas_options = options

    def get_annotation_tokens(self):
        return self.get_before_attachment_tokens() + \
            [self.get_item_annotation_token()] + \
            self.get_after_attachment_tokens()

    def get_item_annotation_token(self) -> str:
        raise NotImplementedError("Override this")

    def get_before_attachment_tokens(self) -> List[str]:
        return []

    def get_after_attachment_tokens(self) -> List[str]:
        return []

    def select_sprites(self, mc: Mashcima):
        pass

    def place_sprites(self):
        self.contribute_to_padding()
        self.sprites.recalculate_bounding_box()

    def contribute_to_padding(self):
        self.sprites.padding_bottom = 0
        self.sprites.padding_top = 0
        self.sprites.padding_left = 0
        self.sprites.padding_right = 0

    def place_item(self, head: int, pitch_positions: Dict[int, int]) -> int:
        self.sprites.position_x = head - self.sprites.left
        self.sprites.position_y = pitch_positions[0]
        return self.sprites.width

    def render(self, img: np.ndarray):
        self.sprites.render(img)

        if self.DEBUG_RENDER:
            # origin
            draw_cross(img, self.sprites.position_x, self.sprites.position_y, 10)

            # bounding box
            cv2.rectangle(
                img,
                (
                    self.sprites.left + self.sprites.position_x,
                    self.sprites.top + self.sprites.position_y
                ),
                (
                    self.sprites.right + self.sprites.position_x,
                    self.sprites.bottom + self.sprites.position_y
                ),
                color=0.5,
                thickness=1
            )
