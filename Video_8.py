# Objective: To understand and implement various blur

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([150, 150, 50])
    upper_red = np.array([180, 255, 150])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    # defining kernel size.
    # kernels are a multidimensional array that specifies the factor at which
    # the operations on the image are to be carried out.
    kernel = np.ones((15, 15), np.float32) / 225
    # storing the image using filtered2D method, that takes the
    # input of the source image, (destination of the converted image), ddepth
    # of output image, and the kernel size that specifies the convulusion factor
    smoothed = cv2.filter2D(res, -1, kernel)
    # using GaussianBlur, to smooth the input data. It take the input data as
    # source images, dimension of the kernel, and the sigmaX value that represents the gaussian deviation
    # GaussianBlur uses a weightage model. the weightage varies across the kernels, The element in the
    # centre of the kernel has the most weightage and the kernel at the outer extreme has the least weightage
    blur = cv2.GaussianBlur(res, (15, 15), 0)
    # the medianBlur takes in arguments as the source image, (destination of the image) and the kernel size.
    # the median of all the pixels of the kernel is taken and accepted as the output pixel value.
    median = cv2.medianBlur(res, 15)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    cv2.imshow('blur', blur)
    cv2.imshow('median', median)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyWindow()
cap.release()
