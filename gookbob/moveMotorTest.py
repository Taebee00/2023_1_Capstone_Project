from controlMotor import *

if __name__ == '__main__':
    cm = ControlMotor()

    while True:
        # Input x,y,z coordinates20 
        x, y, z = map(float, input('Enter the coordinates x,y,z :  ').split())
        if x == 0 and y == 0 and z == 0:
            cm.setDefault()
        # get theta with Inverse Kinematics
        else:
            theta_0, theta_1, theta_2 = CalculateTheta(x, y, z)

            cm.target_angles = [theta_0, theta_1, theta_2]
            # cm.setPWMwithAngle([theta_0, theta_1 + 7 , theta_2 + 21])
            # theta_3 = cm.getThetaWithInverseKinematics()

            print(f"theta_0 : {theta_0}")
            print(f"theta_1 : {theta_1}")
            print(f"theta_2 : {theta_2}")
            print(f"theta_3 : {90 - theta_1 + theta_2 + 20}")
            cm.moveArmSlow()

            ans = input("Default or gripper : ")
            
            if ans == 'G' or ans == 'g':
                griper_angle = int(input('Enter the gripper angle (0 ~ 90) : ')) 
                cm.gripperMove(griper_angle)

                print(f"gripper angle : {griper_angle}")
            elif ans == 'D' or ans == 'd':
                cm.setDefault()

        time.sleep(1)
