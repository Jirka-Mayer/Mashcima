import mashcima as mc
import matplotlib.pyplot as plt

mc.use_only_writer_number_one()

img = mc.synthesize(
    "h-5 ( ) e=-5 =s=-4 #-3 =s-3 s=-2 =s=-1 N0 =s=0 #1 =s1 | " +
    "h2 ( ) e=2 =s=3 #4 =s4 s=5 =s=6 N7 =s=7 #8 =s8 | q9 qr hr",
    above_annotation="qr qr qr",
    below_annotation="qr qr qr | qr",
    crop_horizontally=True, crop_vertically=True, transform_image=False
)
plt.imshow(img)
plt.show()
