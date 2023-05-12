from controlMotor import *

if __name__ == '__main__':
    cm = ControlMotor()

    while True:
        # Input x,y,z coordinates20 
        x, y, z = map(float, input('Enter the coordinates x,y,z :  ').split())
        # get theta with Inverse Kinematics
        theta_0, theta_1, theta_2 = CalculateTheta(x, y, z)

        cm.target_angles = [theta_0, theta_1, theta_2]
        # cm.setPWMwithAngle([theta_0, theta_1 + 7 , theta_2 + 21])
        # theta_3 = cm.getThetaWithInverseKinematics()

        print(f"theta_0 : {theta_0}")
        print(f"theta_1 : {theta_1}")
        print(f"theta_2 : {theta_2}")
        print(f"theta_3 : {90 - theta_1 + theta_2 + 20}")
        cm.moveArmSlow()

        ans = input("Gripper haslsee? : ")
        if ans == 'Y' or ans == 'y':
            griper_angle = int(input('Enter the gripper angle (0 ~ 90) : ')) 
            cm.gripperMove(griper_angle)

            print(f"gripper angle : {griper_angle}")
        elif ans == 'D' or ans == 'd':
            cm.setDefault()
        time.sleep(1)
