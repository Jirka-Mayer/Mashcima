import os
import re
from muscima.io import parse_cropobject_list, CropObject
import itertools
from typing import List, Dict, Optional
from mashcima.Sprite import Sprite
from mashcima.SpriteGroup import SpriteGroup
import cv2
import pickle
import config


MASHCIMA_CACHE_PATH = "mashcima-cache.pkl"


class Mashcima:
    def __init__(
            self,
            documents: List[str] = None,
            take_writers: Optional[List[int]] = None,
            skip_writers: Optional[List[int]] = None,
            use_cache: bool = False
    ):
        print("Loading mashcima...")

        # default documents to load
        if documents is None:
            documents = [
                os.path.join(config.MUSCIMA_PP_CROP_OBJECT_DIRECTORY, f)
                for f in os.listdir(config.MUSCIMA_PP_CROP_OBJECT_DIRECTORY)
            ]
            # TODO: HACK: Limit document count
            #documents = documents[:10]

        ##############################
        # Load and prepare MUSCIMA++ #
        ##############################

        self.DOCUMENTS = []

        # try to restore mashcima from cache since it's faster
        was_restored = False
        if os.path.isfile(MASHCIMA_CACHE_PATH) and use_cache:
            was_restored = True
            print("Restoring mashcima from cache...")
            self.DOCUMENTS = pickle.load(open(MASHCIMA_CACHE_PATH, "rb"))
            print("Restored %s documents." % (len(self.DOCUMENTS),))

        # all loaded crop object documents
        if len(self.DOCUMENTS) == 0:
            for i, doc in enumerate(documents):
                print("Parsing document %d/%d ..." % (i + 1, len(documents)))
                self.DOCUMENTS.append(
                    parse_cropobject_list(
                        os.path.join(config.MUSCIMA_PP_CROP_OBJECT_DIRECTORY, doc)
                    )
                )

        # cache the loaded documents
        if not was_restored and use_cache:
            print("Caching mashcima in", MASHCIMA_CACHE_PATH)
            pickle.dump(self.DOCUMENTS, open(MASHCIMA_CACHE_PATH, "wb"))

        # filter documents
        def _get_writer(document_name: str) -> int:
            m = re.search("^CVC-MUSCIMA_W-(\d+)", document_name)
            assert m is not None
            return int(m.group(1))

        if skip_writers is not None:
            self.DOCUMENTS = list(filter(
                lambda d: _get_writer(d[0].doc) not in skip_writers,
                self.DOCUMENTS
            ))

        if take_writers is not None:
            self.DOCUMENTS = list(filter(
                lambda d: _get_writer(d[0].doc) in take_writers,
                self.DOCUMENTS
            ))

        # names of the documents
        # (used for resolving document index from document name)
        self.DOCUMENT_NAMES = [doc[0].doc for doc in self.DOCUMENTS]

        # all loaded crop objects in one list
        self.CROP_OBJECTS = list(itertools.chain(*self.DOCUMENTS))

        # for each document name create an objid lookup dictionary
        # (to make resolving outlinks easier)
        self.CROP_OBJECT_LOOKUP_DICTS: Dict[str, Dict[int, CropObject]] = {
            self.DOCUMENT_NAMES[i]: {c.objid: c for c in doc}
            for i, doc in enumerate(self.DOCUMENTS)
        }

        ####################################
        # Prepare all symbols for printing #
        ####################################

        print("Preparing symbols...")

        # prevents cyclic imports
        from mashcima.get_symbols import get_whole_notes
        from mashcima.get_symbols import get_half_notes
        from mashcima.get_symbols import get_quarter_notes
        from mashcima.get_symbols import get_eighth_notes
        from mashcima.get_symbols import get_sixteenth_notes
        from mashcima.get_symbols import get_longa_rests
        from mashcima.get_symbols import get_breve_rests
        from mashcima.get_symbols import get_whole_rests
        from mashcima.get_symbols import get_half_rests
        from mashcima.get_symbols import get_quarter_rests
        from mashcima.get_symbols import get_eighth_rests
        from mashcima.get_symbols import get_sixteenth_rests
        from mashcima.get_symbols import get_accidentals
        from mashcima.get_symbols import get_dots
        from mashcima.get_symbols import get_ledger_lines
        from mashcima.get_symbols import get_barlines
        from mashcima.get_symbols import get_g_clefs
        from mashcima.get_symbols import get_f_clefs
        from mashcima.get_symbols import get_c_clefs
        from mashcima.get_symbols import get_time_marks

        # load all symbols
        self.WHOLE_NOTES: List[SpriteGroup] = get_whole_notes(self)
        self.HALF_NOTES: List[SpriteGroup] = get_half_notes(self)
        self.QUARTER_NOTES: List[SpriteGroup] = get_quarter_notes(self)
        self.EIGHTH_NOTES: List[SpriteGroup] = get_eighth_notes(self)
        self.SIXTEENTH_NOTES: List[SpriteGroup] = get_sixteenth_notes(self)

        self.LONGA_RESTS: List[SpriteGroup] = get_longa_rests(self)
        self.BREVE_RESTS: List[SpriteGroup] = get_breve_rests(self)
        self.WHOLE_RESTS: List[SpriteGroup] = get_whole_rests(self)
        self.HALF_RESTS: List[SpriteGroup] = get_half_rests(self)
        self.QUARTER_RESTS: List[SpriteGroup] = get_quarter_rests(self)
        self.EIGHTH_RESTS: List[SpriteGroup] = get_eighth_rests(self)
        self.SIXTEENTH_RESTS: List[SpriteGroup] = get_sixteenth_rests(self)

        self.SHARPS: List[Sprite] = []
        self.FLATS: List[Sprite] = []
        self.NATURALS: List[Sprite] = []
        self.SHARPS, self.FLATS, self.NATURALS = get_accidentals(self)
        self.DOTS: List[Sprite] = get_dots(self)
        self.LEDGER_LINES: List[Sprite] = get_ledger_lines(self)
        self.BAR_LINES: List[SpriteGroup] = []
        self.TALL_BAR_LINES: List[SpriteGroup] = []
        self.BAR_LINES, self.TALL_BAR_LINES = get_barlines(self)
        self.G_CLEFS: List[SpriteGroup] = get_g_clefs(self)
        self.F_CLEFS: List[SpriteGroup] = get_f_clefs(self)
        self.C_CLEFS: List[SpriteGroup] = get_c_clefs(self)
        self.TIME_MARKS: Dict[str, List[SpriteGroup]] = get_time_marks(self)

        # load default symbols if needed
        if len(self.EIGHTH_NOTES) == 0:
            self.EIGHTH_NOTES.append(_load_default_eighth_note())
        if len(self.SIXTEENTH_NOTES) == 0:
            self.SIXTEENTH_NOTES.append(_load_default_sixteenth_note())
        if len(self.LONGA_RESTS) == 0:
            self.LONGA_RESTS.append(_load_default_sprite_group("rest", "rest_longa"))
        if len(self.BREVE_RESTS) == 0:
            self.BREVE_RESTS.append(_load_default_sprite_group("rest", "rest_breve"))
        if len(self.WHOLE_RESTS) == 0:
            self.WHOLE_RESTS.append(_load_default_sprite_group("rest", "rest_whole"))
        if len(self.HALF_RESTS) == 0:
            self.HALF_RESTS.append(_load_default_sprite_group("rest", "rest_half"))
        if len(self.QUARTER_RESTS) == 0:
            self.QUARTER_RESTS.append(_load_default_sprite_group("rest", "rest_quarter"))
        if len(self.EIGHTH_RESTS) == 0:
            self.EIGHTH_RESTS.append(_load_default_sprite_group("rest", "rest_eighth"))
        if len(self.SIXTEENTH_RESTS) == 0:
            self.SIXTEENTH_RESTS.append(_load_default_sprite_group("rest", "rest_sixteenth"))
        if len(self.F_CLEFS) == 0:
            self.F_CLEFS.append(_load_default_sprite_group("clef", "clef_f"))
        if len(self.G_CLEFS) == 0:
            self.G_CLEFS.append(_load_default_sprite_group("clef", "clef_g"))
        if len(self.C_CLEFS) == 0:
            self.C_CLEFS.append(_load_default_sprite_group("clef", "clef_c"))
        for key in self.TIME_MARKS:
            if len(self.TIME_MARKS[key]) == 0:
                self.TIME_MARKS[key].append(
                    _load_default_sprite_group("symbol", key)
                )

        # validate there is no empty list
        assert len(self.WHOLE_NOTES) > 0
        assert len(self.HALF_NOTES) > 0
        assert len(self.QUARTER_NOTES) > 0
        assert len(self.EIGHTH_NOTES) > 0
        assert len(self.SIXTEENTH_NOTES) > 0
        assert len(self.LONGA_RESTS) > 0
        assert len(self.BREVE_RESTS) > 0
        assert len(self.WHOLE_RESTS) > 0
        assert len(self.HALF_RESTS) > 0
        assert len(self.QUARTER_RESTS) > 0
        assert len(self.EIGHTH_RESTS) > 0
        assert len(self.SIXTEENTH_RESTS) > 0
        assert len(self.FLATS) > 0
        assert len(self.SHARPS) > 0
        assert len(self.NATURALS) > 0
        assert len(self.DOTS) > 0
        assert len(self.LEDGER_LINES) > 0
        assert len(self.BAR_LINES) > 0
        assert len(self.TALL_BAR_LINES) > 0
        assert len(self.G_CLEFS) > 0
        assert len(self.F_CLEFS) > 0
        assert len(self.C_CLEFS) > 0
        for key in self.TIME_MARKS:
            assert len(self.TIME_MARKS[key]) > 0

        print("Mashcima loaded.")


def _load_default_sprite_group(sprite_name: str, file_name: str) -> SpriteGroup:
    return SpriteGroup().add(sprite_name, _load_default_sprite(file_name))


def _load_default_sprite(name: str) -> Sprite:
    print("Loading default sprite:", name)
    dir = os.path.join(os.path.dirname(__file__), "default_symbols")
    img_path = os.path.join(dir, name + ".png")
    center_path = os.path.join(dir, name + ".txt")
    if not os.path.isfile(img_path):
        raise Exception("Cannot load default sprite: " + name)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) / 255
    x = -img.shape[1] // 2
    y = -img.shape[0] // 2
    if os.path.isfile(center_path):
        with open(center_path) as f:
            x, y = tuple(f.readline().split())
            x = -int(x)
            y = -int(y)
    return Sprite(x, y, img)


def _load_default_eighth_note() -> SpriteGroup:
    group = SpriteGroup()
    group.add("notehead", _load_default_sprite("note_eighth_notehead"))
    group.add("stem", _load_default_sprite("note_eighth_stem"))
    group.add("flag_8", _load_default_sprite("note_eighth_flag_8"))
    return group


def _load_default_sixteenth_note() -> SpriteGroup:
    group = SpriteGroup()
    group.add("notehead", _load_default_sprite("note_sixteenth_notehead"))
    group.add("stem", _load_default_sprite("note_sixteenth_stem"))
    group.add("flag_8", _load_default_sprite("note_sixteenth_flag_8"))
    group.add("flag_16", _load_default_sprite("note_sixteenth_flag_16"))
    return group
