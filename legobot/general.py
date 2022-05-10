#!/usr/bin/python
import os, sys
import ctypes
KIPR=ctypes.CDLL("/usr/lib/libkipr.so")

# CONSTANTS

R_MOTOR = 0
L_MOTOR = 1

TOPH_RIGHT = 0
TOPH_LEFT = 1
TOPH_BRIGHT = 2
TOPH_BLEFT = 3
LS = 5
    
ARM_SERVO = 0
    
UP = 900
GROUND = 1800

BLACK = 2500
BACK_BLACK = 3800  

def move(l_power, r_power, sleep_time=5):
    KIPR.motor(L_MOTOR, l_power)
    KIPR.motor(R_MOTOR, r_power)
    KIPR.msleep(sleep_time)

def stop(s_time):
	move(0, 0, s_time)
        
def go_to_black(l_power=50, r_power=50):
    while(KIPR.analog(TOPH_LEFT) < BLACK or KIPR.analog(TOPH_RIGHT) < BLACK):
        move(l_power, r_power)
            
def go_to_white(l_power=50, r_power=50):
    while(KIPR.analog(TOPH_LEFT) > BLACK or KIPR.analog(TOPH_RIGHT) > BLACK):
        move(l_power, r_power)
            
def servo_control(servo_name, end_pos, rate=50):
    pos = KIPR.get_servo_position(servo_name)
    if pos > end_pos:
        for i in range(pos, end_pos, -rate):
            KIPR.set_servo_position(servo_name, i)
            KIPR.msleep(rate)
    else:
        for i in range(pos, end_pos, rate):
            KIPR.set_servo_position(servo_name, i)
            KIPR.msleep(rate)
                
def line_follow(time, sensor=TOPH_LEFT):
    end_time = KIPR.seconds() + time
    while(KIPR.seconds() < end_time):
        if(KIPR.analog(sensor) > BLACK):
            if(sensor == TOPH_LEFT):
                move(37, 50)
            else:
                move(50, 37)
        else:
            if(sensor == TOPH_LEFT):
                move(50, 37)
            else:
                move(37, 50)
                    
def blf(time):
    end_time = KIPR.seconds() + time
    while(KIPR.seconds() < end_time):
	if(KIPR.analog(TOPH_BRIGHT) < BACK_BLACK and KIPR.analog(TOPH_BLEFT) < BACK_BLACK):
	    move(-50, -50)
	elif(KIPR.analog(TOPH_BRIGHT) < BACK_BLACK and KIPR.analog(TOPH_BLEFT) > BACK_BLACK):
	    move(-37, -50)
	elif(KIPR.analog(TOPH_BRIGHT) > BACK_BLACK and KIPR.analog(TOPH_BLEFT) < BACK_BLACK):
	    move(-50, -37)
                    
def jitter():
	servo_control(ARM_SERVO, 900, 600)
	servo_control(ARM_SERVO, 1600, 600)
	move(100, 0, 200)
	move(-100, 0, 200)
	move(0, 100, 200)
	move(0, -100, 200)
	stop(100)
        
def wfl():
	START = KIPR.analog(LS)
	while(KIPR.analog(LS) > START/2):
		stop(100)
      
def setup():
    KIPR.enable_servos()
    servo_control(ARM_SERVO, GROUND)
    wfl()
                
def main():
	
	go_to_black(100, 100)
	go_to_white(100, 100)
	move(100, 0, 1400)
	move(100, 100, 400)
	line_follow(20500)
	stop(500)
	servo_control(ARM_SERVO, UP)
	jitter()
	line_follow(1200)
	servo_control(ARM_SERVO, GROUND)
    
	blf(20000)
	stop(200)
	move(-100, 0, 1900)
	move(-50, -50, 4000)
        
	KIPR.ao()
	KIPR.disable_servos()
    
if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    setup()
    main()
