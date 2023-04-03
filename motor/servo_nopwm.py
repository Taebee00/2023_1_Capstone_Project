
import time

from board import SCL, SDA
import busio

from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)

pca.frequency = 50


servo4 = servo.Servo(pca.channels[4])
servo5 = servo.Servo(pca.channels[5])
servo6 = servo.Servo(pca.channels[6])
servo7 = servo.Servo(pca.channels[7])
servo8 = servo.Servo(pca.channels[8])
servo9 = servo.Servo(pca.channels[9])
servo10 = servo.Servo(pca.channels[10])
servo_list = [servo4, servo5, servo6, servo7, servo8, servo9, servo10]

for i in range(0, 7):
    servo_list[i].angle = 0
    time.sleep(1)
    servo_list[i].angle = 180
    time.sleep(1)

pca.deinit()
