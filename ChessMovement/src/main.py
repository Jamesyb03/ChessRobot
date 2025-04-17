# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Billyjimmy                                                   #
# 	Created:      4/16/2025, 11:35:48 PM                                       #
# 	Description:  EXP project     
# 
# 
#                                                #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

# Brain should be defined by default
brain=Brain()

#Chess square size, in cm
SQUARE_SIZE = 2.7
START_LOCATION = (4,7)

#Ports
Turntable = Motor(Ports.PORT1)
Grabber = Motor(Ports.PORT6)
SecondaryArm = Motor(Ports.PORT7)
MainArm = Motor(Ports.PORT8)

#Setting motor power
Grabber.set_velocity(20, PERCENT)
MainArm.set_velocity(20, PERCENT)
SecondaryArm.set_velocity(20, PERCENT)
Turntable.set_velocity(10, PERCENT)


def RadiansToDegrees(radians):
    return radians * 57.2958

def GoToSquare(x,y):
    opposite = SQUARE_SIZE * (4 - x)
    hypotenuse = ((17 + (SQUARE_SIZE * (7 - y))) ** 2 + (opposite ** 2)) ** 0.5
    angle = RadiansToDegrees(math.asin(opposite / hypotenuse))

    Turntable.spin_to_position(angle * 5, DEGREES)
    print(hypotenuse)
    MainArm.spin_to_position(((hypotenuse - 17) / 2.7) * 240, DEGREES)



def Cm_To_Degrees(centimetres):
    return centimetres * 92.6

# Triangle Solving
# Each grid square is by reference to 4, 7
# 0,0 is A1, Bot starts over 4,7 (E8)
# For each difference, add/subtract 250 degrees (one square)
# Then do ((17cm + (Y * 2.7)) ** 2  +  (X * 2.7) ** 2) ** 1/2
# Then use the hypotenuse to do sine rule


def OpenGrabber():
    Grabber.set_velocity(50, PERCENT)
    Grabber.spin_for(REVERSE, 27, DEGREES)
    wait(1, SECONDS)
    

def CloseGrabber():
    wait(1, SECONDS)
    Grabber.set_velocity(5, PERCENT)
    Grabber.spin(FORWARD)
    wait(2, SECONDS)

def LiftGrabber():
    SecondaryArm.spin_for(REVERSE, 180, DEGREES)   


def LowerGrabber():
    SecondaryArm.spin_for(FORWARD, 180, DEGREES)    



def GrabPiece():    
    OpenGrabber()
    LowerGrabber()
    CloseGrabber()    
    LiftGrabber()

def DropPiece():
    LowerGrabber()
    OpenGrabber()
    LiftGrabber()


#Turntable.spin_for(FORWARD, 125, DEGREES)
#LiftGrabber()
#wait(3, SECONDS)

#GrabPiece()

#MainArm.spin_for(FORWARD, Cm_To_Degrees(SQUARE_SIZE), DEGREES)

#DropPiece()

LiftGrabber()
wait(5,SECONDS)
GoToSquare(4,6)
GrabPiece()
GoToSquare(4,4)
DropPiece()
wait(3, SECONDS)




wait(5,SECONDS)
GoToSquare(5,7)
GrabPiece()
GoToSquare(2,4)
DropPiece()
wait(3, SECONDS)










