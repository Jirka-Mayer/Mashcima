from mashcima import Mashcima
from mashcima.canvas_items.Note import Note
from mashcima.debug import draw_cross
import numpy as np
import random


class StemNote(Note):
    def __init__(self, pitch: int, **kwargs):
        super().__init__(pitch, **kwargs)

        # is the note flipped upside-down?
        # decided in select_sprites(...)
        self.flipped = False

    @property
    def stem_head_x(self):
        return self.sprites.point("stem_head")[0]

    @property
    def stem_head_y(self):
        return self.sprites.point("stem_head")[1]

    def select_sprites(self, mc: Mashcima):
        super().select_sprites(mc)

        # decide whether to flip or not
        self.flipped = self.pitch > 0
        if self.pitch in self.canvas_options.randomize_stem_flips_for_pitches:
            self.flipped = random.choice([True, False])

    def place_sprites(self):
        if self.flipped:
            self.sprites = self.sprites.create_flipped_copy(
                [
                    "notehead", "stem", "stem_head",
                    "flag_8", "flag_16", "flag_32"
                ]
            )
        super().place_sprites()

    def render(self, img: np.ndarray):
        super().render(img)

        if self.DEBUG_RENDER:
            draw_cross(
                img,
                self.sprites.position_x + self.stem_head_x,
                self.sprites.position_y + self.stem_head_y,
                5
            )
