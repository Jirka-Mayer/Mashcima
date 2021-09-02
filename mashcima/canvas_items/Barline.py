from mashcima import Mashcima
from mashcima.canvas_items.SlurableItem import SlurableItem
from mashcima.Sprite import Sprite
import random
import copy
from typing import Dict


class Barline(SlurableItem):
    @property
    def up(self):
        return self.canvas_options.barlines_up

    @property
    def down(self):
        return self.canvas_options.barlines_down

    def get_item_annotation_token(self):
        return "|"

    def select_sprites(self, mc: Mashcima):
        if not self.up and not self.down:
            self.sprites = copy.deepcopy(random.choice(mc.BAR_LINES))
        else:
            self.sprites = copy.deepcopy(random.choice(mc.TALL_BAR_LINES))
        super().select_sprites(mc)

    def place_sprites(self):
        s: Sprite = self.sprites.sprite("barline")

        if self.up and not self.down:
            s.y -= s.height // 2

        if not self.up and self.down:
            s.y += s.height // 2

        super().place_sprites()

    def place_item(self, head: int, pitch_positions: Dict[int, int]):
        out = super().place_item(head, pitch_positions)

        if self.up and not self.down:
            self.sprites.position_y = pitch_positions[-4]

        if not self.up and self.down:
            self.sprites.position_y = pitch_positions[4]

        return out
