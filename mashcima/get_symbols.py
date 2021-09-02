import numpy as np
from mashcima.utils import has_outlink_to, get_outlink_to
from mashcima.utils import get_connected_components_not_touching_image_border
from mashcima.utils import sort_components_by_proximity_to_point
from mashcima.utils import get_center_of_component
from mashcima import Mashcima
from mashcima.Sprite import Sprite
from mashcima.SpriteGroup import SpriteGroup
from typing import List, Tuple, Dict
from muscima.io import CropObject
import cv2


###################
# Utility methods #
###################


def _build_notehead_stem_pairs(noteheads, stems, flags8=None, flags16=None):
    """
    Combines list of noteheads and a list of stems into a list of
    canvas items. Handles flipping when stem points down.
    """
    items = []
    for i, h in enumerate(noteheads):
        if len(stems[i].inlinks) > 1:
            continue  # skip chords (the stem would go below the notehead)

        # compute some absolute points
        stem_center_y = (stems[i].top + stems[i].bottom) // 2
        notehead_center_x = (h.left + h.right) // 2
        notehead_center_y = (h.top + h.bottom) // 2

        # determine whether to flip the note
        flip = stem_center_y > notehead_center_y

        # place sprites (notehead and stem)
        item = SpriteGroup()
        item.add("notehead", Sprite(
            h.left - notehead_center_x,
            h.top - notehead_center_y,
            h.mask
        ))
        item.add("stem", Sprite(
            stems[i].left - notehead_center_x,
            stems[i].top - notehead_center_y,
            stems[i].mask
        ))
        if flags8 is not None:
            item.add("flag_8", Sprite(
                flags8[i].left - notehead_center_x,
                flags8[i].top - notehead_center_y,
                flags8[i].mask
            ))
        if flags16 is not None:
            item.add("flag_16", Sprite(
                flags16[i].left - notehead_center_x,
                flags16[i].top - notehead_center_y,
                flags16[i].mask
            ))

        if flip:
            item = item.create_flipped_copy()

            if flags8 is not None:
                f = item.sprite("flag_8")
                f.mask = np.flip(f.mask, axis=1)
                f.x += f.width

            if flags16 is not None:
                f = item.sprite("flag_16")
                f.mask = np.flip(f.mask, axis=1)
                f.x += f.width

        stem_sprite = item.sprite("stem")
        item.add_point("stem_head", (
            stem_sprite.x + np.argmax(stem_sprite.mask[0, :]),
            stem_sprite.y
        ))

        items.append(item)

    return items


def _get_y_position_of_staff_line(
        mc: Mashcima,
        obj: CropObject,
        line_from_top: int = 0
):
    """
    Given a CropObject it finds the y-coordinate of the corresponding staff line
    """
    staff = get_outlink_to(mc, obj, "staff")
    staff_line = None
    line = 0
    for l in staff.outlinks:
        resolved_link = mc.CROP_OBJECT_LOOKUP_DICTS[obj.doc][l]
        if resolved_link.clsname == "staff_line":
            if line == line_from_top:  # counted from top, from zero
                staff_line = resolved_link
                break
            line += 1
    assert staff_line is not None
    return (staff_line.top + staff_line.bottom) // 2


def _get_symbols_centered_on_line(
        mc: Mashcima,
        clsname: str,
        sprite_name: str,
        line_index: int,
        when_center_outside_recenter: bool = False
) -> List[SpriteGroup]:
    """
    Returns list of symbols with given clsname centered on given line index
    """
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in [clsname]
    ]

    items = []
    for o in crop_objects:
        item = SpriteGroup()
        sprite = Sprite(
            -o.width // 2,
            o.top - _get_y_position_of_staff_line(mc, o, line_from_top=line_index),
            o.mask
        )
        item.add(sprite_name, sprite)
        items.append(item)

        if (-sprite.y < 0 or -sprite.y > sprite.height) and when_center_outside_recenter:
            sprite.y = -sprite.height // 2

    return items


################################################
# Code that actually extracts required symbols #
################################################


def get_whole_notes(mc: Mashcima) -> List[SpriteGroup]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-empty"
        and not has_outlink_to(mc, o, "ledger_line")
    ]

    items = []
    for o in crop_objects:
        item = SpriteGroup()
        item.add("notehead", Sprite(
            -o.width // 2,
            -o.height // 2,
            o.mask
        ))
        items.append(item)

    return items


def get_half_notes(mc: Mashcima) -> List[SpriteGroup]:
    noteheads = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-empty"
        and has_outlink_to(mc, o, "stem")
        and not has_outlink_to(mc, o, "ledger_line")
    ]
    stems = [get_outlink_to(mc, o, "stem") for o in noteheads]
    return _build_notehead_stem_pairs(noteheads, stems)


def get_quarter_notes(mc: Mashcima) -> List[SpriteGroup]:
    noteheads = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-full"
        and has_outlink_to(mc, o, "stem")
    ]
    stems = [get_outlink_to(mc, o, "stem") for o in noteheads]
    return _build_notehead_stem_pairs(noteheads, stems)


def get_eighth_notes(mc: Mashcima) -> List[SpriteGroup]:
    noteheads = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-full"
           and has_outlink_to(mc, o, "stem")
           and has_outlink_to(mc, o, "8th_flag")
    ]
    stems = [get_outlink_to(mc, o, "stem") for o in noteheads]
    flags = [get_outlink_to(mc, o, "8th_flag") for o in noteheads]
    return _build_notehead_stem_pairs(noteheads, stems, flags)


def get_sixteenth_notes(mc: Mashcima) -> List[SpriteGroup]:
    noteheads = [
        o for o in mc.CROP_OBJECTS
        if o.clsname == "notehead-full"
           and has_outlink_to(mc, o, "stem")
           and has_outlink_to(mc, o, "8th_flag")
           and has_outlink_to(mc, o, "16th_flag")
    ]
    stems = [get_outlink_to(mc, o, "stem") for o in noteheads]
    flags8 = [get_outlink_to(mc, o, "8th_flag") for o in noteheads]
    flags16 = [get_outlink_to(mc, o, "16th_flag") for o in noteheads]
    return _build_notehead_stem_pairs(noteheads, stems, flags8, flags16)


def get_longa_rests(mc: Mashcima) -> List[SpriteGroup]:
    HEIGHT_THRESHOLD = 44  # split longas from breves
    rests = _get_symbols_centered_on_line(
        mc,
        clsname="multi-measure_rest",
        sprite_name="rest",
        line_index=2
    )
    return list(filter(lambda r: r.sprite("rest").height > HEIGHT_THRESHOLD, rests))


def get_breve_rests(mc: Mashcima) -> List[SpriteGroup]:
    HEIGHT_THRESHOLD = 44  # split longas from breves
    rests = _get_symbols_centered_on_line(
        mc,
        clsname="multi-measure_rest",
        sprite_name="rest",
        line_index=2
    )
    return list(filter(lambda r: r.sprite("rest").height <= HEIGHT_THRESHOLD, rests))


def get_whole_rests(mc: Mashcima) -> List[SpriteGroup]:
    rests = _get_symbols_centered_on_line(
        mc,
        clsname="whole_rest",
        sprite_name="rest",
        line_index=1
    )
    for group in rests:
        sprite = group.sprite("rest")
        if -sprite.y < -sprite.height // 2 or -sprite.y > sprite.height // 2:
            sprite.y = 0
    return rests


def get_half_rests(mc: Mashcima) -> List[SpriteGroup]:
    rests = _get_symbols_centered_on_line(
        mc,
        clsname="half_rest",
        sprite_name="rest",
        line_index=2
    )
    for group in rests:
        sprite = group.sprite("rest")
        if -sprite.y < sprite.height // 2 or -sprite.y > sprite.height * 1.5:
            sprite.y = -sprite.height
    return rests


def get_quarter_rests(mc: Mashcima) -> List[SpriteGroup]:
    return _get_symbols_centered_on_line(
        mc,
        clsname="quarter_rest",
        sprite_name="rest",
        line_index=2,
        when_center_outside_recenter=True
    )


def get_eighth_rests(mc: Mashcima) -> List[SpriteGroup]:
    return _get_symbols_centered_on_line(
        mc,
        clsname="8th_rest",
        sprite_name="rest",
        line_index=2,
        when_center_outside_recenter=True
    )


def get_sixteenth_rests(mc: Mashcima) -> List[SpriteGroup]:
    return _get_symbols_centered_on_line(
        mc,
        clsname="16th_rest",
        sprite_name="rest",
        line_index=2,
        when_center_outside_recenter=True
    )


def get_accidentals(mc: Mashcima) -> Tuple[List[Sprite], List[Sprite], List[Sprite]]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["sharp", "flat", "natural"]
    ]

    sharps = []
    flats = []
    naturals = []
    
    for o in crop_objects:
        # obtain sprite from the center of the inner component
        # and handle open accidentals by repeatedly dilating
        # (dilate vertically twice as much)
        object_center_x, object_center_y = get_center_of_component(o.mask)
        mask = (o.mask * 255).astype(dtype=np.uint8)
        sprite = None
        for i in range(5):
            components = get_connected_components_not_touching_image_border(
                1 - (mask // 255)
            )
            components = sort_components_by_proximity_to_point(
                components,
                object_center_x,
                object_center_y
            )

            if len(components) == 0:
                kernel = np.ones((5, 3), np.uint8)
                mask = cv2.dilate(mask, kernel, iterations=1)
                continue

            component_center_x, component_center_y = get_center_of_component(
                components[0]
            )
            sprite = Sprite(
                -component_center_x,
                -component_center_y,
                o.mask
            )
            break

        # if it didn't succeed, try pulling the center out by the attached note
        if sprite is None and len(o.inlinks) == 1:
            link = mc.CROP_OBJECT_LOOKUP_DICTS[o.doc][o.inlinks[0]]
            if "notehead" in link.clsname:
                sprite = Sprite(
                    -o.width // 2,
                    o.top - ((link.top + link.bottom) // 2),
                    o.mask
                )

        # still nothing, so resort to the crudest method possible
        if sprite is None:
            if o.clsname == "flat":
                sprite = Sprite(
                    -o.width // 2,
                    -int(o.height * 0.75),
                    o.mask
                )
            else:
                sprite = Sprite(
                    -o.width // 2,
                    -o.height // 2,
                    o.mask
                )

        if o.clsname == "sharp":
            sharps.append(sprite)
        elif o.clsname == "flat":
            flats.append(sprite)
        elif o.clsname == "natural":
            naturals.append(sprite)

    return sharps, flats, naturals


def get_dots(mc: Mashcima) -> List[Sprite]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["duration-dot", "staccato-dot", "other-dot"]
    ]

    dots = []
    for o in crop_objects:
        object_center_x, object_center_y = get_center_of_component(o.mask)
        dots.append(Sprite(
            -object_center_x,
            -object_center_y,
            o.mask
        ))

    return dots


def get_ledger_lines(mc: Mashcima) -> List[Sprite]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["ledger_line"]
    ]

    lines = []
    for o in crop_objects:
        if o.mask.sum() == 0:
            print("Skipping invalid ledger line: ", o.uid)
            continue
        object_center_x, object_center_y = get_center_of_component(o.mask)
        lines.append(Sprite(
            -object_center_x,
            -object_center_y,
            o.mask
        ))

    return lines


def get_barlines(mc: Mashcima) -> Tuple[List[SpriteGroup], List[SpriteGroup]]:
    TALL_BARLINE_THRESHOLD = 150

    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["thin_barline"]
    ]

    items = []
    for o in crop_objects:
        item = SpriteGroup()
        item.add("barline", Sprite(
            -o.width // 2,
            -o.height // 2,
            o.mask,
            print_render_warnings=(False if o.height > 350 else True)
        ))
        item.recalculate_bounding_box()  # needed for .height to be set
        items.append(item)

    return (
        list(filter(lambda i: i.height < TALL_BARLINE_THRESHOLD, items)),
        list(filter(lambda i: i.height >= TALL_BARLINE_THRESHOLD, items))
    )


def get_g_clefs(mc: Mashcima) -> List[SpriteGroup]:
    return _get_symbols_centered_on_line(
        mc,
        clsname="g-clef",
        sprite_name="clef",
        line_index=3
    )


def get_f_clefs(mc: Mashcima) -> List[SpriteGroup]:
    return _get_symbols_centered_on_line(
        mc,
        clsname="f-clef",
        sprite_name="clef",
        line_index=1
    )


def get_c_clefs(mc: Mashcima) -> List[SpriteGroup]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["c-clef"]
    ]

    items = []
    for o in crop_objects:
        item = SpriteGroup()
        item.add("clef", Sprite(
            -o.width // 2,
            -o.height // 2,
            o.mask
        ))
        items.append(item)

    return items


def get_time_marks(mc: Mashcima) -> Dict[str, List[SpriteGroup]]:
    crop_objects = [
        o for o in mc.CROP_OBJECTS
        if o.clsname in ["time_signature"]
    ]

    KEY_MAP = {
        "numeral_0": "time_0",
        "numeral_1": "time_1",
        "numeral_2": "time_2",
        "numeral_3": "time_3",
        "numeral_4": "time_4",
        "numeral_5": "time_5",
        "numeral_6": "time_6",
        "numeral_7": "time_7",
        "numeral_8": "time_8",
        "numeral_9": "time_9",
        "whole-time_mark": "time_c",
    }

    items = {
        "time_0": [],
        "time_1": [],
        "time_2": [],
        "time_3": [],
        "time_4": [],
        "time_5": [],
        "time_6": [],
        "time_7": [],
        "time_8": [],
        "time_9": [],
        "time_c": [],
    }

    for o in crop_objects:
        for l in o.outlinks:
            outlink = mc.CROP_OBJECT_LOOKUP_DICTS[o.doc][l]
            if outlink.clsname == "staff":
                continue
            item = SpriteGroup()
            item.add("symbol", Sprite(
                -outlink.width // 2,
                -outlink.height // 2,
                outlink.mask
            ))
            items[KEY_MAP[outlink.clsname]].append(item)

    return items
