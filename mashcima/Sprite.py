import numpy as np
import cv2


PRINT_WARNINGS_DEFAULT = False


class Sprite:
    def __init__(
            self,
            x: int,
            y: int,
            mask: np.ndarray,
            print_render_warnings: bool = PRINT_WARNINGS_DEFAULT
    ):
        # local position within a canvas item (upper left corner of the mask)
        self.x = x
        self.y = y

        # the actual mask to be printed (image data)
        self.mask = mask.astype(dtype=np.float32)

        self.print_render_warnings = print_render_warnings

    @property
    def width(self):
        return self.mask.shape[1]

    @property
    def height(self):
        return self.mask.shape[0]

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    def flip(self):
        self.x = -self.x - self.mask.shape[1]
        self.y = -self.y - self.mask.shape[0]
        self.mask = np.rot90(np.rot90(self.mask))

    def stretch_height(self, target_height: int):
        self.mask = cv2.resize(
            self.mask,
            (self.width, target_height),
            interpolation=cv2.INTER_NEAREST
        )

    def render(self, img: np.ndarray, parent_x: int, parent_y: int):
        x = self.x + parent_x
        y = self.y + parent_y
        mask = self.mask

        # following code is copied from a helper method and
        # expects: x, y, mask        and renders in canvas pixel space

        y_from = y
        y_to = y + mask.shape[0]
        x_from = x
        x_to = x + mask.shape[1]

        if x_from < 0:
            if self.print_render_warnings:
                print("Image does not fit horizontally")
            mask = mask[:, abs(x_from):]
            x_from = 0

        if x_to > img.shape[1]:
            if self.print_render_warnings:
                print("Image does not fit horizontally")
            mask = mask[:, :(mask.shape[1] - (x_to - img.shape[1]))]
            x_to = img.shape[1]

        if y_from < 0:
            if self.print_render_warnings:
                print("Image does not fit vertically")
            mask = mask[abs(y_from):, :]
            y_from = 0

        if y_to > img.shape[0]:
            if self.print_render_warnings:
                print("Image does not fit vertically")
            mask = mask[:(mask.shape[0] - (y_to - img.shape[0])), :]
            y_to = img.shape[0]

        try:
            img[y_from:y_to, x_from:x_to] += (1 - img[y_from:y_to, x_from:x_to]) * mask
        except ValueError:
            # NOTE: this is not a warning, this is bad, so print always
            if PRINT_WARNINGS_DEFAULT:
                print("Image does not fit inside the canvas at all")

    def inspect(self) -> np.ndarray:
        from mashcima.debug import draw_cross
        img = self.mask.copy()
        draw_cross(img, -self.left, -self.top, size=5, thickness=1)
        return img
