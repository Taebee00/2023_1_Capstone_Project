import math
import Adafruit_PCA9685
import time

# Initialise the PCA9685 using desired address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

# Number of servos
servo_num = 12

# Configure min and max servo pulse lengths
servo_min = 150  # min. pulse length
servo_max = 600  # max. pulse length
servo_offset = 50

# Set frequency to 60[Hz]
pwm.set_pwm_freq(60)

l_1 = 10
l_2 = 17

pwm.set_pwm(4, 0, 150)
pwm.set_pwm(8, 0, 150)

while True:
    # Input x,y coordinates1
    x = int(input("X : "))
    y = int(input("Y : "))

    theta_2 = math.acos((x**2 + y**2 - l_1**2 - l_2**2) / (2 * l_1 * l_2))
    theta_1 = math.atan2(y, x) + math.asin(l_2 * math.sin(theta_2) / math.sqrt(x**2 + y**2))

    # Move servos on each channel
    # pwm 핀 theta 에 맞게 잘 설정했는지 확인하기1
    pwm.set_pwm(4, 0, int(servo_min + theta_1 * (servo_max - servo_min) / math.pi))
    pwm.set_pwm(8, 0, int(servo_min + theta_2 * (servo_max - servo_min) / math.pi))

    print(f"{150 + int(int(theta_1) * 2.8)}")
    print(f"{150 + int(int(theta_2) * 2.8)}")
    # print(f"theta_1 : {int(servo_min + theta_1 * (servo_max - servo_min) / math.pi)}")
    # print(f"theta_2 : {int(servo_min + theta_2 * (servo_max - servo_min) / math.pi)}")
    # pwm.set_pwm(0, 0, 150 + int(int(theta_1) * 2.8))
    # pwm.set_pwm(4, 0, 150 + int(int(theta_2) * 2.8))

    time.sleep(1)
