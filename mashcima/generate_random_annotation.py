from typing import List, Optional
from mashcima.vocabulary import PITCHES, HIGHEST_PITCH, LOWEST_PITCH
from mashcima.vocabulary import TokenGroup, TimeSignatureTokenGroup, KeySignatureTokenGroup
from mashcima.vocabulary import validate_annotation, stringify_token_groups_to_annotation
from mashcima.vocabulary import is_note, is_barline, get_pitch
import random


def generate_random_annotation() -> str:
    # create items
    count = random.randint(5, 15)
    groups: List[TokenGroup] = []
    previous_group = None
    i = 0
    while i < count:
        if random.random() < 0.1 and i + 2 < count:
            # beamed group
            beamed_group_length = random.randint(2, min(count - i, 8))
            if random.random() < 0.1:  # boost 2-beams
                beamed_group_length = 2
            groups += _generate_beamed_group(beamed_group_length, previous_group)
            i += beamed_group_length
        else:
            # simple token
            groups.append(_generate_simple_token_group(previous_group))
            i += 1
        previous_group = groups[-1]

    # add slurs
    in_slur = False
    slur_start = None
    for group in groups:
        if not _is_slurable(group):
            continue
        if not in_slur:
            if random.random() < 0.3:
                in_slur = True
                slur_start = group
        else:
            if random.random() < 0.3:
                slur_start.after_attachments.append("(")
                group.before_attachments = [")"] + group.before_attachments
                in_slur = False

    annotation = stringify_token_groups_to_annotation(groups)

    validate_annotation(annotation)
    return annotation


def _is_slurable(group: TokenGroup) -> bool:
    return is_note(group.token)# or is_barline(group.token)


def _generate_beamed_group(length: int, previous_group: Optional[TokenGroup]) -> List[TokenGroup]:
    assert length >= 2

    groups = []
    pitches = _generate_beamed_group_pitches(length)
    for i in range(length):
        left_beamed = "=" if i > 0 else ""
        right_beamed = "=" if i < length - 1 else ""
        kind = random.choice(["e", "s", "t"])
        groups.append(_generate_note(
            kind=left_beamed + kind + right_beamed,
            pitch=pitches[i],
            previous_group=previous_group
        ))
        previous_group = groups[-1]

    return groups


def _generate_beamed_group_pitches(length: int) -> List[int]:
    HALF_SPREAD = 4
    center = random.randint(LOWEST_PITCH + HALF_SPREAD, HIGHEST_PITCH - HALF_SPREAD)
    return [center + random.randint(-HALF_SPREAD, HALF_SPREAD) for _ in range(length)]


_SIMPLE_TOKEN_GROUP_CONSTRUCTORS = [
    *(["|"] * 5),
    #"|:",
    #":|",

    lambda **kwargs: _generate_clef(),
    lambda **kwargs: _generate_time_signature(),
    lambda **kwargs: _generate_key_signature(),

    lambda **kwargs: _generate_some_rest(),

    *([lambda **kwargs: _generate_some_note(**kwargs)] * 3),
]


def _generate_simple_token_group(previous_group: Optional[TokenGroup]) -> TokenGroup:
    """Generates notes, rests, clefs, time signature, barlines, key signatures"""
    constructor = random.choice(_SIMPLE_TOKEN_GROUP_CONSTRUCTORS)

    if isinstance(constructor, str):
        return TokenGroup(token=constructor)

    result = constructor(previous_group=previous_group)

    if isinstance(result, str):
        return TokenGroup(token=result)

    return result


def _generate_some_rest() -> TokenGroup:
    kind = random.choice([
        "lr", "br", "wr", "hr", "qr", "er", "sr",
        # "tr",
    ])
    duration_dots = random.choice([
        *([[]] * 10),
        *([["*"]] * 5),
        *([["**"]] * 1)
    ])
    return TokenGroup(
        token=kind,
        after_attachments=[*duration_dots]
    )


def _generate_some_note(previous_group: Optional[TokenGroup]) -> TokenGroup:
    return _generate_note(random.choice([
        "w", "h", "q", "e", "s",  # "t"
    ]), None, previous_group)


def _generate_note(
        kind: str,
        pitch: Optional[int] = None,
        previous_group: Optional[TokenGroup] = None
) -> TokenGroup:
    if pitch is None:
        pitch = str(_generate_random_pitch())
    else:
        pitch = str(pitch)
    accidental = random.choice([
        *([[]] * 10),
        *([["#" + pitch]] * 1),
        *([["b" + pitch]] * 1),
        *([["N" + pitch]] * 1)
    ])
    # never generate an accidental after a key signature
    if previous_group is not None and isinstance(previous_group, KeySignatureTokenGroup):
        accidental = []
        # also the note pitch has to differ from the last accidental in the key signature
        while pitch == str(get_pitch(previous_group.before_attachments[-1])):
            pitch = str(_generate_random_pitch())
    duration_dots = random.choice([
        *([[]] * 10),
        *([["*"]] * 5),
        *([["**"]] * 1)
    ])
    staccato_dot = random.choice([
        *([[]] * 5),
        *([["."]] * 1)
    ])
    return TokenGroup(
        token=kind + pitch,
        before_attachments=[*accidental],
        after_attachments=[*staccato_dot, *duration_dots]
    )


def _generate_random_pitch() -> int:
    return random.choice(PITCHES)


def _generate_clef() -> str:
    if random.random() < 0.2:
        return "clef.G-2"
    if random.random() < 0.2:
        return "clef.F2"
    if random.random() < 0.2:
        return "clef.C0"
    if random.random() < 0.2:
        return "clef.C2"
    return random.choice([
        "clef.C4", "clef.C-2", "clef.C-4",
        "clef.F0", "clef.F3",
        "clef.G-4",
    ])


def _generate_time_signature() -> TokenGroup:
    if random.random() < 0.3:
        return TokenGroup(token="time.C")
    if random.random() < 0.1:
        return TokenGroup(token="time.C/")
    return TimeSignatureTokenGroup(
        first_number=TokenGroup(token="time." + str(random.randint(0, 9))),
        second_number=TokenGroup(token="time." + str(random.randint(0, 9))),
    )


def _generate_key_signature() -> TokenGroup:
    attachments = []
    for _ in range(random.randint(1, 8)):
        attachments.append(
            random.choice(["#", "b", "N"]) + str(random.randint(-4, 4))
        )

    return KeySignatureTokenGroup(TokenGroup(
        token="NOTHING",
        before_attachments=attachments
    ))
