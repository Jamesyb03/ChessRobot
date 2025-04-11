/*----------------------------------------------------------------------------*/
/*                                                                            */
/*    Module:       main.cpp                                                  */
/*    Author:       jbate                                                     */
/*    Created:      4/1/2025, 4:00:30 PM                                      */
/*    Description:  EXP project                                               */
/*                                                                            */
/*----------------------------------------------------------------------------*/
#include "vex.h"

using namespace vex;

// A global instance of vex::brain used for printing to the EXP brain screen
vex::brain       Brain;

// define your global instances of motors and other devices here


int main() {

    Brain.Screen.printAt( 2, 30, "Hello EXP" );

    while(1) {
       
        // Allow other tasks to run
        this_thread::sleep_for(10);
    }

}



