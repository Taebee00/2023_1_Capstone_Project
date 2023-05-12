#!/usr/bin/python
# -*- coding: utf-8 -*-

import Adafruit_PCA9685
import time
import math

# Initialise the PCA9685 using desired address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)

# Number of servo
servo_num = 12

# Configure min and max servo pulse lengths
servo_min    = 150 # min. pulse length
servo_max    = 600 # max. pulse length
servo_offset = 50

# Set frequency to 60[Hz]
pwm.set_pwm_freq(60)

def AngleToRadian(angle):
    return int(servo_min + math.radians(angle) * (servo_max - servo_min) / math.pi)

# hanoi wonban
# blue : 45 angle
# green : 60 angle
# red : 65 angle
# yellow : 75 angle

ANGLEBOJENG = 20

while True:
	griper_angle = int(input('Enter the gripper angle (0 ~ 90) : ')) + ANGLEBOJENG
	if griper_angle >= 90 + ANGLEBOJENG:
		griper_angle = 90 + ANGLEBOJENG

	pwm.set_pwm(15, 0, AngleToRadian(griper_angle))

	print(f"gripper angle : {griper_angle}")

	time.sleep(1)