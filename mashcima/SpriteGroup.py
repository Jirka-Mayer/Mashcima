from mashcima.Sprite import Sprite
from typing import Dict, Tuple, List
import numpy as np
import copy


class SpriteGroup:
    """A collection of sprites placed around an origin"""
    def __init__(self):
        # position of this group's origin
        self.position_x = 0
        self.position_y = 0

        # padding around the group
        # (added on bounding box calculation)
        self.padding_top = 0
        self.padding_bottom = 0
        self.padding_left = 0
        self.padding_right = 0

        # bounding box in local pixel space
        self.top = 0
        self.left = 0
        self.bottom = 0
        self.right = 0
        self.width = 0
        self.height = 0

        # list of sprites to be drawn
        self.sprites: Dict[str, Sprite] = {}

        # list of points to be tracked
        # (points do not contribute to bounding box)
        self.points: Dict[str, Tuple[int, int]] = {}

    def add(self, name: str, sprite: Sprite):
        self.sprites[name] = sprite
        return self  # make it chainable

    def add_point(self, name: str, point: Tuple[int, int]):
        self.points[name] = point
        return self  # make it chainable

    def sprite(self, name: str):
        return self.sprites[name]

    def point(self, name: str):
        return self.points[name]

    def recalculate_bounding_box(self):
        if len(self.sprites) == 0:
            self.top = 0
            self.left = 0
            self.bottom = 0
            self.right = 0
        else:
            self.left = min([s.x for s in self.sprites.values()])
            self.right = max([s.x + s.mask.shape[1] for s in self.sprites.values()])
            self.top = min([s.y for s in self.sprites.values()])
            self.bottom = max([s.y + s.mask.shape[0] for s in self.sprites.values()])

        self.right += self.padding_right
        self.bottom += self.padding_bottom
        self.top -= self.padding_top
        self.left -= self.padding_left

        # calculate with and height
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    def create_flipped_copy(self, names: List[str] = None):
        """Returns a flipped copy of this item"""
        cp = copy.deepcopy(self)

        if names is None:
            names = list(cp.sprites.keys()) + list(cp.points.keys())

        for sprite_name, sprite in cp.sprites.items():
            if sprite_name in names:
                sprite.flip()

        for point_name in cp.points:
            if point_name in names:
                cp.points[point_name] = (
                    -cp.points[point_name][0],
                    -cp.points[point_name][1]
                )

        return cp

    def render(self, img: np.ndarray):
        for sprite in self.sprites.values():
            sprite.render(img, self.position_x, self.position_y)

    def inspect(self) -> np.ndarray:
        from mashcima.debug import draw_cross
        self.recalculate_bounding_box()
        img = np.zeros(shape=(self.height, self.width), dtype=np.float32)
        for s in self.sprites.values():
            s.render(img, -self.left, -self.top)
        draw_cross(img, -self.left, -self.top, size=5, thickness=1)
        return img
