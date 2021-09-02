import numpy as np
from typing import List, Optional
from mashcima.vocabulary import get_pitch, to_generic
from mashcima.vocabulary import is_accidental
from mashcima.vocabulary import parse_annotation_into_token_groups
from mashcima.vocabulary import KeySignatureTokenGroup, TimeSignatureTokenGroup, TokenGroup
from mashcima.SymbolRepository import SymbolRepository
from mashcima.Canvas import Canvas
from mashcima.canvas_items.Barline import Barline
from mashcima.canvas_items.Clef import Clef
from mashcima.canvas_items.Rest import Rest
from mashcima.canvas_items.WholeNote import WholeNote
from mashcima.canvas_items.HalfNote import HalfNote
from mashcima.canvas_items.QuarterNote import QuarterNote
from mashcima.canvas_items.FlagNote import FlagNote
from mashcima.canvas_items.BeamedNote import BeamedNote
from mashcima.canvas_items.WholeTimeSignature import WholeTimeSignature
from mashcima.canvas_items.TimeSignature import TimeSignature
from mashcima.canvas_items.KeySignature import KeySignature


ITEM_CONSTRUCTORS = {
    "|": Barline,

    "clef.G": lambda **kwargs: Clef(clef="G", **kwargs),
    "clef.F": lambda **kwargs: Clef(clef="F", **kwargs),
    "clef.C": lambda **kwargs: Clef(clef="C", **kwargs),

    "time.C": lambda **kwargs: WholeTimeSignature(crossed=False, **kwargs),
    "time.C/": lambda **kwargs: WholeTimeSignature(crossed=True, **kwargs),
    # numeric time signatures are created in a special way

    "w": WholeNote,
    "h": HalfNote,
    "q": QuarterNote,
    "e": lambda **kwargs: FlagNote(flag_kind="e", **kwargs),
    "s": lambda **kwargs: FlagNote(flag_kind="s", **kwargs),

    "lr": lambda **kwargs: Rest(rest_kind="lr", **kwargs),
    "br": lambda **kwargs: Rest(rest_kind="br", **kwargs),
    "wr": lambda **kwargs: Rest(rest_kind="wr", **kwargs),
    "hr": lambda **kwargs: Rest(rest_kind="hr", **kwargs),
    "qr": lambda **kwargs: Rest(rest_kind="qr", **kwargs),
    "er": lambda **kwargs: Rest(rest_kind="er", **kwargs),
    "sr": lambda **kwargs: Rest(rest_kind="sr", **kwargs),

    "e=": lambda **kwargs: BeamedNote(beams=1, left_beamed=False, right_beamed=True, **kwargs),
    "=e=": lambda **kwargs: BeamedNote(beams=1, left_beamed=True, right_beamed=True, **kwargs),
    "=e": lambda **kwargs: BeamedNote(beams=1, left_beamed=True, right_beamed=False, **kwargs),

    "s=": lambda **kwargs: BeamedNote(beams=2, left_beamed=False, right_beamed=True, **kwargs),
    "=s=": lambda **kwargs: BeamedNote(beams=2, left_beamed=True, right_beamed=True, **kwargs),
    "=s": lambda **kwargs: BeamedNote(beams=2, left_beamed=True, right_beamed=False, **kwargs),

    "t=": lambda **kwargs: BeamedNote(beams=3, left_beamed=False, right_beamed=True, **kwargs),
    "=t=": lambda **kwargs: BeamedNote(beams=3, left_beamed=True, right_beamed=True, **kwargs),
    "=t": lambda **kwargs: BeamedNote(beams=3, left_beamed=True, right_beamed=False, **kwargs),
}


def token_groups_to_canvas(canvas: Canvas, groups: List[TokenGroup]):
    """Appends token groups to a canvas instance"""
    for group in groups:

        # special token groups
        if isinstance(group, TimeSignatureTokenGroup):
            canvas.add(TimeSignature(
                top=int(group.first_token[len("time."):]),
                bottom=int(group.second_token[len("time."):])
            ))
            continue
        if isinstance(group, KeySignatureTokenGroup):
            canvas.add(KeySignature(
                types=[to_generic(a) for a in group.before_attachments],
                pitches=[get_pitch(a) for a in group.before_attachments]
            ))
            continue

        # default token group
        accidental = None
        accidentals = [b for b in group.before_attachments if is_accidental(b)]
        if len(accidentals) > 0:
            accidental = to_generic(accidentals[0])

        duration_dots = None
        if "*" in group.after_attachments:
            duration_dots = "*"
        elif "**" in group.after_attachments:
            duration_dots = "**"

        canvas.add(ITEM_CONSTRUCTORS[to_generic(group.token)](**{
            "pitch": get_pitch(group.token),
            "accidental": accidental,
            "duration_dots": duration_dots,
            "staccato": "." in group.after_attachments,
            "slur_start": "(" in group.after_attachments,
            "slur_end": ")" in group.before_attachments,
        }))


def annotation_to_canvas(canvas: Canvas, annotation: str, print_warnings=True):
    """Appends symbols in annotation to the canvas"""

    groups, warnings = parse_annotation_into_token_groups(annotation)

    if print_warnings and len(warnings) > 0:
        print("Warnings when parsing: " + annotation)
        print("\t" + "\t\n".join(warnings))

    token_groups_to_canvas(canvas, groups)

    # make sure the canvas produced what it was supposed to produce
    given_annotation = " ".join(annotation.split())
    generated_annotation = " ".join(canvas.get_annotations())
    if given_annotation != generated_annotation:
        print("Canvas generated different annotation from the one given:")
        print("Given: ", given_annotation)
        print("Generated: ", generated_annotation)
        assert given_annotation == generated_annotation  # kill the program


def annotation_to_image(repo: SymbolRepository, annotation: str) -> np.ndarray:
    """Generates an image from an annotation string"""
    canvas = Canvas()

    annotation_to_canvas(canvas, annotation)

    img = canvas.render(repo)

    return img


def multi_staff_annotation_to_image(
        repo: SymbolRepository,
        main_annotation: str,
        above_annotation: Optional[str],
        below_annotation: Optional[str],
        min_width=0,  # keep some empty staff lines after the end
        crop_horizontally=True,
        crop_vertically=True,
        transform_image=True
) -> np.ndarray:
    """
    Advanced function that creates image of a staff with staves above and
    below and applies transformations if requested.
    """
    from mashcima.generate_staff_lines import generate_staff_lines
    from mashcima.transform_image import transform_image as transform_image_function

    staff_img, pitch_positions = generate_staff_lines()
    staff_height = staff_img.shape[0] // 3
    staff_width = staff_img.shape[1]

    img = np.zeros(
        shape=(staff_height * 9, staff_width),
        dtype=np.float32
    )

    # draw staff lines
    if above_annotation is not None:
        img[staff_height * 1:staff_height * 4, :] = staff_img
    img[staff_height * 3:staff_height * 6, :] = staff_img
    if below_annotation is not None:
        img[staff_height * 5:staff_height * 8, :] = staff_img

    # draw above staff symbols
    if above_annotation is not None:
        canvas = Canvas()
        canvas.options.barlines_up = False
        canvas.options.barlines_down = False
        annotation_to_canvas(canvas, above_annotation)
        canvas.render_onto_image(
            repo, img,
            {pitch: y + staff_height * 1 for pitch, y in pitch_positions.items()},
            head_start=0
        )

    # draw main staff symbols
    canvas = Canvas()
    canvas.options.barlines_up = above_annotation is not None
    canvas.options.barlines_down = below_annotation is not None
    annotation_to_canvas(canvas, main_annotation)
    head_end = canvas.render_onto_image(
        repo, img,
        {pitch: y + staff_height * 3 for pitch, y in pitch_positions.items()},
        head_start=0
    )

    # draw below staff symbols
    if below_annotation is not None:
        canvas = Canvas()
        canvas.options.barlines_up = False
        canvas.options.barlines_down = False
        annotation_to_canvas(canvas, below_annotation)
        canvas.render_onto_image(
            repo, img,
            {pitch: y + staff_height * 5 for pitch, y in pitch_positions.items()},
            head_start=0
        )

    # minimal length
    if head_end < min_width:
        head_end = min_width

    # cropping box
    box = [
        0,  # x
        staff_height * 3 if crop_vertically else 0,  # y
        head_end if crop_horizontally else staff_width,  # width
        staff_height * 3 if crop_vertically else img.shape[0]  # height
    ]

    # transform or just crop
    if transform_image:
        img = transform_image_function(img, box)
    else:
        img = img[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]

    return img
