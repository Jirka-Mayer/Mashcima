from mashcima.canvas_items.CanvasItem import CanvasItem
from typing import List, Tuple


ADDITIONAL_SLUR_PADDING = 20


class SlurableItem(CanvasItem):
    def __init__(
            self,
            slur_start: bool = False,
            slur_end: bool = False,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.slur_start = slur_start
        self.slur_end = slur_end

    def get_before_attachment_tokens(self) -> List[str]:
        if self.slur_end:
            return [")"]
        else:
            return []

    def get_after_attachment_tokens(self) -> List[str]:
        if self.slur_start:
            return ["("]
        else:
            return []

    # def contribute_to_padding(self):
    #     if self.slur_end:
    #         self.sprites.padding_left += ADDITIONAL_SLUR_PADDING
    #     if self.slur_start:
    #         self.sprites.padding_right += ADDITIONAL_SLUR_PADDING

    def get_slur_start_attachment_point(self, slur) -> Tuple[int, int]:
        return self._get_slur_attachment_point(True, slur)

    def get_slur_end_attachment_point(self, slur) -> Tuple[int, int]:
        return self._get_slur_attachment_point(False, slur)

    def _get_slur_attachment_point(self, start: bool, slur) -> Tuple[int, int]:
        sign = -1 if start else 1
        y = slur.end_item.get_slur_end_attachment_point(slur)[1] if start \
            else slur.start_item.get_slur_start_attachment_point(slur)[1]
        return (
            self.sprites.position_x + sign * (self.sprites.width // 2 + 8),
            y
        )
