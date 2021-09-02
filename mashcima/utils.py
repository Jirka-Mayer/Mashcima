from muscima.io import CropObject
from mashcima import Mashcima
import cv2
import numpy as np
from typing import List, Tuple
import random


def fork(label: str, stay_probability: float):
    """Helper for random binary splitting"""
    return random.random() <= stay_probability


def get_outlink_to(mc: Mashcima, obj: CropObject, clsname: str) -> CropObject:
    for l in obj.outlinks:
        resolved_link = mc.CROP_OBJECT_LOOKUP_DICTS[obj.doc][l]
        if resolved_link.clsname == clsname:
            return resolved_link
    raise Exception("Object has no outlink of requested clsname")


def has_outlink_to(mc: Mashcima, obj: CropObject, clsname: str) -> bool:
    for l in obj.outlinks:
        resolved_link = mc.CROP_OBJECT_LOOKUP_DICTS[obj.doc][l]
        if resolved_link.clsname == clsname:
            return True
    return False


def get_connected_components_not_touching_image_border(
        mask: np.ndarray
) -> List[np.ndarray]:
    """
    Takes a binary image and finds all components (areas with value 1)
    that don't touch the image border.
    """
    height, width = mask.shape
    ret, labels = cv2.connectedComponents(mask)

    indices_to_remove = set()
    for x in range(width):
        indices_to_remove.add(labels[0, x])
        indices_to_remove.add(labels[height - 1, x])
    for y in range(height):
        indices_to_remove.add(labels[y, 0])
        indices_to_remove.add(labels[y, width - 1])
    indices = set(range(1, ret)) - indices_to_remove

    out_masks: List[np.ndarray] = []
    for i in indices:
        out_masks.append(labels == i)
    return out_masks


def get_center_of_component(mask: np.ndarray) -> Tuple[int, int]:
    m = cv2.moments(mask.astype(np.uint8))
    if m["m00"] == 0:
        import matplotlib.pyplot as plt
        plt.imshow(mask)
        plt.show()
    x = int(m["m10"] / m["m00"])
    y = int(m["m01"] / m["m00"])
    return x, y


def point_distance_squared(ax: int, ay: int, bx: int, by: int) -> int:
    """Returns distance between two points squared"""
    return (ax - bx) ** 2 + (ay - by) ** 2


def sort_components_by_proximity_to_point(
        components: List[np.ndarray], x: int, y: int
) -> List[np.ndarray]:
    with_distances = [
        {
            "component": c,
            "distanceSqr": point_distance_squared(
                *get_center_of_component(c),
                x, y
            )
        }
        for c in components
    ]
    with_distances.sort(key=lambda x: x["distanceSqr"])
    return [x["component"] for x in with_distances]
