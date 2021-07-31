import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    # laplacian edge detection works by searching for zero-crossings in the second derivative of images.
    # Laplacian kernel looks similar to
    # [-1 -1 -1]
    # [-1  8 -1]
    # [-1 -1 -1]
    laplacian = cv2.Laplacian(frame, cv2.CV_64F)
    # sobel filters are another edge detection. It uses the maximum
    # and minimum values of the first derivative of x and y to figure out the edges and difference in intensities
    # sobelx uses a kernel that roughly looks like
    # [1 0 -1]
    # [2 0 -2]
    # [1 0 -1]
    # and gives an result that looks more definitivily in the x axis
    sobelx = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
    # sobely uses a kernel that rougly looks like
    # [1 2 -1]
    # [0 0  0]
    # [1 2 -1]
    # and gives a result that looks more definitevely in the y axis
    # to get the best results using a sobel filter,
    # both sobel x and y filters should be used.
    sobely = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=5)
    # canny filter is another edge-detection filter thst uses multiple steps to get the best possible result.
    # It first applies a gaussian filter to remove noise and then finds the intensity gradient of the image.
    # Canny works by applying non-maximum compression. It applies double threshhold to find probable edges.
    # and then tracks the edges and removes weaker/softer edges that do not seem to be connvcted to more significant edges.
    edge = cv2.Canny(frame, 150, 255)

    cv2.imshow('original', frame)
    cv2.imshow('Laplacian', laplacian)
    cv2.imshow('Sobelx', sobelx)
    cv2.imshow('sobely', sobely)
    cv2.imshow('canny', edge)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyWindow()
cap.release()

# https://www.cs.auckland.ac.nz/compsci373s1c/PatricesLectures/Edge%20detection-Sobel_2up.pdf
# to understand sobel concept better
