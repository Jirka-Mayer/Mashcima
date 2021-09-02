from typing import Optional, List
from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
import copy
import random


class DurationDots:
    def __init__(self, item: CanvasItem, token: Optional[str]):
        # canvas item reference (what are we attached on)
        self.item = item

        assert token in [None, "*", "**"]
        self.token = token

    def get_tokens(self) -> List[str]:
        if self.token is not None:
            return [self.token]
        else:
            return []

    def select_sprites(self, mc: Mashcima):
        if self.token is None:
            return
        self.item.sprites.add("duration_dot", copy.deepcopy(random.choice(mc.DOTS)))
        if self.token == "**":
            self.item.sprites.add("duration_dot_2", copy.deepcopy(random.choice(mc.DOTS)))

    def place_sprites(self):
        from mashcima.canvas_items.Note import Note  # prevent cyclic dependency
        from mashcima.canvas_items.Rest import Rest

        if self.token is None:
            return

        # Before this call, dot is centered on origin

        # X offset from the item
        first_dot = self.item.sprites.sprite("duration_dot")

        if isinstance(self.item, Note):
            first_dot.x += self.item.sprites.sprite("notehead").width // 2
        if isinstance(self.item, Rest):
            first_dot.x += self.item.sprites.sprite("rest").width // 2

        first_dot.x += first_dot.width // 2
        first_dot.x += random.randint(5, 15)

        # Y offset from the item
        if isinstance(self.item, Note):
            if self.item.pitch % 2 == 0:
                first_dot.y += 10 if self.item.pitch > 0 else -10  # put it into a space
        if isinstance(self.item, Rest):
            if self.item.kind == "wr":
                first_dot.y += 10
            else:
                first_dot.y -= 10
        first_dot.y += random.randint(-5, 5)

        # second dot position
        if self.token == "**":
            second_dot = self.item.sprites.sprite("duration_dot_2")
            second_dot.x += first_dot.x
            second_dot.y += first_dot.y
            second_dot.x += second_dot.width // 2
            second_dot.x += random.randint(5, 15)
