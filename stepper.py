#!/usr/bin/python
#--------------------------------------
#
# Author   : Tomas Stary
# Date     : Sat Sep  6 18:29:14 UTC 2014
# Modified : Fri  5 Feb 10:47:32 GMT 2016
# License  : GNU GPLv3
#
#--------------------------------------

# Import libraries
from time import sleep
import RPi.GPIO as GPIO

def RotateInner(delay = 0.002):
  '''Rotates the inner motor once following the information specified in
  sequence array.  Wait 'delay' ms to allow the movement of the motor.

  '''
  for line in sequence:
    for pin, signal in zip(PINS, line):
      # this sets up the output pins according to the signal on the line
      GPIO.output(pin, signal)

    # take a break to allow the rotation of the axis
    sleep(delay)

def trackMotor():
  ''' Move the motor according to the signals send from the driver.'''
  # forward rotation
  forward = [[1,0,0,0],
             [1,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,1,0],
             [0,0,1,1],
             [0,0,0,1],
             [1,0,0,1]]
  # backward rotation
  backward = forward[:] # copy the list
  backward.reverse()    # reverse the list in place

  global MOVE_SIGNAL  # variable to be changed from parent function
  # initialise security stop to avoid full rotations which could
  # break the Rpi and camera
  sec_stop = 256
  sec_count = sec_count//2

  # Use board GPIO references 
  GPIO.setmode(GPIO.BOARD)
  # Set all pins as output
  for pin in PINS:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, 0)
  print "Output pins set up, waiting for instruction."

  # rotation loop
  while (MOVE_SIGNAL != 'Q') or (MOVE_SIGNAL != 'q'):
    # evaluate the signal and security counter
    if (MOVE_SIGNAL == 'F') and (sec_count < sec_stop):
      RotateInner(forward) # move forward
      sec_count += 1
    else if MOVE_SIGNAL == 'B'and (sec_count > 0):
      RotateInner(backward) # move backward
      sec_count -= 1
    else:
      sleep(0.02) # free parking
    
  # switch off the motor
  for pin in PINS:
    GPIO.output(pin, 0)
  GPIO.cleanup()
  
  print "GPIO cleaned up. The function will terminate."
  
##################################################
# Define properties of the motor

# GPIO pins for the output
# Pins 18,22,24,26
PINS = [18,22,24,26]

##################################################
    

