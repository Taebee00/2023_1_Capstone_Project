from controlMotor import *
from utils import *
from hanoi import *


GRIPPER_COLORS = {1: 110, 2: 100, 3: 90}


def get_pole_idx(letter):
    return ord(letter) - ord('A')


def get_wonban(state, pole_letter):
    return state[get_pole_idx(pole_letter)][0] if state[get_pole_idx(pole_letter)] else None


def calculate_and_move(cm, coord, is_grip, gripper_angle):
    theta_0, theta_1, theta_2 = CalculateTheta(*coord)
    print(*coord)
    cm.target_angles = [theta_0, theta_1, theta_2]
    print(theta_0, theta_1, theta_2)
    cm.moveArmSlow()
    if is_grip:
        cm.gripperMove(gripper_angle)
        time.sleep(1)


def execute_movement(cm, coordinates, gripper_angle):
    for coord in coordinates:
        calculate_and_move(cm, coord, coord[1] == 1, gripper_angle)
    cm.gripperMove(0)
    time.sleep(1)
    cm.setDefault()
    time.sleep(1)


if __name__ == '__main__':
    cm = ControlMotor()
    cm.setDefault()
    Yellow = 110
    Red = 100
    Green = 90

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
    current_state = [[1, 2, 3], [], []]
    h = HanoiTower(3)
    h.invade_state(current_state)

    for i, state in enumerate(h.state_history):
        print(f"--> {state}" if i == h.current_state_idx else state)
        if i != h.current_state_idx:
            gripper_angle = GRIPPER_COLORS.get(get_wonban(state, state[3][1]))
            if gripper_angle is not None:
                execute_movement(cm, coordinates[i - 1], gripper_angle)

    print(h.current_state_idx)
