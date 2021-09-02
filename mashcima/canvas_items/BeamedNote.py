from mashcima import Mashcima
from mashcima.canvas_items.QuarterNote import QuarterNote
import copy


class BeamedNote(QuarterNote):
    def __init__(
            self,
            beams: int,
            left_beamed: bool,
            right_beamed: bool,
            **kwargs
    ):
        super().__init__(**kwargs)
        assert beams in [1, 2, 3]

        self.beams = beams
        self.left_beamed = left_beamed
        self.right_beamed = right_beamed

        # computed by the beam instance
        self.left_beam_count = 0
        self.right_beam_count = 0

        # reference to a beam instance set by the canvas when creating the beam
        self.beam = None

    def get_note_generic_annotation(self) -> str:
        SYMBOLS = {
            1: "e",
            2: "s",
            3: "t"
        }
        token = SYMBOLS[self.beams]
        if self.left_beamed:
            token = "=" + token
        if self.right_beamed:
            token += "="
        return token

    def select_sprites(self, mc: Mashcima):
        super().select_sprites(mc)

        # override flip -> pull it from the beam
        self.flipped = self.beam.flipped

    def update_sprites_for_stem_length(self, stem_length: int):
        self.sprites = copy.deepcopy(self.sprites)

        sign = -1 if self.flipped else 1

        stem = self.sprites.sprite("stem")
        lengthen = stem_length + stem.y
        if self.flipped:
            lengthen = stem_length - stem.y - stem.height
        if stem.height + lengthen < 1:
            lengthen = 1 - stem.height
            # Silence this warning because it happens quite often.
            # And the reason is that some notes have stems starting quite
            # far away from the notehead, therefore the scaled height
            # would be negative.
            # print("Stem length for beamed note clamped to minimal height.")
        stem.stretch_height(stem.height + lengthen)

        if not self.flipped:
            stem.y -= lengthen

        sh = self.sprites.point("stem_head")
        sh = (sh[0], sh[1] - sign * lengthen)
        self.sprites.add_point("stem_head", sh)

        self.sprites.recalculate_bounding_box()

    @property
    def global_stem_head(self):
        sh = self.sprites.point("stem_head")
        return self.sprites.position_x + sh[0], self.sprites.position_y + sh[1]
