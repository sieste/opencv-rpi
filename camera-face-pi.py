#!/usr/bin/env python2

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os.path

camera = PiCamera()
rawCapture = PiRGBArray(camera)
# saved classifier xml in local directory
xmlfile = './haarcascade_frontalface_alt2.xml'
if not os.path.isfile(xmlfile):
  print "classifier xml file not found ... exiting"
  quit()

face_recog = cv2.CascadeClassifier(xmlfile)

# # initialise kalman filter to smooth the tracking trajectory
# ret, frame = cap.read()
# window_height, window_width = [float(z) for z in frame.shape[0:2]]
# W = [10., 10., 1., 1.] # process variance (left/right variance is larger than depth variance)
# V = [100., 100., 100., 100.] # observational variance
# m = [window_width/2. - 150., window_height/2. - 150., 300., 300.] # state estimate
# P = [V[i] + W[i] for i in range(4)] # state uncertainty
# obs = m # init observation vector

time.sleep(1)
camera.capture(rawCapture, format="bgr")
frame = rawCapture.array
print frame.shape

faces = face_recog.detectMultiScale(frame, 1.3, 5)
print faces



# # main loop
# while(True):
# 
# 
#   # get an image
#   ret, frame = cap.read()
# 
#   camera.capture(rawCapture, format="bgr")
#   frame = rawCapture.array
# 
# 
#   # look for faces
#   faces = face_recog.detectMultiScale(frame, 1.3, 5)
#   if len(faces) > 0:
# 
#     obs = [float(z) for z in faces[0]]
#     print obs
# 
#    # kalman-filter equations
#    for i in range(4):
#      K = (P[i] + W[i]) / (P[i] + W[i] + V[i]) # kalman gain
#      m[i] = m[i] + K * (obs[i] - m[i]) # updated state estimate
#      P[i] = (1 - K) * (P[i] + W[i]) # updated state uncertainty
#
#    colr = (255, 0, 0)
#  else:
#    colr = (0, 0, 255)
#
#
#  # draw rectangle using raw coordinates
#  xx, yy, ww, hh = int(obs[0]), int(obs[1]), int(obs[2]), int(obs[3])
#  cv2.rectangle(frame,(xx, yy),(xx+ww, yy+hh),(0,0,255),1)
#
#
# # # draw rectangle using filtered coordinates
# # xxf, yyf, wwf, hhf = int(m[0]), int(m[1]), int(m[2]), int(m[3])
# # cv2.rectangle(frame,(xxf, yyf),(xxf+wwf, yyf+hhf),colr,2)
#
#
#  # draw image
#  cv2.imshow('OpenCV face recognition', cv2.flip(frame, 1))
#
#
#  if QUIT == True:
#    break


# cap.release()
# cv2.destroyAllWindows()
  
  
