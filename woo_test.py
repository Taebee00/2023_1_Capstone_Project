import math
import Adafruit_PCA9685
import time
import decimal


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
    return int(servo_min + math.radians(angle) * (servo_max - servo_min) / math.pi)


def setPWMwithAngle(theta0, theta1, theta2):
    pwm.set_pwm(0, 0, AngleToRadian(theta0))
    pwm.set_pwm(4, 0, AngleToRadian(theta1))
    pwm.set_pwm(8, 0, AngleToRadian(theta2))


# set default angle
def setDefaultMode():
    setPWMwithAngle(0, 110, 170)


def sqrtXYZ(x=0, y=0, z=0):
    return math.sqrt(x**2 + y**2 + z**2)


def CalcaulteTheta(x, y, z):
    # Flag for Handling when the coordinates in distance from origin
    range_flag = 1 if x**2 + y**2 < math.sqrt(7.5) else 0

    theta_0 = math.atan2(y, x)

    x = x - abs(O_x*math.cos(theta_0)) if x >= 0 else x + \
        abs(O_x*math.cos(theta_0))
    y = y - abs(O_y*math.sin(theta_0)) if y >= 0 else y + \
        abs(O_y*math.sin(theta_0))
    z -= O_z

    theta_2 = math.acos(
        (x**2 + y**2 + z**2 - l_1**2 - l_2**2) / (2 * l_1 * l_2))

    if (range_flag == 1):
        theta_1 = math.atan2(z, -sqrtXYZ(x, y)) + \
            math.asin(l_2 * math.sin(theta_2) / sqrtXYZ(x, y, z))

    else:
        theta_1 = math.atan2(z, sqrtXYZ(x, y)) + \
            math.asin(l_2 * math.sin(theta_2) / sqrtXYZ(x, y, z))

    return theta_0 * (180/math.pi), theta_1 * (180/math.pi), theta_2 * (180/math.pi)


# arm1 & arm2 length
l_1, l_2 = 20, 20
# l_1, l_2 =40, 20


# distance from origin
# O_x, O_y, O_z = 6, 6, 5
# O_x, O_y, O_z = 7.5, 7.5, 5
# O_x, O_y, O_z = 8, 5, 5
O_x, O_y, O_z = 0, 0, 0


while True:
    ans = input("Default?")
    if ans == 'Y' or ans == 'y':
        setDefaultMode()
        current_angles = [0,110,170] # default

    # Input x,y,z coordinates
    x, y, z = map(float, input('Enter the coordinates x,y,z :  ').split())

    # get theta with Inverse Kinematics
    theta_0, theta_1, theta_2 = CalcaulteTheta(x, y, z)
    theta_1+=7
    theta_2+=21
    theta_3=abs(theta_2-theta_1)
    pwm.set_pwm(12, 0, AngleToRadian(theta_3))
    # Start at the Deafult and then move Each Motors for 3steps with 0.07seconds
    for i in range(3):
        target_angle=[theta_0, theta_1, theta_2]
        angle_diff=target_angle[i]-current_angles[i]
        steps=abs(int(angle_diff/5))
        direction = 1 if angle_diff>0 else -1
        for j in range(steps):
            current_angles[i] +=3 * direction
            setPWMwithAngle(current_angles[0], current_angles[1], current_angles[2])
            time.sleep(0.07)


# 