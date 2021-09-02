from mashcima.canvas_items.SlurableItem import SlurableItem


class InvisibleSlurEnd(SlurableItem):
    def get_annotation_tokens(self):
        return []

    def contribute_to_padding(self):
        self.sprites.padding_left += 10
        self.sprites.padding_right += 10
