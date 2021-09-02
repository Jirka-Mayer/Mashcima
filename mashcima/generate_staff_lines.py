import os
import numpy as np
from muscima.io import parse_cropobject_list
from typing import Tuple, Dict
import config
from mashcima.vocabulary import HIGHEST_PITCH, LOWEST_PITCH


# to prevent the XML from being loaded each time this method gets called
_staff_line_cache = None


def generate_staff_lines() -> Tuple[np.ndarray, Dict[int, int]]:
    """Generates an image of a staff with pixel positions of note positions"""
    global _staff_line_cache

    if _staff_line_cache is not None:
        return _staff_line_cache[0].copy(), _staff_line_cache[1]

    doc = parse_cropobject_list(
        os.path.join(
            config.MUSCIMA_PP_CROP_OBJECT_DIRECTORY,
            "CVC-MUSCIMA_W-01_N-19_D-ideal.xml"
        )
    )

    staves = [x for x in doc if x.clsname == "staff"]
    staff = staves[-1]  # last staff has no notes on this piece
    margin = staff.height

    # build the empty staff image with proper margin
    img = np.zeros(
        shape=(staff.height + margin * 2, staff.width),
        dtype=np.float32
    )
    img[margin:(margin + staff.height), :] += staff.mask

    # get positions of lines with respect to the image
    lines = [
        x for x in doc if x.clsname == "staff_line"
        if staff.top - 10 < x.top < staff.bottom + 10
    ]
    line_centers = [
        int((line.top + line.bottom) / 2) - (staff.top - margin)
        for line in lines
    ]
    line_centers.sort()  # from top line to bottom line

    # convert line centers to an actual note position mapping
    spaces = [s[1] - s[0] for s in zip(line_centers, line_centers[1:])]
    space_centers = np.array(line_centers[0:-1]) + np.array(spaces) / 2
    position_zip = zip(line_centers, space_centers)
    positions = [int(p) for t in position_zip for p in t] + [line_centers[-1]]

    # add positions above and below (ledger lines)
    step = int(np.mean(spaces) / 2)
    add_count = max(abs(HIGHEST_PITCH), abs(LOWEST_PITCH)) - 4
    for i in range(add_count):
        positions = [positions[0] - step] + positions + [positions[-1] + step]

    # create a pitch -> position mapping
    position_dict = {
        ((len(positions) - 1) // 2) - i: pos
        for i, pos in enumerate(positions)
    }

    # for debug
    # for c in positions:
    #     img[c, :] = 0.5

    _staff_line_cache = (img.copy(), position_dict)

    return img, position_dict
