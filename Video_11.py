import cv2

img = cv2.imread('pagecurved.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
retval, threshold = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)
returnv, thresholdgray = cv2.threshold(gray, 10, 255, cv2.COLOR_BGR2GRAY)
# adaptive threshold
adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)

cv2.imshow('ORIGINAL',img)
cv2.imshow('thhreshold', threshold)
cv2.imshow('grayed', thresholdgray)
cv2.imshow('adaptive', adaptive)
cv2.waitKey(0)
cv2.destroyWindow()
