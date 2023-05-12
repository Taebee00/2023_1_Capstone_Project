from Adafruit_PCA9685 import PCA9685
from utils import *
import time
import numpy as np


class ControlMotor:
    def __init__(self):
        # Initialise the PCA9685 using desired address and/or bus:
        self.pwm = PCA9685(address=0x40, busnum = 1)
        # Set frequency to 60[Hz]
        self.pwm.set_pwm_freq(60)
        self.default_angles = [90, 180, 190, 45]
        self.current_angles = [90, 110, 170]
        self.target_angles = [90, 110, 170]

    def setDefault(self):
        diff = []
        for i in range(3):
            diff.append(np.linspace(self.current_angles[i], self.default_angles[i], 50))

        for i in range(50):
            for j in range(3):
                self.current_angles[j] = diff[j][i]
                self.setPWMwithAngle(self.current_angles, j)
                time.sleep(.01)
        self.pwm.set_pwm(12, 0, AngleToRadian(45))

    def setPWMwithAngle(self, thetas, num):
        if num == 1:
            self.pwm.set_pwm(4, 0, AngleToRadian(thetas[1]))
        elif num == 0: self.pwm.set_pwm(0, 0, AngleToRadian(thetas[0]))
        elif num == 2 : self.pwm.set_pwm(8, 0, AngleToRadian(thetas[2]))
        self.pwm.set_pwm(12, 0, AngleToRadian(90 - thetas[1] - 7 + thetas[2] - 21 + 20))



    # woo test code (need to modify)
    """
    def moveArmSlow(self):
        for i in range(3):
            angle_diff = self.target_angles[i] - self.current_angles[i]
            steps = abs(int(angle_diff / 10))
            direction = 1 if angle_diff > 0 else -1
            for j in range(steps):
                self.current_angles[i] += 10 * direction
                self.setPWMwithAngle(self.current_angles)
    """
    def moveArmSlow(self):
        diff = []
        diff.append(np.linspace(self.current_angles[0], self.target_angles[0], 50))

        if self.current_angles[0] - self.target_angles[0] != 0:
            diff.append(np.linspace(self.current_angles[1], 110, 50))
            diff.append(np.linspace(self.current_angles[2], 170, 50))
            diff.append(np.linspace(110, self.target_angles[1], 50))
            diff.append(np.linspace(170, self.target_angles[2], 50))

            for i in range(50):
                for j in range(1, 3):
                    self.current_angles[j] = diff[j][i]
                    self.setPWMwithAngle(self.current_angles, j)
                    time.sleep(.01)

            for i in range(50):
                self.current_angles[0] = diff[0][i]
                self.setPWMwithAngle(self.current_angles, 0)
                time.sleep(.01)
            
            for i in range(50):
                for j in range(3, 5):
                    self.current_angles[j - 2] = diff[j][i]
                    self.setPWMwithAngle(self.current_angles, j - 2)
                    time.sleep(.01)
        else:
            diff.append(np.linspace(self.current_angles[1], self.target_angles[1], 50))
            diff.append(np.linspace(self.current_angles[2], self.target_angles[2], 50))
            for i in range(50):
                for j in range(1, 3):
                    self.current_angles[j] = diff[j][i]
                    self.setPWMwithAngle(self.current_angles, j)
                    time.sleep(.01)
    #"""

    def gripperMove(self, _ga):
        if _ga >= 120:
            _ga = 120

        self.pwm.set_pwm(15, 0, AngleToRadian(_ga))
