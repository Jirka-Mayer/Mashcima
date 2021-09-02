from mashcima.generate_random_annotation import generate_random_annotation
import matplotlib.pyplot as plt
from mashcima.annotation_to_image import annotation_to_image
from mashcima import Mashcima

SHOW_IMAGES = True
IMAGE_COUNT = 10

mc = None
if SHOW_IMAGES:
    mc = Mashcima([
        "CVC-MUSCIMA_W-01_N-10_D-ideal.xml",
        "CVC-MUSCIMA_W-01_N-14_D-ideal.xml",
        "CVC-MUSCIMA_W-01_N-19_D-ideal.xml",
    ])

for i in range(IMAGE_COUNT):
    annotation = generate_random_annotation()
    print(annotation)
    if i % 100 == 0:
        print(i)

    if SHOW_IMAGES:
        img = annotation_to_image(mc, annotation)
        plt.imshow(img)
        plt.show()
