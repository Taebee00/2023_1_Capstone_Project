import math
import Adafruit_PCA9685
import time

# Initialise the PCA9685 using desired address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

# Configure min and max servo pulse lengths
servo_min = 150  # min. pulse length
servo_max = 600  # max. pulse length
servo_offset = 50

# Set frequency to 60[Hz]
pwm.set_pwm_freq(60)

l_1 = 20
l_2 = 20

pwm.set_pwm(0, 0, 150)
pwm.set_pwm(4, 0, 150)
pwm.set_pwm(8, 0, 150)


x = 30
y = 10
z = 10
theta_0 = math.atan2(y,x)
if (x >= 0) :
        x -= abs(5.5*math.cos(theta_0))
else :
        x += abs(5.5*math.cos(theta_0))
if (y >= 0):
        y -= abs(5.5 *math.sin(theta_0))
else :
        y += abs(5.5 *math.sin(theta_0))
z-=5

while True:
    # Input x,y coordinates1
        
    x = x - 1
    
    print(x)
    

    
    
    theta_2 = math.acos((x**2 + y**2 + z**2 - l_1**2 - l_2**2) / (2 * l_1 * l_2))
    theta_1 = math.atan2(z,(math.sqrt(x**2+y**2))) + math.asin(l_2 * math.sin(theta_2) / math.sqrt(x**2 + y**2 + z**2))
    
    # R = math.sqrt(x**2 + y**2)
    
    # if ((R > l_1 * math.cos(theta_1) + l_2 * math.cos(theta_1 - theta_2) and R < 7) or (z > l_1 * math.sin(theta_1) and z < 7)):
    #     print("범위를 넘어갔습니다.")
    #     continue;
    
    
    # Move servos on each channel
    # pwm 핀 theta 에 맞게 잘 설정했는지 확인하기
    pwm.set_pwm(0, 0, int(servo_min + theta_0 * (servo_max - servo_min) / math.pi))
    pwm.set_pwm(4, 0, int(servo_min + theta_1 * (servo_max - servo_min) / math.pi))
    pwm.set_pwm(8, 0, int(servo_min + theta_2 * (servo_max - servo_min) / math.pi))
    

    print(f"{150 + int(int(theta_1) * 2.8)}")
    print(f"{150 + int(int(theta_2) * 2.8)}")

    time.sleep(1)
