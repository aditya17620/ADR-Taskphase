# Correction: a video was used in the lecture, whereas i have used a video feed from the camera
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# using the createBackgroundSubtractor method from cv2 to use it in further steps
# make a mask of the foreground
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    retu, frame = cap.read()
    # the fgbg.apply method makes a mask to show the moving parts of the video
    # and display all static elements as black.
    # takes in the input of the main picture read from the video.
    fgmask = fgbg.apply(frame)

    cv2.imshow('Original', frame)
    cv2.imshow('Foreground', fgmask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cap.destroyAllWindows()
