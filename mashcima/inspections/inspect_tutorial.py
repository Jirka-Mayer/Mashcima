import mashcima as mc
import matplotlib.pyplot as plt


# Example 1:
# Synthesizing for training
annotation = "h-5 ( ) e=-5 =s=-4 #-3 =s-3 s=-2 =s=-1 N0 =s=0 #1 =s1 | " + \
    "h2 ( ) e=2 =s=3 #4 =s4 s=5 =s=6 N7 =s=7 #8 =s8 | q9 qr hr"

img = mc.synthesize_for_training(annotation)

plt.imshow(img)
plt.show()


# Example 2:
# Synthesizing for beauty
mc.use_only_writer_number_one()

img = mc.synthesize_for_beauty(annotation)

plt.imshow(img)
plt.show()


# Example 3:
# Synthesize multi-staff
img = mc.synthesize_for_beauty(
    above_annotation=annotation,
    main_annotation=annotation,
    below_annotation=annotation,
)

plt.imshow(img)
plt.show()


# Example 4:
# Synthesize from random annotation
img = mc.synthesize_for_beauty(
    mc.generate_random_annotation()
)

plt.imshow(img)
plt.show()

# Example 5:
# Loading the PrIMuS dataset
data = mc.load_primus_as_mashcima_annotations(take=5)
print(mc.load_primus_as_mashcima_annotations(take=5))

img = mc.synthesize_for_beauty(
    data[0]["mashcima"]
)

plt.imshow(img)
plt.show()

# Example 6:
# Converting PrIMuS agnostic encoding to mashcima encoding
print(mc.convert_primus_annotation_to_mashcima_annotation(
    "clef.G-L2\taccidental.sharp-L5\taccidental.sharp-S3\tmetersign.C-L3"
)) # prints "clef.G-2 #4 #1 time.C"
