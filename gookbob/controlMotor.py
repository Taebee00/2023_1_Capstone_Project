import Adafruit_PCA9685
from utils import *
import time


class ControlMotor:
    def __init__(self):
        # Initialise the PCA9685 using desired address and/or bus:
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
        # Set frequency to 60[Hz]
        self.pwm.set_pwm_freq(60)
        self.current_angles = [0, 110, 170]
        self.target_angle = self.current_angles

    def setPWMwithAngle(self, thetas):
        self.pwm.set_pwm(12, 0, AngleToRadian(90 - thetas[1] - 7 + thetas[2] - 21 + 20))
        self.pwm.set_pwm(4, 0, AngleToRadian(thetas[1]))
        self.pwm.set_pwm(0, 0, AngleToRadian(thetas[0]))
        self.pwm.set_pwm(8, 0, AngleToRadian(thetas[2]))

    # def setDefaultMode(self):
    #     default_angles = [0, 110, 170]
    #     self.setPWMwithAngle(default_angles)

    #     the_3 = 90 - 110 + 170 + 13
    #     self.pwm.set_pwm(12, 0, AngleToRadian(the_3))
    #     for i in range(3):
    #         angle_diff = self.target_angle[i] - default_angles[i]
    #         steps = abs(int(angle_diff / 3))
    #         direction = 1 if angle_diff > 0 else -1
    #         for j in range(steps):
    #             default_angles[i] += 3 * direction
    #             self.setPWMwithAngle(default_angles)
    #             time.sleep(0.05)
    #     self.current_angles = default_angles

    def getThetaWithInverseKinematics(self):
        # _th_3 = 90 - self.target_angle[1] - 7 + self.target_angle[2] - 21 + 20
        # self.pwm.set_pwm(12, 0, AngleToRadian(_th_3))
        # Move servos on each channel
        self.setPWMwithAngle([self.target_angle[0], self.target_angle[1] + 7, self.target_angle[2] + 21])
        # return _th_3

        print('hi')

    # woo test code (need to modify)
    def moveArmSlow(self):
        for i in range(3):
            angle_diff = self.target_angle[i] - self.current_angles[i]
            steps = abs(int(angle_diff / 3))
            direction = 1 if angle_diff > 0 else -1
            for j in range(steps):
                self.current_angles[i] += 3 * direction
                self.setPWMwithAngle(self.current_angles)
                time.sleep(0.2)

    def gripperMove(self, _ga):
        if _ga >= 180:
            _ga = 180
        elif _ga <= 90:
            _ga = 90
        self.pwm.set_pwm(15, 0, AngleToRadian(_ga))
