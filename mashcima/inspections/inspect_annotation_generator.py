from mashcima.generate_random_annotation import generate_random_annotation
import matplotlib.pyplot as plt
from mashcima.annotation_to_image import annotation_to_image
from mashcima.SymbolRepository import SymbolRepository

SHOW_IMAGES = True
IMAGE_COUNT = 10

repo = None
if SHOW_IMAGES:
    repo = SymbolRepository([
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
        img = annotation_to_image(repo, annotation)
        plt.imshow(img)
        plt.show()
