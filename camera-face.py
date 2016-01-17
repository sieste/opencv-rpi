#!/usr/bin/env python2

import cv2
cv2.namedWindow('window')
cv2.startWindowThread()
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')

QUIT = False
def quit(event, x, y, flags, param):
  global QUIT
  if event == cv2.EVENT_LBUTTONDOWN:
    QUIT = True
cv2.setMouseCallback('window', quit)

while(True):
  ret, frame = cap.read()
  faces = face_cascade.detectMultiScale(frame, 1.3, 5)
  if len(faces) > 0:
    x,y,w,h = faces[0]
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
  cv2.imshow('window', frame)
  if QUIT == True:
    break

cap.release()
cv2.destroyAllWindows()
  
  
