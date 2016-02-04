#!/usr/bin/python
#--------------------------------------
#
# Author : Tomas Stary
# Date   : Sat Sep  6 18:29:14 UTC 2014
# License: GNU GPLv3
#
#--------------------------------------

##################################################
# Change mainly this part of the code

# number of rotations needed
ROTATIONS = 0.5

# frequency of inner motor

##################################################



# Import libraries
from time import sleep
import RPi.GPIO as GPIO


##################################################
# Define the function to rotate inner motor
def RotateInner(sequence):
  '''Rotates the inner motor once following the information specified in sequence array.'''
  for line in sequence:
    for index in range(len(PINS)):
      # this sets up the output pins according to the information on the line
      GPIO.output(PINS[index], line[index])

    # take a break to allow the rotation of the axis
    sleep(DELAY)

def RotateOuter(rotations, sequence):
  ''' Rotate outer axis a number of rotations.'''
  turns = int(rotations*GEAR)
  for i in range(turns):
    RotateInner(sequence)

  # switch of the motor
  for pin in PINS:
    GPIO.output(pin, 0)
    
##################################################    



##################################################
# Set up the board

# Use board GPIO references 
GPIO.setmode(GPIO.BOARD)

# Define GPIO pins for the output
# Pins 18,22,24,26
PINS = [18,22,24,26]

# Set all pins as output
print "Setting up the output pins."
for pin in PINS:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, 0)

##################################################


##################################################
# Define properties of the motor

# the gearing ratio between the inner and outer rotations
GEAR = 512
# delay between the impulses
DELAY = 0.001

# forward rotation
FORWARD = [[1,0,0,0],
           [1,1,0,0],
           [0,1,0,0],
           [0,1,1,0],
           [0,0,1,0],
           [0,0,1,1],
           [0,0,0,1],
           [1,0,0,1]]

# backward rotation
BACKWARD = FORWARD[:] # copy the list
BACKWARD.reverse()    # reverse the list in place
##################################################
    

##################################################
# The actual work

print "Moving the motor."

print "Rotate forward."
RotateOuter(ROTATIONS,FORWARD)
sleep(1)

print "Rotate backward."
RotateOuter(ROTATIONS,BACKWARD)

##################################################
# Clean up
print "Cleaning up the GPIO pins."
GPIO.cleanup()


print "Finished succesfully."


  
