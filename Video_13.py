import cv2
import numpy as np

img = cv2.imread('L13.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# all the values of the pixels in gray are converted into floating numbers to provide extra precision
gray = np.float32(gray)

# goodFreaturesToTrack is used to track the corners.
# It takes in the arguments of image, max corners,
# quality level and the minimum distance between each corners.
# it is used to track features of an image, and display them
# working is based on difference in intensities of the pixel values.
# if there is a drastic value change in pixels, it is considered to be a feature
# works best with gray images, as there is only one layer of picture matrix.
corners = cv2.goodFeaturesToTrack(gray, 1000, 0.01, 10)
# converting the values stored in corners to an integer variable of 64 bits size
corners = np.int64(corners)

# executing a for-loop to mark all the features discovered in the above method
# and to draw a circle on top of that image.
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 2, (255, 255, 255), 1)

cv2.imshow('corner', img)
cv2.waitKey(0)
