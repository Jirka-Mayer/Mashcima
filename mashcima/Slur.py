import numpy as np
import cv2
import random
from mashcima.canvas_items.SlurableItem import SlurableItem
from mashcima.canvas_items.StemNote import StemNote


class Slur:
    def __init__(self, start_item: SlurableItem, end_item: SlurableItem):
        self.start_item = start_item
        self.end_item = end_item

        # True: /\   False: \/
        self.flipped = False

        # whether to use the simple tail-to-tail attachment
        # or below-note to below-note
        self.tail_to_tail = True

    def _set_is_flipped(self):
        # both ends have a stem
        if isinstance(self.start_item, StemNote) and isinstance(self.end_item, StemNote):

            # both not flipped
            if not self.start_item.flipped and not self.end_item.flipped:
                self.flipped = False
                self.tail_to_tail = False
                return

            # both flipped
            if self.start_item.flipped and self.end_item.flipped:
                self.flipped = True
                self.tail_to_tail = False
                return

            # otherwise randomize
            self.flipped = random.choice([True, False])
            return

        # start has a stem
        if isinstance(self.start_item, StemNote):
            self.flipped = self.start_item.flipped
            self.tail_to_tail = False
            return

        # end has a stem
        if isinstance(self.end_item, StemNote):
            self.flipped = self.end_item.flipped
            self.tail_to_tail = False
            return

        # otherwise randomize
        self.flipped = random.choice([True, False])
        return

    def render(self, img: np.ndarray):
        slur_thickness = 3

        # NOTE: the slur is rendered as a parabola going through 3 points
        # (two attachments and one center point)

        self._set_is_flipped()
        start_attachment = self.start_item.get_slur_start_attachment_point(self)
        end_attachment = self.end_item.get_slur_end_attachment_point(self)
        width = end_attachment[0] - start_attachment[0]

        # calculate center point
        center_point = [
            (start_attachment[0] + end_attachment[0]) // 2,
            (start_attachment[1] + end_attachment[1]) // 2
        ]
        center_point[1] += (-1 if self.flipped else 1) * min(int(width / 5), 20)
        center_point = tuple(center_point)

        # calculate coefficients a of: y = ax^2 +bx +c
        A = np.array([
            [start_attachment[0] ** 2, start_attachment[0], 1],
            [center_point[0] ** 2, center_point[0], 1],
            [end_attachment[0] ** 2, end_attachment[0], 1]
        ])
        v = np.array([
            [start_attachment[1]],
            [center_point[1]],
            [end_attachment[1]]
        ])
        try:
            abc = np.linalg.inv(A).dot(v)
        except:
            print("Slur didn't render - singular matrix")
            return
        f = lambda x: abc[0] * x**2 + abc[1] * x + abc[2]

        for x in range(start_attachment[0], end_attachment[0]):
            cv2.line(
                img,
                (x, int(f(x))),
                (x + 1, int(f(x + 1))),
                thickness=slur_thickness,
                color=1
            )
