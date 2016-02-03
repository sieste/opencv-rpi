#!/usr/bin/env python2

##################################################
# flags to set up the properties of the script
# this can be later accepted using comand line arguments
filter = True


# import required functions
import cv2
if filter:
  from filter import kalman

############################################################
# define the functions
# quitting: click into window to stop program
RUN = True
def quit(event, x, y, flags, param):
  global RUN
  if event == cv2.EVENT_LBUTTONDOWN:
    RUN = False

############################################################
# initialise window, video capture, and face recognition
cv2.namedWindow('OpenCV face recognition')
cv2.moveWindow('OpenCV face recognition', 10, 10)
cv2.startWindowThread()
cap = cv2.VideoCapture(0)
face_recog = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml')
ret, frame = cap.read()
window_height, window_width = [float(z) for z in frame.shape[0:2]]

cv2.setMouseCallback('OpenCV face recognition', quit)

# initialise kalman filter to smooth the tracking trajectory
m = [window_width/2. - 150., window_height/2. - 150., 300., 300.] # state estimate currently in the middle of the image

# the state uncertainty is now choosen independently from the V and W.
# What would be a reasonable guess? The face can initialy be anywhere, so what is the uncertainty?
P = [1, 1, 1, 1] # state uncertainty
# P = [V[i] + W[i] for i in range(4)] # state uncertainty

# main loop
while(RUN):
  # get an image
  ret, frame = cap.read()

#  # transform to small and grayscale
#  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#  gray = cv2.resize(gray, (0, 0), fx=0.5, fy=0.5)

  # look for faces
  faces = face_recog.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

  if len(faces):
    colr = (255, 0, 0)
    if filter:
      xx, yy, ww, hh = kalman([float(z) for z in faces[0]], P, m)      # filter coordinates
    else:
      xx, yy, ww, hh = faces[0]      # raw coordinates
  else:
    colr = (0, 0, 255)

  # draw the results
  cv2.rectangle(frame,(xx, yy),(xx+ww, yy+hh),colr,2)  # rectangle
  cv2.imshow('OpenCV face recognition', cv2.flip(frame, 1))  # image

# clean up
cap.release()
cv2.destroyAllWindows()
  
  
