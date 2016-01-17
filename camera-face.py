#!/usr/bin/env python2

import cv2
import numpy as np

cv2.namedWindow('window')
cv2.startWindowThread()
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')


# quitting sequence: click into window to stop program
QUIT = False
def quit(event, x, y, flags, param):
  global QUIT
  if event == cv2.EVENT_LBUTTONDOWN:
    QUIT = True
cv2.setMouseCallback('window', quit)


# initialise kalman filter
m = [200., 200., 50., 50.] # state estimate
obs = m
P = [1., 1., 1., 1.] # state variance
W = [10., 10., 1., 1.] # process variance (left/right variance is faster than depth variance)
V = [25., 25., 25., 25.] # observational variance

# main loop
while(True):
  ret, frame = cap.read()
  faces = face_cascade.detectMultiScale(frame, 1.3, 5)
  if len(faces) > 0:
    obs = [float(z) for z in faces[0]]

    # kalman filter equations
    for i in range(4):
      K = (P[i] + W[i]) / (P[i] + W[i] + V[i])
      m[i] = m[i] + K * (obs[i] - m[i])
      P[i] = (1 - K) * (P[i] + W[i])

  # unfiltered face
  xx, yy, ww, hh = int(obs[0]), int(obs[1]), int(obs[2]), int(obs[3])
  cv2.rectangle(frame,(xx, yy),(xx+ww, yy+hh),(0,0,255),1)

  # noise-filtered face
  xxf, yyf, wwf, hhf = int(m[0]), int(m[1]), int(m[2]), int(m[3])
  cv2.rectangle(frame,(xxf, yyf),(xxf+wwf, yyf+hhf),(255,0,0),2)

  # draw image
  cv2.imshow('window', frame)

  if QUIT == True:
    break

cap.release()
cv2.destroyAllWindows()
  
  
