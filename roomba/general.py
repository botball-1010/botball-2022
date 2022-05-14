#!/usr/bin/python
import os, sys
import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")

## constants
slow_speed = 100
fast_speed = 250

base_servo = 1
top_servo = 3

LS = 5

## built in wrappers

# return gyroscope val
def _gyro_val():
    return(KIPR.gyro_z())

# suspend for n miliseconds
def msleep(time):
    KIPR.msleep(time)

# drive roomba
def _drive_direct(left_power, right_power):
    KIPR.create_drive_direct(left_power, right_power)

# all off
def stop():
    _drive_direct(0,0)

# turn roomba on
def turn_on():
    KIPR.create_connect()
    print("Connected!")
    KIPR.enable_servos()
    print("Enable Servos")
    


## top level functions for use

# function for using servo
def servo_control(servo_name, end_pos, rate=1):
    pos = KIPR.get_servo_position(servo_name)
    print(pos, end_pos)
    if pos > end_pos:
        for i in range(pos, end_pos, -rate):
            KIPR.set_servo_position(servo_name, i)
            KIPR.msleep(rate)
    else:
        for i in range(pos, end_pos, rate):
            KIPR.set_servo_position(servo_name, i)
            KIPR.msleep(rate)

# drives forward for n miliseconds
def drive(left_power, right_power, duration):
    _drive_direct(left_power, right_power)
    msleep(duration)
    stop()    

# main routines
def wfl():
    START = KIPR.analog(LS)
    while(KIPR.analog(LS) > START/2):
        pause(50)

def back_align():
    drive(-100, -100, 500)

def straighten_claw():
    servo_control(base_servo, 1450)

def claw_open():
    servo_control(top_servo, 0)
    
def claw_tighten():
    servo_control(top_servo, 590)

def drive_towards_rings():
    drive(50, 50, 2950)    

def left_rotate_servo():
    servo_control(base_servo, 0, rate=150)
    drive(200, -200, 950)

def drive_toward_cylinder():
    drive(107, 100, 3050)


def cylinder_align():
    drive(100, -100, 2100)

def pause(time):
    _drive_direct(0, 0)
    msleep(time)

def reset():
    servo_control(base_servo, 330)
    servo_control(top_servo, 750)

def main():

    # Roomba Setup
    turn_on()
    reset()
    
    # Wait for light start
    wfl()

    KIPR.shut_down_in(119)


    # back align with wall in start box
    back_align()

    # Move claw into operating position
    straighten_claw()
    claw_open()

    # Set Roomba to Claw Position
    drive_towards_rings()

    # Reduce extraneous momentum 
    pause(50)

    # Tighten claw around rings
    claw_tighten()

    # Rotate Claw and Rotate Roomba to Remove Rings  
    left_rotate_servo()
    
    # Align Roomba to Rotation Position
    drive_toward_cylinder()

    # Rotate Roomba to Insert Rings into Cylinder
    cylinder_align()

    # Release rings
    claw_open()



if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();



    
