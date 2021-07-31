import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 =cv2.imread('matchee.jpg')
img2 = cv2.imread('mathcer.jpg')

# ORB or oriented BRIEF is a keypoint detector and descriptor extractor
# that is used to detect stable keypoints within images, so that they can be matched later on.
# ORD_create is used to initialize the method (using the orb object here)
orb = cv2.ORB_create()

# detectAndCompute method is a method of the ORB class, and it is used to detect the keypoints
# and the descriptors in an image. These two are the important elements that help match the
# objects from the two images.
# it takes in input of the image, and the mask. It gives an output of keywords & descriptors
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# BFMatchers is a method of the ORB class as well. It stands for Brute Force Matcher
# and as the name suggests, it is a brute Force method of comparing the keywords, descriptors
# to find a match between two different images.
# it takes in the inputs of the norm type, or the method used to compute distance between points
# and a boolean cross check value which is false by default. This makes sure that both sets
# match eachother and is recommended to be set to true for consistent results.
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

# matches is used to match the descriptors of both the images
matches = bf.match(des1, des2)
matches = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], None, flags = 2)
plt.imshow(img3)
plt.show()
