# Objective: to add or superimpose one image over the other and display the resulting image in a separate window
import cv2

# creating objects circle and notACircle to read
# the respective images that we need to superimpose
circle = cv2.imread('circle.png')
notACircle = cv2.imread('notACircle.png')
# resizing both the images using the resize method from cv2
# to the same dimensions as we can not add two images with different dimensions
# and storing them in the same image objects
circle = cv2.resize(circle, (568, 568))
notACircle = cv2.resize(notACircle, (568,568))

# this is a basic version of adding the pixels of both the images and displaying the output.
# the final image does not lose any opaqueness
add = circle+ notACircle

# using a simple add method that adds up the bitwise pixel values of both the images and caps the range to 255
# the disadvantage of this method is that it shows any thing above the 255th channel as 255, if the images
# contain white spaces, this method will add both of the whites and give out an extremely bright white spot
# for example, if the pixel values are [200,150, 100] and [150, 150, 50] the output pixel will have the value of
# [255, 255, 150]
add1 = cv2.add(circle, notACircle)

# another method by cv2 known as weighted addition gives better results. This method
# takes i arguments of the img1, the weight of img1, img2, the weight of img2 and the gamma value for the final image
add2 = cv2.addWeighted(circle, 0.5, notACircle, 0.5, 2)

cv2.imshow('output', add1)
cv2.waitKey(0)
