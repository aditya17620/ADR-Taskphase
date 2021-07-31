# Objective: To impose a youtube logo and show only the ogo instead of the entire picture including the white part.
import cv2

cap = cv2.VideoCapture(0)
overlay = cv2.imread('youtube.png')
overlay = cv2.resize(overlay, (230, 100))

while True:
    ret, img = cap.read()
    # using the shape method to get the values of the rows, columns and the nmber of channels the image has.
    rows,cols,channels = overlay.shape
    # defining the region of image, for us to use it later on in various transformations
    roi = img[0:rows, 0:cols]
    overlayG = cv2.cvtColor(overlay, cv2.COLOR_BGR2GRAY)
    # using the threshold method to make a mask of the image, and then inverse the image.
    retu, mask = cv2.threshold(overlayG, 220, 255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)
    cv2.imshow('output',mask_inv)

    # using the bitwise operation to ge an image with only the masked area
    img_bg = cv2.bitwise_and(roi, roi, mask= mask_inv)
    overlay_fg = cv2.bitwise_and(overlay, overlay, mask= mask)

    # adding the two images using the add method of cv2
    dst = cv2.add(img_bg, overlay_fg)
    # pasting the picture in dst, back into image.
    img[0:rows, 0:cols] = dst

    cv2.imshow('FINAL', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.waitKey(0)

cap.release()
cv2.destroyWindow()
