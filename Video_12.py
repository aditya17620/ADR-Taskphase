import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('l12.jpg')
img = cv2.resize(img, (250, 550))
print(img.shape[:2])
mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

# defining the region of the image where we need the operation to be performed
# the argument is starting width starting height ending width ending height

rect = (25, 80, 170, 550)

# using grabCut to extraxt the foreground of the image.
# it takes in arguments as the source image, the mask, rectangular region of interest,
# backgroundModel, foregroundModel, iteration count, before the method returns the data(higher vaalue, better result) and the operation mode
# in this case, we use the operation mode as, GC_INIT_WITH_RECT, this means that the method will ignore everything thats outside the rectangle,
# and will consider only the ROI inside the specified rectangle.
# Another operation mode used is GC_INIT_WITH_MASK, where the region that is black in the mask is not considered by the method.
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
# mask has 4 types of pixels, foreground pixel, background pixel, probable foreground, probable background.
# Hence, the condition of mask 2 and 4 is used to isolate the background
# we use the np.where method and use it as a true or false output to store the value as an unsigned integer of 8 bits
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
# np.newaxis is used to make a new
img = img * mask2[:, :, np.newaxis]
plt.imshow(img)
plt.colorbar()
plt.show()
