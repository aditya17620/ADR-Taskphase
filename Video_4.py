# Objective: to understand image copying, drawing over image and writing text over image
import cv2

# font object created to store the data of the required font, ie, hershey complex
font = cv2.FONT_HERSHEY_COMPLEX

# reading the image and storing it into object starship
starship = cv2.imread('starship.jpg', cv2.IMREAD_COLOR)

# resizing the image and storing it back into the same object
# using the resize method from cv2. It takes in the source and the dimensions of end image
starship = cv2.resize(starship, (1080, 720))
# converting the BGR picture into a gray image
starshipG = cv2.cvtColor(starship, cv2.COLOR_BGR2GRAY)
# copying a part of the image by specifying the
# start_width:end_width and start_height:end_height
# and storing it into copy_img
copy_img = starship[40:710, 500:600]
# using the putText method to overlay text on the specified image.
# it takes the arguments in the following order:
# source image, text to be overlayed, starting position of the image,
# the font size, and the color of the text
cv2.putText(starship, 'Starship', (0, 650), font, 1, (0, 0, 0))
# displaying the pictures
cv2.imshow('original', starship)
# pasting the copied part of the image onto a new position, with exactly the same number of pixels w*h
starship[40:710, 388:488] = copy_img
cv2.imshow('copied', starship)
# cv2.imshow('gray,full', starshipG)

# waiting infinitely till any key is pressed
cv2.waitKey(0)
