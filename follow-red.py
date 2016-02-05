#!/usr/bin/env python2


# import required functions
import numpy as np
import cv2

############################################################
# define the functions
# quitting: click into window to stop program
RUN = True
def quit(event, x, y, flags, param):
  global RUN
  if event == cv2.EVENT_LBUTTONDOWN:
    RUN = False

############################################################
# initialise window, video capture
cv2.namedWindow('OpenCV Red')
cv2.moveWindow('OpenCV Red', 10, 10)
cv2.startWindowThread()
cv2.setMouseCallback('OpenCV Red', quit)

cap = cv2.VideoCapture(0)


# main loop
while(RUN):

  # get an image
  ret, frame = cap.read()

  # transform to hsv color model, retain only red (hue range 0:20) with
  # sufficient saturation, and apply median filter to eliminate some noise
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  red = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([20, 255, 255]))
  red = cv2.medianBlur(red, 5)

  # transform to binary (1=red, 0=not red)
  redbin = 1 * (red > 0)
  
  # only do something if more than 5% of the screen is red
  if (np.mean(redbin) > 0.05):
    # calculate column sums
    redsum = np.sum(redbin, axis=0)
    # calculate screen width
    w = redbin.size
    # which side has the most red? (-1 = left of camera, 0 = center, +1 = right of camera)
    side = np.argmax(np.array([np.sum(redbin[:int(w/3)]), 
                               np.sum(redbin[int(w/3):int(2*w/3)]), 
                               np.sum(redbin[int(2*w/3):])
                              ]))
    side = side - 1
  else: 
    side=0
  
  print side
  cv2.imshow('OpenCV Red', cv2.flip(red, 1))  # image, mirrored horizontally

# clean up
cap.release()
cv2.destroyAllWindows()
  

