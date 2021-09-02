import numpy as np
import cv2
import random
import math
from typing import Optional, List


def _generate_transformation(img_shape):
    """Generates a random affine transformation for an image."""
    MAX_SKEW = 10  # deg
    MAX_RAISE_ROT = 0.3  # 1/2 image height times this number
    MAX_ABS_ROT = 10  # deg

    # skew (and scale on X axis)
    max_skew_angle = MAX_SKEW  # deg
    max_scale = 1.2
    skew_angle = random.randint(-max_skew_angle, max_skew_angle)
    scale = random.uniform(1 / max_scale, max_scale)
    skew_shift = 100 * math.tan(skew_angle / 180 * math.pi)
    pts1 = np.float32([[0, 0], [100, 0], [0, 100]])
    pts2 = np.float32([[0, 0], [100 * scale, 0], [skew_shift, 100]])
    skew_matrix = cv2.getAffineTransform(pts1, pts2)

    # rotate (such that the rise at the end is at most half the height)
    max_angle = 0
    if img_shape[0] / img_shape[1] < 1:
        max_angle = math.asin(img_shape[0] / img_shape[1]) / math.pi * 90
        max_angle = int(max_angle * MAX_RAISE_ROT)
    if max_angle > MAX_ABS_ROT:
        max_angle = MAX_ABS_ROT

    angle = random.randint(-max_angle, max_angle)
    rotation_matrix = cv2.getRotationMatrix2D((0, 0), angle, 1)

    # compose transformations
    matrix = np.matrix(skew_matrix[0:2, 0:2]) * np.matrix(rotation_matrix[0:2, 0:2])

    matrix = np.zeros(shape=(2, 3), dtype=np.float32)
    matrix[0:2, 0:2] = rotation_matrix[0:2, 0:2].dot(skew_matrix[0:2, 0:2])

    return matrix


def _generate_padding(img_shape):
    """Generates a random padding"""
    staff_height = img_shape[0] / 3
    horizontal_max = int(staff_height * 0.5)
    vertical_max = int(staff_height * 0.1)  # vertical padding can be negative
    left = random.randint(0, horizontal_max)
    right = random.randint(0, horizontal_max)
    top = random.randint(-vertical_max, vertical_max)
    bottom = random.randint(-vertical_max, vertical_max)
    return top, right, bottom, left


def transform_image(img: np.ndarray, box: Optional[List[int]]=None):
    """Rotates and deforms the image slightly"""
    # box = [x, y, width, height]

    if box is None:
        corners = np.array([
            [[0, 0]],
            [[img.shape[1], 0]],
            [[img.shape[1], img.shape[0]]],
            [[0, img.shape[0]]]
        ], dtype=np.int32)
        box_shape = img.shape
    else:
        box_shape = (box[3], box[2])
        corners = np.array([
            [[box[0], box[1]]],
            [[box[0] + box_shape[1], box[1]]],
            [[box[0] + box_shape[1], box[1] + box_shape[0]]],
            [[box[0], box[1] + box_shape[0]]]
        ], dtype=np.int32)

    # setup the transformation matrix
    matrix = _generate_transformation(box_shape)

    # setup padding (top, right, bottom, left)
    padding = _generate_padding(box_shape)

    # transform image corners to get the new dimensions (rect)
    transformed_corners = cv2.transform(corners, matrix)
    rect = cv2.boundingRect(transformed_corners)  # (left, top, width, height)

    # move the image so that it fits the destination image (include padding)
    matrix[0, 2] += -rect[0] + padding[3]
    matrix[1, 2] += -rect[1] + padding[0]

    # calculate destination image size
    dest_size = (
        rect[2] + padding[3] + padding[1],
        rect[3] + padding[0] + padding[2]
    )

    # do the final image transformation
    img = cv2.warpAffine(img, matrix, dest_size, borderValue=0)

    return img
