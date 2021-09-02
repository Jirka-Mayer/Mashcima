from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
from mashcima.DurationDots import DurationDots
from typing import Optional, Dict, List
import random
import copy


class Rest(CanvasItem):
    def __init__(
            self,
            rest_kind: str = "qr",
            duration_dots: Optional[str] = None,
            **kwargs
    ):
        super().__init__(**kwargs)

        # rest kind
        assert rest_kind in ["lr", "br", "wr", "hr", "qr", "er", "sr"]
        self.kind = rest_kind

        # duration dots
        self.duration_dots = DurationDots(self, duration_dots)

    def get_item_annotation_token(self) -> str:
        return self.kind

    def get_after_attachment_tokens(self) -> List[str]:
        tokens = super().get_after_attachment_tokens()
        tokens = self.duration_dots.get_tokens() + tokens
        return tokens

    def contribute_to_padding(self):
        if self.kind in ["lr", "br", "wr", "hr"]:
            self.sprites.padding_left += 20
            self.sprites.padding_right += 20

    def select_sprites(self, mc: Mashcima):
        if self.kind == "lr":
            self.sprites = copy.deepcopy(random.choice(mc.LONGA_RESTS))
        if self.kind == "br":
            self.sprites = copy.deepcopy(random.choice(mc.BREVE_RESTS))
        if self.kind == "wr":
            self.sprites = copy.deepcopy(random.choice(mc.WHOLE_RESTS))
        if self.kind == "hr":
            self.sprites = copy.deepcopy(random.choice(mc.HALF_RESTS))
        if self.kind == "qr":
            self.sprites = copy.deepcopy(random.choice(mc.QUARTER_RESTS))
        if self.kind == "er":
            self.sprites = copy.deepcopy(random.choice(mc.EIGHTH_RESTS))
        if self.kind == "sr":
            self.sprites = copy.deepcopy(random.choice(mc.SIXTEENTH_RESTS))

        self.duration_dots.select_sprites(mc)
        super().select_sprites(mc)

    def place_sprites(self):
        self.duration_dots.place_sprites()
        super().place_sprites()

    def place_item(self, head: int, pitch_positions: Dict[int, int]):
        out = super().place_item(head, pitch_positions)
        if self.kind == "wr":
            self.sprites.position_y = pitch_positions[2]
        return out
