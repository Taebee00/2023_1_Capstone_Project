from controlMotor import *
from utils import *
from hanoi import *


def get_wonban_and_color(state, pole):
    wonban_colors = {1: 110, 2: 100, 3: 90}
    wonban = state[pole][0] if state[pole] else None
    return wonban, wonban_colors.get(wonban)


def process_hanoi_state(cm, state, prev_coordinates):
    if state[3][1] in ['A', 'B', 'C']:
        wonban, color = get_wonban_and_color(
            state, ord(state[3][1]) - ord('A'))
        if wonban:
            cm.gripperMove(color)
            time.sleep(1)
            for j in range(3):
                theta_0, theta_1, theta_2 = CalculateTheta(
                    prev_coordinates[j][0], prev_coordinates[j][1], prev_coordinates[j][2])
                cm.target_angles = [theta_0, theta_1, theta_2]
                cm.moveArmSlow()
                time.sleep(1.5)

            theta_0, theta_1, theta_2 = CalculateTheta(
                prev_coordinates[2][0], prev_coordinates[2][1], 1)
            cm.target_angles = [theta_0, theta_1, theta_2]
            cm.moveArmSlow()
            time.sleep(1.5)
            cm.gripperMove(0)
            time.sleep(1.5)
            cm.setDefault()
            time.sleep(1.5)


if __name__ == '__main__':
    cm = ControlMotor()
    cm.setDefault()
    # while True:
    coordinates = [
        [[11, 2.2, -1.8], [11.2, 2.2, 2.5], [13.3, -4.5, 2.1]],
        [[11, 2.2, -2.5], [11.2, 2.2, 2.3], [11, -0.9, 2.3]],
        [[13.4, -4.5, -3.4], [13.4, -4.5, 2.5], [11.9, -0.8, 2.5]],
        [[12.3, 2.1, -3.3], [12.5, 2.1, 2.5], [14, -4.8, 2.1]],
        [[11, -1, -2.5], [11.3, -1, 2.5], [11.4, 2.1, 2.3]],
        [[11, -1, -3], [11.3, -1, 2.5], [13.5, -4.7, 2.2]],
        [[11, 2.1, -3], [11.3, 2.2, 2.4], [13.1, -4.5, 2.2]],
    ]
    # while True:
    current_state = [[1, 2, 3], [], []]
    h = HanoiTower(3)
    h.invade_state(current_state)

    for i in range(len(h.state_history)):
        if i == h.current_state_idx:
            print(f"--> {h.state_history[i]}")
        else:
            print(h.state_history[i])
            process_hanoi_state(cm, h.state_history[i], coordinates[i - 1])

    print(h.current_state_idx)
