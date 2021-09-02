import numpy as np
import cv2


def show_images(images, row_length=5):
    """For debugging - shows many images in a single plot"""
    import matplotlib.pyplot as plt

    n_total = len(images)
    n_rows = n_total // row_length + 1
    n_cols = min(n_total, row_length)
    fig = plt.figure()
    for i, img in enumerate(images):
        plt.subplot(n_rows, n_cols, i+1)
        #plt.imshow(img, cmap='gray', interpolation='nearest')
        plt.imshow(img)
    # Let's remove the axis labels, they clutter the image.
    for ax in fig.axes:
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_xticks([])
    plt.show()


def draw_cross(
        img: np.ndarray,
        x: int, y: int,
        size: int = 10,
        thickness: int = 2,
        color: any = 0.5
) -> np.ndarray:
    """Draws a cross into an image"""
    cv2.line(
        img,
        (x - size, y + size),
        (x + size, y - size),
        thickness=thickness,
        color=color
    )
    cv2.line(
        img,
        (x - size, y - size),
        (x + size, y + size),
        thickness=thickness,
        color=color
    )
    return img
