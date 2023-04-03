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

# Caluate the angle to radian
def AngleToRadian(angle):
    return int(servo_min + angle*(math.pi/180) * (servo_max - servo_min) / math.pi)


def setPWMwithAngle(theta0, theta1, theta2):
    pwm.set_pwm(0, 0, AngleToRadian(theta0))
    pwm.set_pwm(4, 0, AngleToRadian(theta1))
    pwm.set_pwm(8, 0, AngleToRadian(theta2))
    

# set default angle
def setDefaultMode():
    setPWMwithAngle(90, 110, 170)
    
    
def sqrtXYZ(x=0, y=0, z=0):
    return math.sqrt(x**2 + y**2 + z**2)
    

def CalcaulteTheta(x,y,z):
    # Flag for Handling when the coordinates in distance from origin
    range_flag = 1 if x**2 + y**2 < 36 else 0

    theta_0 = math.atan2(y,x)
    
    x = x - abs(O_x*math.cos(theta_0)) if x >= 0 else x + abs(O_x*math.cos(theta_0))
    y = y - abs(O_y*math.sin(theta_0)) if y >= 0 else y + abs(O_y*math.sin(theta_0))
    z -= O_z

    theta_2 = math.acos((x**2 + y**2 + z**2 - l_1**2 - l_2**2) / (2 * l_1 * l_2))
    
    if (range_flag == 1) :
        theta_1 = math.atan2(z, -sqrtXYZ(x,y)) + math.asin(l_2 * math.sin(theta_2) / sqrtXYZ(x,y,z))

    else : 
        theta_1 = math.atan2(z, sqrtXYZ(x,y)) + math.asin(l_2 * math.sin(theta_2) / sqrtXYZ(x,y,z))
        
    return theta_0 * (180/math.pi), theta_1 * (180/math.pi), theta_2 * (180/math.pi)


# arm1 & arm2 length
l_1, l_2 =20, 20


# distance from origin
O_x, O_y, O_z = 6, 6, 5
    

while True: 
    ans=input("Default?")
    if ans=='Y' or ans=='y':
        setDefaultMode()
        
    # Input x,y,z coordinates
    x,y,z = map(float, input('Enter the coordinates x,y,z :  ').split())
    
    
    # get theta with Inverse Kinematics
    theta_0, theta_1, theta_2 = CalcaulteTheta(x,y,z)
    
    # Move servos on each channel
    setPWMwithAngle(theta_0, theta_1, theta_2)
    

    print(f"theta_0 : {theta_0}")
    print(f"theta_1 : {theta_1}")
    print(f"theta_2 : {theta_2}")
    time.sleep(1)
