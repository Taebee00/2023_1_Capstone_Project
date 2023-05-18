# from controlMotor import *
from utils import *
from hanoi import *

if __name__ == '__main__':
    # cm = ControlMotor()
    Yellow = 110
    Red = 100
    Green = 90

    # while True:
    current_state = [[1, 2, 3], [], []]
    coordinates = [
        [[11, 2.2, -1.8], [11.2, 2.2, 2.5], [13.4, -4.5, 2.1]],
        [[11, 2.2, -2.5], [11.2, 2.2, 2.3], [11, - 0.9, 2.3]],
        [[13.4, -4.5, -3.4], [13.4, 4.5, 2.5], [12.1, -0.7, 2.5]],
        [[12.3, 2.1, -3], [12.5, 2.1, 2.5], [14, -4.8, 2.1]],
        [[11, -1, -2.5], [11.3, -1, 2.5], [11.5, 2.2, 2.3]],
        [[11, -1, -3], [11.3, -1, 2.5], [13.5, -4.7, 2.2]],
        [[11, 2.1, -3], [11.3, 2.2, 2.3], [13.5, -4.5, 2.2]],
    ]
    h = HanoiTower(3)

    h.invade_state(current_state)

    for i in range(len(h.state_history) - 1):
        if i == h.current_state_idx:
            print(f"--> {h.state_history[i]}")
        else:
            print(h.state_history[i])
            if h.state_history[i][3][2] == 'A':
                wonban = h.state_history[i][0][0]
                if wonban == 1:
                    gripper_angle = Yellow
                elif wonban == 2:
                    gripper_angle = Red
                elif wonban == 3:
                    gripper_angle = Green

            elif h.state_history[i][3][2] == 'B':
                wonban = h.state_history[i][1][0]
                if wonban == 1:
                    gripper_angle = Yellow
                elif wonban == 2:
                    gripper_angle = Red
                elif wonban == 3:
                    gripper_angle = Green

            elif h.state_history[i][3][2] == 'C':
                wonban = h.state_history[i][2][0]
                if wonban == 1:
                    gripper_angle = Yellow
                elif wonban == 2:
                    gripper_angle = Red
                elif wonban == 3:
                    gripper_angle = Green

            for j in range(3):
                theta_0, theta_1, theta_2 = CalculateTheta(
                    coordinates[i][j][0], coordinates[i][j][1], coordinates[i][j][2])
                print(coordinates[i][j][0], coordinates[i]
                      [j][1], coordinates[i][j][2])
                # cm.target_angles = [theta_0, theta_1, theta_2]
                print(theta_0, theta_1, theta_2)
                # cm.moveArmSlow()
                # time.sleep(1)

    print(h.current_state_idx)
