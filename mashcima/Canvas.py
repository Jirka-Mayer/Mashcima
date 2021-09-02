from typing import List, Optional, Dict
from mashcima import Mashcima
from mashcima.canvas_items.CanvasItem import CanvasItem
from mashcima.canvas_items.SlurableItem import SlurableItem
from mashcima.canvas_items.InvisibleSlurEnd import InvisibleSlurEnd
from mashcima.canvas_items.BeamedNote import BeamedNote
from mashcima.Slur import Slur
from mashcima.Beam import Beam
from mashcima.CanvasOptions import CanvasOptions
import numpy as np
import random


class Canvas:
    def __init__(self, options: Optional[CanvasOptions] = None):
        # items on the canvas
        self.items: List[CanvasItem] = []

        # beams between beamed notes
        self.beams: List[Beam] = []

        # slurs between items
        self.slurs: List[Slur] = []

        # was the construction finished or not
        self._construction_finished = False

        # options that alter how is the staff printed
        self.options = CanvasOptions() if options is None else options
        
    def add(self, item: CanvasItem):
        if self._construction_finished:
            raise Exception("Cannot add item, construction has been finished")
        self.items.append(item)
        item.set_canvas_options(self.options)

    def get_annotations(self) -> List[str]:
        out: List[str] = []
        for item in self.items:
            out += item.get_annotation_tokens()
        return out

    def finish_construction(self):
        """Creates additional data structures around canvas items"""
        if self._construction_finished:
            raise Exception("Construction has been already finished")

        self._create_beams()
        self._create_slurs()

    def _create_beams(self):
        self.beams = []

        in_beam = False
        beam_items = []
        for i in self.items:
            if not isinstance(i, BeamedNote):
                continue

            if in_beam:
                # append item to a built beam
                beam_items.append(i)

                # end the beam
                if not i.right_beamed:
                    self.beams.append(Beam(beam_items))
                    in_beam = False
                    beam_items = []

            else:
                # start new beam
                if i.right_beamed:
                    beam_items.append(i)
                    in_beam = True

        assert not in_beam, "Unfinished beam group added to the canvas"

    def _create_slurs(self):
        self.slurs = []
        slur_stack: List[SlurableItem] = []

        def add_slur(start: SlurableItem, end: SlurableItem):
            self.slurs.append(Slur(start, end))

        def create_invisible_slur_end(at_index: int, start_here: bool) -> SlurableItem:
            ise = InvisibleSlurEnd(
                slur_end=not start_here,
                slur_start=start_here
            )
            self.items.insert(at_index, ise)
            return ise

        # iterate over slurable items
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if isinstance(item, SlurableItem):

                if item.slur_end:
                    if len(slur_stack) == 0:  # slur ending out of nowhere
                        slur_stack.append(create_invisible_slur_end(i, True))
                        i += 1
                    add_slur(slur_stack.pop(), item)

                if item.slur_start:
                    slur_stack.append(item)

                pass  # here do something

            i += 1

        # slurs not ending anywhere
        while len(slur_stack) != 0:
            start = slur_stack.pop()
            end = create_invisible_slur_end(self.items.index(start) + 1, False)
            add_slur(start, end)

    def render(self, mc: Mashcima):
        """Simple rendering that creates a single cropped staff"""
        from mashcima.generate_staff_lines import generate_staff_lines
        img, pitch_positions = generate_staff_lines()
        head = self.render_onto_image(
            mc,
            img,
            pitch_positions,
            0
        )

        # crop the result
        img = img[:, 0:head]

        return img

    def render_onto_image(
            self,
            mc: Mashcima,
            img: np.ndarray,
            pitch_positions: Dict[int, int],
            head_start: int
    ) -> int:
        """More advanced rendering that renders onto a given staff image"""
        if not self._construction_finished:
            self.finish_construction()

        # select sprites
        for item in self.items:
            item.select_sprites(mc)

        # place sprites and place items
        head = self._place_items(pitch_positions, head_start)

        # place beams
        for b in self.beams:
            b.place()

        # render
        for item in self.items:
            item.render(img)

        for b in self.beams:
            b.render(img)

        for s in self.slurs:
            s.render(img)

        return head

    def _place_items(self, pitch_positions, head_start):
        """Move items to proper places in the pixel space"""
        for item in self.items:
            item.place_sprites()

        def generate_random_space():
            if self.options.random_space_probability == 0:
                return 0
            if random.random() < self.options.random_space_probability:
                return random.randint(*self.options.random_space_size)
            return 0

        def generate_padding():
            return random.randint(5, 25)

        head = head_start
        for i, item in enumerate(self.items):
            head += generate_random_space()
            head += generate_padding()  # left padding
            head += item.place_item(head, pitch_positions)
            head += generate_padding()  # right padding
        return head
