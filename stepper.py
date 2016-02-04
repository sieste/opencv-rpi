#!/usr/bin/python
#--------------------------------------
#
# Author : Tomas Stary
# Date   : Sat Sep  6 18:29:14 UTC 2014
# License: GNU GPLv3
#
#--------------------------------------

# Import libraries
from time import sleep
import RPi.GPIO as GPIO

##################################################
# Define the functions
def init():
  '''Setup pins as output pins of the motor'''
  # Use board GPIO references 
  GPIO.setmode(GPIO.BOARD)
  
  # Set all pins as output
  print "Setting up the output pins."
  for pin in PINS:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, 0)

def RotateInner(delay = 0.002):
  '''Rotates the inner motor once following the information specified in
  sequence array.  Wait 'delay' ms to allow the movement of the motor.

  '''
  for line in sequence:
    for index in range(len(PINS)):
      # this sets up the output pins according to the information on the line
      GPIO.output(PINS[index], line[index])

    # take a break to allow the rotation of the axis
    sleep(delay)

def trackMotor(rotations, sequence):
  ''' Move the motor according to the signals send from the driver.'''
  global MOVE
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

  while (MOVE != 'Q') or (MOVE != 'q'):
    if MOVE == 'F':
      RotateInner(forward)
    if MOVE == 'B':
      RotateInner(backward)
    
  # switch off the motor
  for pin in PINS:
    GPIO.output(pin, 0)
  GPIO.cleanup()
  
##################################################
# Define properties of the motor

# GPIO pins for the output
# Pins 18,22,24,26
PINS = [18,22,24,26]

##################################################
    

