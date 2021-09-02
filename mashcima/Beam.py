import cv2
import numpy as np
import random
from typing import List
from mashcima.canvas_items.BeamedNote import BeamedNote
from mashcima.debug import draw_cross


BEAM_THICKNESS = 4
BEAM_SPACING = 16
MAX_SLOPE = 0.35
SLOPE_JITTER = 0.1


class Beam:
    def __init__(self, items: List[BeamedNote]):
        assert len(items) >= 2
        assert not items[0].left_beamed
        assert items[0].right_beamed
        assert items[-1].left_beamed
        assert not items[-1].right_beamed
        for i in range(1, len(items) - 1):
            assert items[i].left_beamed and items[i].right_beamed

        self.DEBUG_RENDER = False

        # list of beamed notes
        self.items: List[BeamedNote] = items

        # is flipped
        self.flipped = (sum([i.pitch for i in items]) / len(items)) > 0

        # cross link
        for i in items:
            i.beam = self

        # rendering parameters
        self.pivot = (0, 0)
        self.slope = 0
        self._tops = []  # list of points for debug rendering

        # pre-compute some values
        self._compute_sided_beam_counts()

    def _f(self, x):
        """Line of the beam"""
        return x, int((x - self.pivot[0]) * self.slope + self.pivot[1])

    def place(self):
        # calculate the closest points above the notes where a beam can be
        # and pick a pivot point (the topmost point)
        tops = []
        sign = -1 if self.flipped else 1
        pivot = None
        for i in self.items:
            min_stem_length = (max(i.beams, 2) + 1) * BEAM_SPACING
            top = (
                i.sprites.position_x,
                i.sprites.position_y - sign * min_stem_length
            )
            tops.append(top)
            if pivot is None:
                pivot = top
            elif sign * top[1] < sign * pivot[1]:
                pivot = top

        # calculate viable slopes from pivot (that don't drop below any tops)
        slopes = []
        for i, t in enumerate(tops):
            if t == pivot:
                continue

            s = (pivot[1] - t[1]) / (pivot[0] - t[0])

            too_low = False
            for tt in tops:
                SLACK = 5  # slack for rounding error
                if ((tt[0] - pivot[0]) * s + pivot[1] - SLACK * sign) * sign > tt[1] * sign:
                    too_low = True
                    break
            if too_low:
                continue

            slopes.append(s)

        if len(slopes) == 0:
            print("Warning: No slopes found when placing a beam!")
            slopes.append(0)

        # pick the slope closest to the fitting line slope
        line = cv2.fitLine(np.array(tops), cv2.DIST_L2, 0, 0, 0).flatten()
        fitting_slope = line[1] / line[0]

        self.slope = sorted(slopes, key=lambda x: abs(x - fitting_slope))[0]
        self.pivot = pivot

        # randomize slope if too straight
        if abs(self.slope) < 0.01:
            self.slope = random.uniform(-SLOPE_JITTER, SLOPE_JITTER)

        # clamp to max slope
        if self.slope > MAX_SLOPE:
            self.slope = MAX_SLOPE
        if self.slope < -MAX_SLOPE:
            self.slope = -MAX_SLOPE

        # for debug
        self._tops = tops

        # update note sprites
        for i in self.items:
            i.update_sprites_for_stem_length(
                abs(i.sprites.position_y - self._f(i.sprites.position_x)[1])
            )

    def _compute_sided_beam_counts(self):
        self.items[0].left_beam_count = 0
        self.items[0].right_beam_count = self.items[0].beams
        self.items[-1].left_beam_count = self.items[-1].beams
        self.items[-1].right_beam_count = 0

        for i in range(1, len(self.items) - 1):
            before = self.items[i - 1]
            item = self.items[i]
            after = self.items[i + 1]

            # to each side give as many as possible shared beams
            item.left_beam_count = min(before.beams, item.beams)
            item.right_beam_count = min(after.beams, item.beams)

            # how many beams are needed to fit the note duration?
            remaining = item.beams - max(item.left_beam_count, item.right_beam_count)

            # no more beams needed
            if remaining == 0:
                continue

            assert remaining > 0

            # choose a side and add the remaining beams
            if random.choice([True, False]):
                item.left_beam_count += remaining
            else:
                item.right_beam_count += remaining

    def render(self, img: np.ndarray):
        for i in range(len(self.items) - 1):
            self._render_segment(img, self.items[i], self.items[i + 1])

        if self.DEBUG_RENDER:
            draw_cross(img, *self.pivot, 5)
            for t in self._tops:
                draw_cross(img, *t, 2)
            cv2.line(
                img,
                self._f(self.items[0].sprites.position_x),
                self._f(self.items[-1].sprites.position_x),
                thickness=1,
                color=0.5
            )

    def _render_segment(self, img: np.ndarray, start: BeamedNote, end: BeamedNote):
        a = start.global_stem_head
        b = end.global_stem_head

        def step_down(a, b):
            sp = -BEAM_SPACING if self.flipped else BEAM_SPACING
            return (a[0], a[1] + sp), (b[0], b[1] + sp)

        left_beams = start.right_beam_count
        right_beams = end.left_beam_count

        while left_beams > 0 and right_beams > 0:
            cv2.line(img, a, b, thickness=BEAM_THICKNESS, color=1)
            a, b = step_down(a, b)
            left_beams -= 1
            right_beams -= 1

        while left_beams > 0:
            t = random.uniform(0.6, 0.8)
            m = (int(a[0] * t + b[0] * (1 - t)), int(a[1] * t + b[1] * (1 - t)))
            cv2.line(img, a, m, thickness=BEAM_THICKNESS, color=1)
            a, b = step_down(a, b)
            left_beams -= 1

        while right_beams > 0:
            t = random.uniform(0.2, 0.4)
            m = (int(a[0] * t + b[0] * (1 - t)), int(a[1] * t + b[1] * (1 - t)))
            cv2.line(img, m, b, thickness=BEAM_THICKNESS, color=1)
            a, b = step_down(a, b)
            right_beams -= 1
