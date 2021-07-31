# Objective: To dynamically get the values of hue, saturation and value
# from the user to filter out unwanted colors from an image and display
# the image of the filtered color
import cv2
import numpy as np


# defining a function empty, that does nothing
def empty(a):
    pass


cap = cv2.VideoCapture(0)
# Creating a window named Trackbars using the namedWindow method in cv2
cv2.namedWindow("Trackbars")
# resizing the window to 640, 250. The arguments given in are the name of the window, and the width and height
cv2.resizeWindow("Trackbars", 640, 250)
# creating trackbars for the window TRACKBARS. It takes in the arguments of
# name of the trackbar, name of the window, the default set value, the maximum value, callback function
# here the callback function does nothing as we do not need it to do anything
cv2.createTrackbar("Hue Min", "Trackbars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "Trackbars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "Trackbars", 4, 255, empty)
cv2.createTrackbar("Sat Max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Val Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val Max", "Trackbars", 255, 255, empty)

while True:
    _, img = cap.read()
    # converting every frame into hsv type, as it is easier to differentiate colors from.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # using getTrackbarPos to update the current value. this method takes in arguments
    # name of the trackbar and the name of the window
    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv2.getTrackbarPos("VAl Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val Max", "Trackbars")

    # all the values from the getTrackbarsPos are then put into an array using the method np.array
    # the lower array consists of all the lower end values of the hue, saturation and value
    # and the upper array consists of the upper end of the hue saturation and value
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # a mask is used to display the pixels only in the range defined in the inRange method.
    # the arguments taken by the inRange method are the image source, the lower end and the upper end of hsv values to display
    mask = cv2.inRange(hsv, lower, upper)

    # bitwise_and operation is performed on img, to show only the parts that are not black in the mask
    # bitwise operations take arguments of img1 and img2 that are going to be worked on. And a mask.
    # the mask can be understood as rules, for merging the two images. Only the non-black parts of the mask, will be merged
    # and the rest is going to be stored as a black pixel.
    imgR = cv2.bitwise_and(img, img, mask=mask)

    # similarly, an inverse of the mask can be done by using the biwise_not method.
    mask_inv = cv2.bitwise_not(mask)

    img_bg = cv2.bitwise_and(img, img, mask=mask)
    # overlay_fg = cv2.bitwise_and(img, img, mask= mask)

    # dest = cv2.add(img_bg, overlay_fg)
    # cv2.imshow('FINAL', mask_inv)


    cv2.imshow('mask', mask)
    cv2.imshow('final', img_bg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyWindow()
cap.release()
