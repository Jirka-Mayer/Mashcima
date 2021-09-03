import numpy as np
from mashcima.SymbolRepository import SymbolRepository
import matplotlib.pyplot as plt
from mashcima.Canvas import Canvas
import random
from mashcima.annotation_to_image import annotation_to_canvas
from mashcima.vocabulary import PITCHES


repo = SymbolRepository([
    "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
    "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
])
# repo = SymbolRepository()


def inspect(generator, samples=10):
    for _ in range(samples):
        canvas = Canvas()
        canvas.options.random_space_probability = 0  # disable random spaces

        generator(canvas)

        img = canvas.render(repo)
        annotation = " ".join(canvas.get_annotations())

        print(annotation)
        plt.imshow(img)
        #plt.savefig("test_1.pdf", dpi=300, bbox_inches="tight")
        plt.show()


###############
# INSPECTIONS #
###############


def whole_notes(canvas):
    annotation_to_canvas(canvas, " ".join(["w" + str(i) for i in PITCHES]))


def half_notes(canvas):
    annotation_to_canvas(canvas, " ".join(
        ["h" + str(i) for i in PITCHES] +
        ["h0" for _ in range(6)]
    ))


def quarter_notes(canvas):
    annotation_to_canvas(canvas, " ".join(
        ["q" + str(i) for i in PITCHES] +
        ["q0" for _ in range(6)]
    ))


def eighth_notes(canvas):
    annotation_to_canvas(canvas, " ".join(
        ["e" + str(i) for i in PITCHES] +
        ["e0" for _ in range(6)]
    ))


def sixteenth_notes(canvas):
    annotation_to_canvas(canvas, " ".join(
        ["s" + str(i) for i in PITCHES] +
        ["s0" for _ in range(6)]
    ))


def rests(canvas):
    annotation_to_canvas(
        canvas,
        "lr lr br br wr wr hr hr qr qr er er sr sr"
    )


def bar_lines(canvas):
    # TODO bar lines that stretch only up or only down
    # TODO repeat bar lines
    # TODO double bar lines
    # TODO thick bar lines
    annotation_to_canvas(canvas, " ".join(["|" for _ in range(20)]))


def clefs(canvas):
    annotation_to_canvas(
        canvas,
        "clef.G-4 clef.G-2 clef.F0 clef.F2 clef.F3 " +
        "clef.C-4 clef.C-2 clef.C0 clef.C2 clef.C4"
    )


def time_signature(canvas):
    annotation_to_canvas(
        canvas,
        "time.C time.C/ time.0 time.1 time.2 time.3 time.4 time.5 time.6 " +
        "time.7 time.8 time.9"
    )


def key_signature(canvas):
    annotation_to_canvas(
        canvas,
        "#-4 b-2 N0 | #-4 b-2 N0 | b-1 b2 b-2 b1"
    )


def accidentals(canvas):
    annotation_to_canvas(canvas, "#-4 q-4 b-2 q-2 N0 q0 | #-4 q-4 b-2 q-2 N0 q0")


def sharps(canvas):
    annotation_to_canvas(canvas, " ".join(
        ["#" + str(i) + " q" + str(i) for i in PITCHES]
    ))


def flats(canvas):
    annotation_to_canvas(canvas, " ".join(
        ["b" + str(i) + " q" + str(i) for i in PITCHES]
    ))


def naturals(canvas):
    annotation_to_canvas(canvas, " ".join(
        ["N" + str(i) + " q" + str(i) for i in PITCHES]
    ))


def note_duration_dots(canvas):
    annotation_to_canvas(canvas, "q-2 * q0 * e=-2 * =s0 q-1 * | q6 * q8 *")


def note_duration_double_dots(canvas):
    annotation_to_canvas(canvas, "q-2 ** q0 ** e=-2 ** =s0 q-1 ** | q6 ** q8 **")


def rest_duration_dots(canvas):
    annotation_to_canvas(canvas, "lr * br * wr * hr * qr * er * sr *")


def rest_duration_double_dots(canvas):
    annotation_to_canvas(canvas, "lr ** br ** wr ** hr ** qr ** er ** sr **")


def staccato(canvas):
    annotation_to_canvas(
        canvas,
        "q-2 . q0 . e=-2 . =s0 q-1 . | q6 . q8 ."
    )


# ================= BEAMS =================


def single_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "e=-4 =e-4 | e=-4 =e=-4 =e=0 =e-4 | " +
        "e=4 =e4 | e=4 =e=4 =e=0 =e4"
    )


def double_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "s=-4 =s-4 | s=-4 =s=-4 =s=0 =s-4 | " +
        "s=4 =s4 | s=4 =s=4 =s=0 =s4"
    )


def single_to_double_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "e=-4 =s=-4 =s=-2 =e-4 | e=-2 =s0 | s=0 =e2 | "
        "e=-4 =s=-4 =e=-2 =s-4 | e=-4 =s-4 e=-2 =s-4"
    )


def triple_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "t=-4 =t-4 | t=-4 =t=-4 =t=0 =t-4 | " +
        "t=4 =t4 | t=4 =t=4 =t=0 =t4"
    )


def double_to_triple_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "s=-4 =t=-4 =t=-2 =s-4 | s=-2 =t0 | t=0 =s2 | "
        "s=-4 =t=-4 =s=-2 =t-4 | s=-4 =t-4 s=-2 =t-4"
    )


def single_to_triple_beam_group(canvas):
    annotation_to_canvas(
        canvas,
        "e=-4 =t=-4 =t=-2 =e-4 | e=-2 =t0 | t=0 =e2 | "
        "e=-4 =t=-4 =e=-2 =t-4 | e=-4 =t-4 e=-2 =t-4"
    )


# ================= SLURS =================


def simple_slurs(canvas):
    annotation_to_canvas(
        canvas,
        " q-4 ( ) q-4 " + " q4 ( ) q4 " + " q-8 ( ) q-4 " + " q-4 ( ) q-8 " +
        " q-4 ( ) q4 " + " q4 ( ) q-4 " + " q4 ( ) | " + " qr " + " | ( ) q-4"
    )


def joined_slurs(canvas):
    annotation_to_canvas(
        canvas,
        "q-2 ( ) q-2 ( ) q-2 ( ) q-2 " +
        " q-2 ( q-2 q-2 ) q-2"
    )


def nested_slurs(canvas):
    annotation_to_canvas(canvas, "q-4 ( q-2 ( ) q-2 ) q-4")


def staff_beginning_slur(canvas):
    annotation_to_canvas(
        canvas,
        "qr ) q-2 q2 ( qr qr"
    )


##################################
# Running individual inspections #
##################################

inspect(whole_notes, 1)
# inspect(half_notes, 1)
# inspect(quarter_notes, 1)
# inspect(eighth_notes, 1)
# inspect(sixteenth_notes, 1)
#
# inspect(rests, 1)
#
# inspect(bar_lines, 1)
# inspect(clefs, 1)
# inspect(time_signature, 1)
# inspect(key_signature, 1)
#
# inspect(accidentals, 1)
# inspect(sharps, 1)
# inspect(flats, 1)
# inspect(naturals, 1)

# inspect(note_duration_dots, 1)
# inspect(note_duration_double_dots, 1)
# inspect(rest_duration_dots, 1)
# inspect(rest_duration_double_dots, 1)
# inspect(staccato, 1)
# TODO: note duration dots (one, two) -> update slur attachment points
# TODO: rest duration dots (one, two) -> update slur attachment points
# TODO: staccato -> update slur attachment points

# inspect(single_beam_group, 1)
# inspect(double_beam_group, 1)
# inspect(single_to_double_beam_group, 1)
# inspect(triple_beam_group, 1)
# inspect(double_to_triple_beam_group, 1)
# inspect(single_to_triple_beam_group, 1)
#
# inspect(simple_slurs, 1)
# inspect(joined_slurs, 1)
# inspect(nested_slurs, 1)
# inspect(staff_beginning_slur, 1)

# TODO: fermata
