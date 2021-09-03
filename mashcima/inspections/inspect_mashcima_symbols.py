from mashcima.SymbolRepository import SymbolRepository
from mashcima.Sprite import Sprite
from mashcima.SpriteGroup import SpriteGroup
from mashcima.debug import show_images
from typing import List
import numpy as np


# repo = SymbolRepository([
#     "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
#     "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
#     "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
#
#     # "CVC-MUSCIMA_W-02_N-06_D-ideal.xml",
#     # "CVC-MUSCIMA_W-02_N-13_D-ideal.xml",
#     # "CVC-MUSCIMA_W-02_N-17_D-ideal.xml",
# ])
repo = SymbolRepository()


def inspect(items: List):
    batch: List[np.ndarray] = []
    BATCH_SIZE = 50
    for index, item in enumerate(items):
        if isinstance(item, Sprite):
            batch.append(item.inspect())
        elif isinstance(item, SpriteGroup):
            batch.append(item.inspect())

        if len(batch) == BATCH_SIZE:
            print("Showing indices:", index - BATCH_SIZE + 1, "-", index, "/", len(items))
            show_images(batch, row_length=10)
            batch = []
    if len(batch) != 0:
        print("Showing indices:", len(items) - len(batch), "-", len(items) - 1, "/", len(items))
        show_images(batch, row_length=10)


###############
# INSPECTIONS #
###############

# DEFAULT SYMBOL SAVING:
# import cv2, os
# s = mc.BREVE_RESTS[0].sprite("rest")
# p = os.path.join(os.path.dirname(__file__), "mashcima/default_symbols/rest_breve")
# cv2.imwrite(p + ".png", s.mask * 255)
# with open(p + ".txt", "w") as f:
#     f.write(str(-s.x) + " " + str(-s.y))


inspect(repo.WHOLE_NOTES)
# inspect(mc.HALF_NOTES)
# inspect(mc.QUARTER_NOTES)
# inspect(mc.EIGHTH_NOTES)
# inspect(mc.SIXTEENTH_NOTES)

# inspect(mc.LONGA_RESTS)
# inspect(mc.BREVE_RESTS)
# inspect(mc.WHOLE_RESTS)
# inspect(mc.HALF_RESTS)
# inspect(mc.QUARTER_RESTS)
# inspect(mc.EIGHTH_RESTS)
# inspect(mc.SIXTEENTH_RESTS)
#
# inspect(mc.FLATS)
# inspect(mc.SHARPS)
# inspect(mc.NATURALS)
#
# inspect(mc.DOTS)
# inspect(mc.LEDGER_LINES)
# inspect(mc.BAR_LINES)
#
# inspect(mc.G_CLEFS)
# inspect(mc.F_CLEFS)
# inspect(mc.C_CLEFS)
#
# inspect(mc.TIME_MARKS["time_0"])
# inspect(mc.TIME_MARKS["time_1"])
# inspect(mc.TIME_MARKS["time_2"])
# inspect(mc.TIME_MARKS["time_3"])
# inspect(mc.TIME_MARKS["time_4"])
# inspect(mc.TIME_MARKS["time_5"])
# inspect(mc.TIME_MARKS["time_6"])
# inspect(mc.TIME_MARKS["time_7"])
# inspect(mc.TIME_MARKS["time_8"])
# inspect(mc.TIME_MARKS["time_9"])
# inspect(mc.TIME_MARKS["time_c"])
