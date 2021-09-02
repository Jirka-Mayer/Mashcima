from typing import List, Optional, Tuple

# pitches that can be used for items that have pitches
HIGHEST_PITCH = 12  # fourth ledger line above
LOWEST_PITCH = -12  # fourth ledger line below
PITCHES = [str(pos) for pos in reversed(range(LOWEST_PITCH, HIGHEST_PITCH + 1))]

# Vocabulary representation with wildcards
#
# It contains more symbols than are actually generated or trained, to prepare
# ground for future expansion. These symbols are marked as NOT_GENERATED or
# are commented otherwise.
_WILDCARD_VOCABULARY = [
    # unknown symbol
    # Used for symbols that are not recognised, e.g. grace notes.
    # Not generated, should be present only in annotations of validation data.
    "?",

    # barlines
    "|",  # barline
    "|:",  # repeat start       NOT_GENERATED
    ":|",  # repeat end         NOT_GENERATED
    ":|:",  # repeat both       NOT_GENERATED

    # clefs
    "clef.C4",
    "clef.C2",
    "clef.C0",  # standard alto clef (middle sitting on position 0 (center line))
    "clef.C-2",
    "clef.C-4",
    "clef.F0",
    "clef.F2",  # standard bass clef (colon sitting on position 2 (line))
    "clef.F3",
    "clef.G-2",  # standard treble clef (curl sitting on position -2 (line))
    "clef.G-4",

    # time signatures
    "time.C",  # common (C) meter sign (shorthand for 4/4)
    "time.C/",  # crossed C meter sign (shorthand for 2/2)
    "time.0",
    "time.1",
    "time.2",
    "time.3",
    "time.4",
    "time.5",
    "time.6",
    "time.7",
    "time.8",
    "time.9",

    # accidentals & key signatures
    "#{p}",  # sharp
    "b{p}",  # flat
    "N{p}",  # natural
    "x{p}",  # double sharp         NOT_GENERATED
    "bb{p}",  # double flat         NOT_GENERATED

    # slurs
    "(",  # slur start
    ")",  # slur end

    # tuplets (number above a note)
    "tuplet.3",  # triplet          NOT_GENERATED

    # other before attachments
    "fermata",  # fermata           NOT_GENERATED
    "trill",  # trill               NOT_GENERATED
    "+",  # also trill              NOT_GENERATED

    # other after attachments
    ".",  # staccato dot
    "_",  # tenuto bar              NOT_GENERATED
    ">",  # accent                  NOT_GENERATED
    "^",  # marcato                 NOT_GENERATED
    "*",  # duration dot
    "**",  # duration double dot

    # rests
    "lr",  # longa rest (4 bars)
    "br",  # breve rest (2 bars)
    "wr",  # whole rest
    "hr",  # half rest
    "qr",  # quarter rest
    "er",  # eighth rest
    "sr",  # sixteenth rest
    "tr",  # thirty-two rest        NOT_GENERATED

    # notes
    "w{p}",  # whole note
    "h{p}",  # half note
    "q{p}",  # quarter note
    "e{p}",  # eighth note
    "s{p}",  # sixteenth note
    "t{p}",  # thirty-second note   NOT_GENERATED

    # beamed notes
    "=e{p}",  # beamed left eight note
    "=e={p}",  # beamed both eight note
    "e={p}",  # beamed left eight note

    "=s{p}",  # beamed left sixteenth note
    "=s={p}",  # beamed both sixteenth note
    "s={p}",  # beamed left sixteenth note

    "=t{p}",  # beamed left thirty-second note
    "=t={p}",  # beamed both thirty-second note
    "t={p}",  # beamed left thirty-second note
]

# the actual vocabulary
# These values are used for encoding model output.
VOCABULARY = []
for wild in _WILDCARD_VOCABULARY:
    if "{p}" in wild:
        VOCABULARY += [wild.replace("{p}", str(p)) for p in PITCHES]
    else:
        VOCABULARY.append(wild)

# check for duplicities
assert len(VOCABULARY) == len(set(VOCABULARY))


##########################
# Helper sets (internal) #
##########################

_ACCIDENTALS = [
    "#", "b", "N", "x", "bb"
]

_DURATION_DOTS = [
    "*", "**"
]

_BEFORE_ATTACHMENTS = [
    # order DOES matter!
    ")",
    "fermata", "trill", "+",
    "tuplet.3",
    *_ACCIDENTALS
]

_AFTER_ATTACHMENTS = [
    # order DOES matter!
    ".", "_", ">", "^",
    *_DURATION_DOTS,
    "("
]

# dictates in what order should attachments be placed around an item
_ATTACHMENT_ORDER = [
    *_BEFORE_ATTACHMENTS, *_AFTER_ATTACHMENTS
]

# all the attachment symbols
_ATTACHMENTS = _ATTACHMENT_ORDER

_BEAMED_NOTES = [
    "=e", "=e=", "e=",
    "=s", "=s=", "s=",
    "=t", "=t=", "t=",
]

_NOTES = [
    "w", "h", "q", "e", "s", "t",
    *_BEAMED_NOTES
]

_RESTS = [
    "lr", "br", "wr", "hr", "qr", "er", "sr", "tr"
]

_NUMERIC_TIME_SIGNATURE = [
    "time.0",
    "time.1",
    "time.2",
    "time.3",
    "time.4",
    "time.5",
    "time.6",
    "time.7",
    "time.8",
    "time.9",
]

_BARLINES = [
    "|", ":|", "|:"
]


###################
# Utility methods #
###################

def to_generic(annotation_token: str):
    """
    Converts an annotation token to it's generic version (pitch-less version).
    For generic tokens nothing happens.
    """
    # these tokens end with a digit, but it isn't a pitch
    if annotation_token.startswith("tuplet."):
        return annotation_token
    if annotation_token.startswith("time."):
        return annotation_token

    # remove digits at the end
    return annotation_token.rstrip("-0123456789")


def get_pitch(annotation_token: str) -> Optional[int]:
    """Returns pitch of a token or None if it has no pitch or is generic"""
    generic = to_generic(annotation_token)
    pitch_string = annotation_token[len(generic):]
    if pitch_string == "":
        return None
    return int(pitch_string)


def is_before_attachment(annotation_token: str) -> bool:
    """Returns true if the token is a before attachment (generic or not)"""
    return to_generic(annotation_token) in _BEFORE_ATTACHMENTS


def is_after_attachment(annotation_token: str) -> bool:
    """Returns true if the token is a before attachment (generic or not)"""
    return to_generic(annotation_token) in _AFTER_ATTACHMENTS


def is_attachment(annotation_token: str) -> bool:
    """Returns true if the token is an attachment (generic or not)"""
    return to_generic(annotation_token) in _ATTACHMENTS


def is_duration_dot(annotation_token: str) -> bool:
    """Returns true if the token is a duration dot"""
    return annotation_token in _DURATION_DOTS


def is_note(annotation_token: str) -> bool:
    """Returns true if the token is a note (generic or not)"""
    return to_generic(annotation_token) in _NOTES


def is_beamed_note(annotation_token: str) -> bool:
    """Returns true if the token is a beamed note (generic or not)"""
    return to_generic(annotation_token) in _BEAMED_NOTES


def is_rest(annotation_token: str) -> bool:
    """Returns true if the token is a rest"""
    return annotation_token in _RESTS


def is_clef(annotation_token: str) -> bool:
    """Returns true if the token is a clef"""
    return annotation_token.startswith("clef.")


def is_accidental(annotation_token: str) -> bool:
    """Returns true if the token is an accidental (generic or not)"""
    return to_generic(annotation_token) in _ACCIDENTALS


def is_numeric_time_signature(annotation_token: str) -> bool:
    """Returns true if the token is a numeric time signature (not C or C/)"""
    return annotation_token in _NUMERIC_TIME_SIGNATURE


def is_barline(annotation_token: str) -> bool:
    """Returns true if the token is some kind of barline"""
    return annotation_token in _BARLINES


def get_measures(annotation: str) -> List[str]:
    """
    Splits annotation into annotations of individual measures.

    WARNING: This split is done in a dummy way and ignores barline attachments
    and similar, so should be used with caution.
    """
    tokens = annotation.split()

    if tokens[0] == "|":
        tokens.pop(0)
    if tokens[-1] == "|":
        tokens.pop(-1)

    measures = []

    measure = []
    for token in tokens:
        if is_barline(token):
            measures.append(" ".join(measure))
            measure = []
        else:
            measure.append(token)

    return measures


#########################
# Grouping and analysis #
#########################

# Tokens can be grouped into larger units that make analysis easier.

class TokenGroup:
    """An item with before and after attachments"""
    def __init__(
            self,
            token: str,
            before_attachments: Optional[List[str]] = None,
            after_attachments: Optional[List[str]] = None
    ):
        super().__init__()

        if before_attachments is None:
            before_attachments = []

        if after_attachments is None:
            after_attachments = []

        self.token = token
        self.before_attachments = before_attachments
        self.after_attachments = after_attachments


class TimeSignatureTokenGroup(TokenGroup):
    """Two-number time signature (not C and C/)"""
    def __init__(self, first_number: TokenGroup, second_number: TokenGroup):
        super().__init__(
            "TIME_SIGNATURE",
            first_number.before_attachments + second_number.before_attachments
        )
        self.after_attachments = first_number.after_attachments + second_number.after_attachments
        self.first_token = first_number.token
        self.second_token = second_number.token


class KeySignatureTokenGroup(TokenGroup):
    """Group of accidentals without an item to stick to"""
    def __init__(self, group: TokenGroup):
        super().__init__(
            "KEY_SIGNATURE",
            [b for b in group.before_attachments if is_accidental(b)]
        )
        group.before_attachments = [b for b in group.before_attachments if not is_accidental(b)]

    @staticmethod
    def should_key_signature_be_extracted(group: TokenGroup) -> bool:
        accidentals = [b for b in group.before_attachments if is_accidental(b)]
        if len(accidentals) == 0:  # no accidentals present
            return False
        if len(accidentals) > 1:  # multiple accidentals present
            return True
        if not is_note(group.token):  # group is not a note
            return True
        # now we have one accidental in front of a note -> create key signature
        # if this accidental has different pitch than the note
        if get_pitch(accidentals[0]) != get_pitch(group.token):
            return True
        # otherwise it's just an accidental for a note, no key signature
        return False


def parse_annotation_into_token_groups(annotation: str) -> Tuple[List[TokenGroup], List[str]]:
    """
    Parses, validates and repairs an annotation and produces token groups,
    which is an intermediate representation that is easy to add to canvas.

    Returns list of token groups and a list of warnings.
    """
    tokens = annotation.split()

    # output
    groups: List[TokenGroup] = []
    warnings: List[str] = []

    # === 1. phase: stick attachments to items ===

    # bound the start and end with extra tokens to gather unattached attachments
    tokens = ["START"] + tokens + ["END"]

    # accumulator for before attachments
    before_attachments = []

    # last created item
    item: TokenGroup = None

    # iteration control
    skip_next = False
    for i, token in enumerate(tokens):
        if skip_next:
            skip_next = False
            continue

        # accumulate before attachments
        if is_before_attachment(token):
            before_attachments.append(token)

        # stick after attachment to the last item
        elif is_after_attachment(token):
            item.after_attachments.append(token)

        # create new item
        else:
            item = TokenGroup(token, before_attachments)
            before_attachments = []
            groups.append(item)

    # === 2. phase: group time signatures ===

    i = 0
    while i < len(groups) - 1:
        if is_numeric_time_signature(groups[i].token):
            if is_numeric_time_signature(groups[i + 1].token):
                groups[i].before_attachments += groups[i + 1].before_attachments
                groups[i].after_attachments += groups[i + 1].after_attachments
                groups[i] = TimeSignatureTokenGroup(groups[i], groups[i + 1])
                groups.pop(i + 1)
            else:
                warnings.append("Unpaired numeric time signature: " + groups[i].token)
                groups.pop(i)
                i -= 1
        i += 1

    # === 3. phase: extract key signatures ===

    i = 0
    while i < len(groups):
        if KeySignatureTokenGroup.should_key_signature_be_extracted(groups[i]):
            groups.insert(i, KeySignatureTokenGroup(groups[i]))
            i += 1
        i += 1

    # === 4. phase: handle unattached attachments ===

    i = 0
    while i < len(groups):
        if groups[i].token in ["START", "END"]:
            if len(groups[i].before_attachments) != 0:
                warnings.append(
                    "Unattached before attachments: "
                    + repr(groups[i].before_attachments)
                )
            if len(groups[i].after_attachments) != 0:
                warnings.append(
                    "Unattached after attachments: "
                    + repr(groups[i].before_attachments)
                )
            groups.pop(i)
            i -= 1
        i += 1

    # === 5. phase: validate attachment ordering ===

    def _order_tokens(tokens: List[str]) -> List[str]:
        return list(sorted(
            tokens,
            key=lambda t: _ATTACHMENT_ORDER.index(to_generic(t))
        ))

    def _is_properly_ordered(tokens: List[str]) -> bool:
        return tokens == _order_tokens(tokens)

    for group in groups:
        if isinstance(group, KeySignatureTokenGroup):
            continue  # key signature need not be checked for ordering

        if not _is_properly_ordered(group.before_attachments):
            warnings.append(
                "Attachments are not ordered properly: "
                + repr(group.before_attachments)
            )
            group.before_attachments = _order_tokens(group.before_attachments)

        if not _is_properly_ordered(group.after_attachments):
            warnings.append(
                "Attachments are not ordered properly: "
                + repr(group.after_attachments)
            )
            group.after_attachments = _order_tokens(group.after_attachments)

    # === 6. phase: validate beam continuity ===

    def _remove_right_beam(group):
        pitch = get_pitch(group.token)
        assert pitch is not None
        generic = to_generic(group.token)
        if generic.endswith("="):
            group.token = generic[:-1] + str(pitch)

    def _remove_left_beam(group):
        if group.token.startswith("="):
            group.token = group.token[1:]

    def _add_left_beam(group):
        if not group.token.startswith("="):
            group.token = "=" + group.token

    in_beam = False
    last_beamed_group = None
    for group in groups:
        if in_beam:
            # inside of a beam we have to hit another beamed note

            # except for these allowed symbols
            if is_rest(group.token)\
                    or is_clef(group.token)\
                    or isinstance(group, KeySignatureTokenGroup)\
                    or group.token == "?":
                continue

            if not is_beamed_note(group.token):
                warnings.append(
                    "Unexpected token inside a beamed group: " + repr(group.token)
                )
                _remove_right_beam(last_beamed_group)
                in_beam = False
                last_beamed_group = None
                continue

            # now the beamed note has to have a left beam
            if not to_generic(group.token).startswith("="):
                warnings.append(
                    "Non-finished beam: 'x= x' at: " + repr(group.token)
                )
                _add_left_beam(group)

            # end beam
            if not to_generic(group.token).endswith("="):
                in_beam = False
                last_beamed_group = None

        else:
            # outside of a beam we just wait for a beam to start and check
            # that we don't encounter non-started beams
            if not is_beamed_note(group.token):
                continue

            if to_generic(group.token).startswith("="):
                warnings.append(
                    "Non-started beam: 'x =x' at: " + repr(group.token)
                )
                _remove_left_beam(group)

            # start beam, but only if it does actually start
            if to_generic(group.token).endswith("="):
                in_beam = True
                last_beamed_group = group

    if in_beam:
        # unfinished beam
        warnings.append(
            "Non-finished beam: 'x= EOS' at the last token."
        )
        _remove_right_beam(last_beamed_group)
        
    # === Done ===

    return groups, warnings


def validate_annotation(annotation: str):
    groups, warnings = parse_annotation_into_token_groups(annotation)
    if len(warnings) > 0:
        print("Invalid annotation:")
        print(annotation)
        print("\t" + "\t\n".join(warnings))
        raise Exception("Invalid annotation")


def stringify_token_groups_to_annotation(groups: List[TokenGroup]) -> str:
    def sort_attachments(attachments: List[str]):
        return list(sorted(
            attachments,
            key=lambda a: _ATTACHMENT_ORDER.index(to_generic(a))
        ))

    tokens = []
    for group in groups:
        tokens += sort_attachments(group.before_attachments)
        if isinstance(group, KeySignatureTokenGroup):
            pass  # attachments will be added, and there's no token
        elif isinstance(group, TimeSignatureTokenGroup):
            tokens.append(group.first_token)
            tokens.append(group.second_token)
        else:
            tokens.append(group.token)
        tokens += sort_attachments(group.after_attachments)

    return " ".join(tokens)


def repair_annotation(annotation: str) -> Tuple[str, List[str]]:
    """
    Repairs attachment ordering, fixes beams, ...
    Returns the fixed annotation and a list of warnings
    """
    groups, warnings = parse_annotation_into_token_groups(annotation)
    repaired_annotation = stringify_token_groups_to_annotation(groups)
    return repaired_annotation, warnings


def trim_non_repeat_barlines(annotation: str) -> str:
    """Removes all leading and trailing barlines (that are not repeat barlines)"""
    tokens = annotation.split()

    # leading
    while len(tokens) > 0 and tokens[0] == "|":
        del tokens[0]

    # trailing
    while len(tokens) > 0 and tokens[-1] == "|":
        del tokens[-1]

    return " ".join(tokens)


#######################################
# Transformations for ITER evaluation #
#######################################


_NON_IMPORTANT_TOKENS = [
    # question mark
    "?",

    # all attachments, except for accidentals and duration dots
    *list(set(_ATTACHMENTS) - set(_ACCIDENTALS) - set(_DURATION_DOTS)),

    # Double sharp and double flat are also non important, because they aren't
    # present in training or evaluation right now. They should, however,
    # become important once they are being trained on.
    "x", "bb",
]


def is_important_token(token: str) -> bool:
    if to_generic(token) in _NON_IMPORTANT_TOKENS:
        return False
    return True


def count_important_tokens(annotation: str) -> int:
    return len(list(filter(is_important_token, annotation.split())))


def iter_raw_transformation(annotation: str) -> str:
    return annotation  # raw = identity


def iter_trained_transformation(annotation: str):
    annotation = iter_raw_transformation(annotation)

    TRANSFORMATION_TABLE = {
        "?": None,

        "|:": "|",
        ":|": "|",
        ":|:": "|",

        "x{p}": None,
        "bb{p}": None,
        "tuplet.3": None,
        "fermata": None,
        "trill": None,
        "+": None,
        "_": None,
        ">": None,
        "^": None,
    }

    tokens = annotation.split()
    i: int = 0
    while i < len(tokens):
        if tokens[i] in TRANSFORMATION_TABLE:
            if TRANSFORMATION_TABLE[tokens[i]] is None:
                del tokens[i]
                continue
            else:
                tokens[i] = TRANSFORMATION_TABLE[tokens[i]]
        i += 1
    return " ".join(tokens)


def iter_slurless_transformation(annotation: str) -> str:
    annotation = iter_trained_transformation(annotation)
    return " ".join(
        filter(
            lambda t: t not in ["(", ")"],
            annotation.split()
        )
    )


def iter_ornamentless_transformation(annotation: str) -> str:
    annotation = iter_slurless_transformation(annotation)

    def is_ornament(token: str) -> bool:
        if is_accidental(token):
            return False
        if is_duration_dot(token):
            return False
        if is_attachment(token):
            return True
        return False

    return " ".join(filter(
        lambda token: not is_ornament(token),
        annotation.split()
    ))


def iter_pitchless_transformation(annotation: str) -> str:
    annotation = iter_ornamentless_transformation(annotation)
    return " ".join(map(lambda t: to_generic(t), annotation.split()))
