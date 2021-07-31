# Aim: To read input from the webcam, Store the video, and also output
# the same video feed in gray and BGR colors until 'q' is pressed to quit.

import cv2

# VideoCapture is used to get the information from the user and it takes the argument of which webcam is to be used.
# cap is a video capture object. This object is later used to manipulate the video feed as required.
cap = cv2.VideoCapture(0)
# fourcc is also an object that holds the required information (codec) for the video to be saved.
# It is then used on the VideoWriter method.
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# defining an object for VideoWriter where the arguments are
# the output name, codec, fps and the size of the video frame.
vid = cv2.VideoWriter('Test.avi', fourcc, 20.0, (640, 480))

# creating a for loop to read the data from the specified webcam infinitely
while True:
    ret, img = cap.read()
    # cvtColor used to convert the color of the image from BGR to gray
    # using COLOR_BGR2GRAY to specify the initial and end color required and then storing the data into imgG
    imgG: None = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # saving the 'vid; file onto the device using the write method. It takes in img as an argument
    vid.write(img)
    # using the imshow method to print out the output.
    # its arguments are the name of the window, and the object that holds the image data
    cv2.imshow('OUTPUT', img)
    cv2.imshow('GRAY', imgG)

    # using the waitKey method to wait for a set time for any keyboard event
    # using the ord function to check for the input of the letter 'q'
    # if both conditions are true, the program will break out of the while loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# the release method is used to release the camera from
# the program, so that other applications can use it
cap.release()
vid.release()
