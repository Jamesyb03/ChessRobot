# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       jbate                                                        #
# 	Created:      4/11/2025, 11:51:58 AM                                       #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

# Brain should be defined by default
brain = Brain()

# Chess square size, in cm
SQUARE_SIZE = 2.7
START_LOCATION = (4, 7)

# Ports
Turntable = Motor(Ports.PORT1)
Grabber = Motor(Ports.PORT6)
SecondaryArm = Motor(Ports.PORT7)
MainArm = Motor(Ports.PORT8)

# Setting motor power
Grabber.set_velocity(20, PERCENT)
MainArm.set_velocity(20, PERCENT)
SecondaryArm.set_velocity(20, PERCENT)
Turntable.set_velocity(10, PERCENT)

def RadiansToDegrees(radians):
    return radians * 57.2958

def GoToSquare(x, y):
    opposite = SQUARE_SIZE * (4 - x)
    hypotenuse = ((17 + (SQUARE_SIZE * (7 - y))) ** 2 + (opposite ** 2)) ** 0.5
    angle = RadiansToDegrees(math.asin(opposite / hypotenuse))

    Turntable.spin_to_position(angle * 5, DEGREES)
    print(hypotenuse)
    MainArm.spin_to_position(((hypotenuse - 17) / 2.7) * 240, DEGREES)

def GrabPiece():
    OpenGrabber()
    LowerGrabber()
    CloseGrabber()
    LiftGrabber()

def DropPiece():
    LowerGrabber()
    OpenGrabber()
    LiftGrabber()

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

if __name__ == "__main__":
    while True:
        try:
            GoToSquare(0, 0)  # Move to the starting position
            # Input coordinates for GoToSquare
            x = int(input("Enter the column (0-7): "))
            y = int(input("Enter the row (0-7): "))

            # Validate input
            if not (0 <= x <= 7 and 0 <= y <= 7):
                print("Invalid coordinates. Please enter values between 0 and 7.")
                continue

            # Move to the specified square
            GoToSquare(x, y)

            # Ask if the user wants to grab or drop a piece
            action = input("Do you want to 'grab', 'drop', or 'exit'? ").strip().lower()
            if action == "grab":
                GrabPiece()
            elif action == "drop":
                DropPiece()
            elif action == "exit":
                print("Exiting program.")
                break
            else:
                print("Invalid action. Please enter 'grab', 'drop', or 'exit'.")

        except ValueError:
            print("Invalid input. Please enter integers for coordinates.")