from controlMotor import *

if __name__ == '__main__':
    cm = ControlMotor()
    cm.setDefaultMode()  # default

    while True:
        # Input x,y,z coordinates
        x, y, z = map(float, input('Enter the coordinates x,y,z :  ').split())

        # get theta with Inverse Kinematics
        theta_0, theta_1, theta_2 = CalculateTheta(x, y, z)
        theta_3 = cm.getThetaWithInverseKinematics()

        print(f"theta_0 : {theta_0}")
        print(f"theta_1 : {theta_1}")
        print(f"theta_2 : {theta_2}")
        print(f"theta_3 : {theta_3}")

        cm.moveArmSlow()

        ans = input("Gripper haslsee? : ")
        if ans == 'Y' or ans == 'y':
            griper_angle = int(input('Enter the gripper angle (0 ~ 90) : ')) + 90
            cm.gripperMove(griper_angle)

            print(f"gripper angle : {griper_angle}")

        time.sleep(1)
