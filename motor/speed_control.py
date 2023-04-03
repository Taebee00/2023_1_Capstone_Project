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


# Caluate the angle to radian
def AngleToRadian(angle):
    return int(servo_min + angle*(math.pi/180) * (servo_max - servo_min) / math.pi)


def setPWMwithAngle(num, angle):
    pwm.set_pwm(num, 0, AngleToRadian(angle))

prev_a = 0
prev_b = 0


while True:
    a, b = map(int, input("각도를 입력하삼 : ").split())
    
    if a < prev_a:
        for i in range(a, prev_a, -1):
            setPWMwithAngle(0, i)
            time.sleep(0.01)  # 대기 시간을 0.01초로 수정
    else:
        for i in range(prev_a, a):
            setPWMwithAngle(0, i)
            time.sleep(0.01)  # 대기 시간을 0.01초로 수정
    
    if b < prev_b:
        for i in range(b, prev_b, -1):
            setPWMwithAngle(4, i)
            time.sleep(0.01)  # 대기 시간을 0.01초로 수정
    else:
        for i in range(prev_b, b):
            setPWMwithAngle(4, i)
            time.sleep(0.01)  # 대기 시간을 0.01초로 수정

    prev_a = a  # prev_a와 prev_b를 갱신해 주어야 합니다.
    prev_b = b
    
        

