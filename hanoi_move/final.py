from controlMotor import *
from hanoi import *
import jetson.inference
import jetson.utils

coordinates = [
    [[11, 2.2, -1.3], [11.2, 2.2, 2.5], [11, -0.9, 2.3]],
    [[11, 2.2, -1.8], [11.2, 2.2, 2.5], [12.9, -4.2, 2.1]],
    [[11, -1, -3], [11.3, -1, 2.5], [13.5, -4.5, 2.2]],  # y should go to + when down but, no change
    [[11.2, 2.1, -2.7], [11.4, 2.2, 2.4], [11, -0.8, 2.3]],
    [[13.4, -4.5, -2.9], [13.4, -4.5, 2.5], [12, 2.4, 2.3]],
    [[13.4, -4.5, -3.4], [13.4, -4.5, 2.5], [11.9, -0.8, 2.3]],
    [[11, 2.2, -2.5], [11.2, 2.2, 2.3], [11.1, -0.8, 2.3]],
    [[12, 2.3, -3.4], [12.3, 2.4, 2.4], [13.7, -4.5, 2.3]],  # modify z +0.2 1st, x + 0.1 3rd, y + 0.1 3rd
    [[11, -1, -1.6], [11.4, -1, 2.5], [13.5, -4.5, 2.3]],
    [[11, -1, -2.6], [11.4, -1, 2.5], [11.5, 2.2, 2.3]],
    [[13.4, -4.5, -2.8], [13.4, -4.5, 2.5], [12, 2.3, 2.5]],
    [[11.5, -1, -3], [11.5, -1, 2.5], [13.4, -4.5, 2.3]],
    [[11, 2.2, -2.5], [11.2, 2.2, 2.5], [11, -0.8, 2.3]],
    [[11, 2.2, -3], [11.2, 2.2, 2.5], [13.1, -4.3, 2.3]],  # modify y + 0.1 3rd
    [[11, -1, -3], [11.3, -1, 2.5], [13.5, -4.5, 2.2]]  # modify y + 0.1 3rd
]


def get_disk_and_color(_state, pole):
    disk_colors = {1: 110, 2: 100, 3: 90, 4: 80}
    disk = _state[pole][0] if _state[pole] else None
    return disk, disk_colors.get(disk)


def process_hanoi_state(cm, _state, prev_coordinates):
    if _state[3][1] in ['A', 'B', 'C']:
        disk, color = get_disk_and_color(_state, ord(_state[3][1]) - ord('A'))
        if disk:

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
    net = jetson.inference.detectNet(
        argv=["--model=../jetson-inference/python/training/detection/ssd/models/05_23_1100/ssd-mobilenet.onnx",
              "--labels=../jetson-inference/python/training/detection/ssd/models/05_23_1100/labels.txt",
              "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes", "--threshold=0.3"])
    camera = jetson.utils.videoSource("/dev/video0")  # "/dev/video0" for V4L2
    display = jetson.utils.videoOutput("display://0")  # "my_video.mp4" for file

    cm = ControlMotor()
    h = HanoiTower(4)
    prev_state_labels = []
    cnt = 0

    cm.setDefault()
    while display.IsStreaming():
        state = [{}, {}, {}]
        img = camera.Capture()
        detections = net.Detect(img)
        height = display.GetHeight()
        width = display.GetWidth()
        jetson.utils.cudaDrawLine(img, (width / 3, 0), (width / 3, height), (255, 255, 255, 255), 5)
        jetson.utils.cudaDrawLine(img, (width / 3 * 2, 0), (width / 3 * 2, height), (255, 255, 255, 255), 5)

        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

        check = [0, 0, 0, 0]
        for detection in detections:
            if detection.ClassID == 3:
                classId = 1
            elif detection.ClassID == 1:
                classId = 2
            elif detection.ClassID == 2:
                classId = 3
            elif detection.ClassID == 4:
                classId = 4
            else:
                classId = 0

            if 0 < detection.Center[0] < width / 3:
                # a.append(detection.ClassID)
                state[0][classId] = detection.Center[1]
            elif width / 3 < detection.Center[0] < width / 3 * 2:
                # b.append(detection.ClassID)
                state[1][classId] = detection.Center[1]
            elif width / 3 * 2 < detection.Center[0] < width:
                # c.append(detection.ClassID)
                state[2][classId] = detection.Center[1]

        sort_state = [[], [], []]
        sorted_labels = [[], [], []]
        for i in range(3):
            sort_state[i] = sorted(state[i].items(), key=lambda item: item[1])
            sorted_labels[i] = [label[0] for label in sort_state[i]]

        print(f"a:{sorted_labels[0]}\nb:{sorted_labels[1]}\nc:{sorted_labels[2]}")
        # sujung pilyo
        total_cnt = len(set(sorted_labels[0] + sorted_labels[1] + sorted_labels[2]))
        if sorted_labels == [[], [], [1, 2, 3, 4]]:
            continue

        if len(prev_state_labels) == 0:
            prev_state_labels = sorted_labels

        if prev_state_labels == sorted_labels:
            cnt += 1
        else:
            prev_state_labels = sorted_labels
            cnt = 0

        if cnt == 50 and total_cnt == 4:
            current_state = [sorted_labels[0], sorted_labels[1], sorted_labels[2]]
            # 타겟 상태로 이동
            h.invade_state(current_state)

            process_hanoi_state(cm, h.state_history[h.current_state_idx + 1], coordinates[h.current_state_idx])

            print(h.current_state_idx)
            cnt = 0
