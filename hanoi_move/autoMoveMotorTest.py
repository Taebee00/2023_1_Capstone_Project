from controlMotor import *
from utils import *
from hanoi import *


def get_wonban_and_color(state, pole):
    wonban_colors = {1: 110, 2: 100, 3: 90, 4: 80}
    wonban = state[pole][0] if state[pole] else None
    return wonban, wonban_colors.get(wonban)


def process_hanoi_state(cm, state, prev_coordinates):
    if state[3][1] in ['A', 'B', 'C']:
        wonban, color = get_wonban_and_color(
            state, ord(state[3][1]) - ord('A'))
        if wonban:
            
            time.sleep(1)
            for j in range(3):
                if j == 1:
                    cm.gripperMove(color)
                    time.sleep(0.5)
                theta_0, theta_1, theta_2 = CalculateTheta(
                    prev_coordinates[j][0], prev_coordinates[j][1], prev_coordinates[j][2])
                cm.target_angles = [theta_0, theta_1, theta_2]
                cm.moveArmSlow()
                time.sleep(1.5)
            
            theta_0, theta_1, theta_2 = CalculateTheta(
                prev_coordinates[2][0], prev_coordinates[2][1], 1)
            cm.target_angles = [theta_0, theta_1, theta_2]
            cm.moveArmSlow()
            time.sleep(0.5)
            cm.gripperMove(0)
            time.sleep(0.5)
            cm.setDefault()
            time.sleep(1.5)


if __name__ == '__main__':
    cm = ControlMotor()
    cm.setDefault()

    # hanoi_3
    # coordinates = [
    #     [[11, 2.2, -1.8], [11.2, 2.2, 2.5], [13.3, -4.5, 2.1]],
    #     [[11, 2.2, -2.5], [11.2, 2.2, 2.3], [11, -0.9, 2.3]],
    #     [[13.4, -4.5, -3.4], [13.4, -4.5, 2.5], [11.9, -0.8, 2.5]],
    #     [[12.3, 2.1, -3.3], [12.5, 2.1, 2.5], [14, -4.8, 2.1]],
    #     [[11, -1, -2.5], [11.3, -1, 2.5], [11.4, 2.1, 2.3]],
    #     [[11, -1, -3], [11.3, -1, 2.5], [13.5, -4.7, 2.2]],
    #     [[11, 2.1, -3], [11.3, 2.2, 2.4], [13.1, -4.5, 2.2]],
    # ]
    # current_state = [[1,2,3], [], []]
    # h = HanoiTower(3)

    #hanoi_4
    coordinates = [
        [[11, 2.2, -1.3], [11.2, 2.2, 2.5], [11, -0.9, 2.3]],
        [[11, 2.2, -1.6], [11.2, 2.2, 2.5], [12.9, -4.2, 2.1]],
        [[11, -1, -3], [11.3, -1, 2.5], [13.5, -4.5, 2.2]], # y should go to + when down but, no change
        [[11, 2.1, -2.5], [11.3, 2.2, 2.4], [11, -0.9, 2.3]],
        [[13.4, -4.5, -2.7], [13.4, -4.5, 2.5], [12, 2.3, 2.3]],
        [[13.4, -4.5, -3.4], [13.4, -4.5, 2.5], [11.9, -0.8, 2.3]],
        [[11, 2.2, -2.5], [11.2, 2.2, 2.3], [11.1, -0.8, 2.3]],
        [[12, 2.3, -3.3],[12.3, 2.4, 2.4],[13.7, -4.5, 2.3]], # modify z +0.2 1st, x + 0.1 3rd, y + 0.1 3rd
        [[11, -1, -1.6],[11.4, -1, 2.5],[13.5, -4.5, 2.3]],
        [[11, -1, -2.5],[11.4, -1, 2.5],[11.5, 2.2, 2.3]],
        [[13.4, -4.5, -2.8],[13.4, -4.5, 2.5],[12, 2.3, 2.5]],
        [[11.5, -1, -3],[11.5, -1, 2.5],[13.4, -4.5, 2.3]],
        [[11, 2.2, -2.5],[11.2, 2.2, 2.5],[11, -0.8, 2.3]],
        [[11, 2.2, -3],[11.2, 2.2, 2.5],[13.1, -4.3, 2.3]], # modify y + 0.1 3rd
        [[11, -1, -3],[11.3, -1, 2.5],[13.5, -4.5, 2.2]] # modify y + 0.1 3rd
    ]
    current_state = [[1, 2, 3, 4], [], []]
    h = HanoiTower(4)
    h.invade_state(current_state)
    flag = 0
    for i in range(len(h.state_history)):
        if flag == 1:
            process_hanoi_state(cm, h.state_history[i], coordinates[i - 1])
            
        if i == h.current_state_idx:
            flag = 1
            print(f"--> {h.state_history[i]}")
        else:
            print(h.state_history[i])



    print(h.current_state_idx)
