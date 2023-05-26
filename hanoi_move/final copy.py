from controlMotor import *
from hanoi import *
import jetson.inference
import jetson.utils

"""
    To Do List
    save moving coord in constant
    control motor with hanoi state 
"""
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
    net=jetson.inference.detectNet(argv=["--model=../jetson-inference/python/training/detection/ssd/models/05_23_1100/ssd-mobilenet.onnx", "--labels=../jetson-inference/python/training/detection/ssd/models/05_23_1100/labels.txt", "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes", "--threshold=0.2"])
    camera = jetson.utils.videoSource("/dev/video0")      # "/dev/video0" for V4L2
    display = jetson.utils.videoOutput("display://0") # "my_video.mp4" for file

    cm = ControlMotor()
    h = HanoiTower(4)

    while display.IsStreaming():
        a={}
        b={}
        c={}
        img = camera.Capture()
        detections = net.Detect(img)
        height=display.GetHeight()
        width=display.GetWidth()
        jetson.utils.cudaDrawLine(img,(width/3,0),(width/3,height),(255,255,255,255),5)
        jetson.utils.cudaDrawLine(img,(width/3*2,0),(width/3*2,height),(255,255,255,255),5)	
        
        display.Render(img)
        display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
        for detection in detections :
            if detection.ClassID == 3:
                classId = 1
            elif detection.ClassID == 1:
                classId = 2
            elif detection.ClassID == 2:
                classId = 3
            elif detection.ClassID == 4:
                classId = 4
            if (detection.Center[0]>0 and detection.Center[0]<width/3):
                # a.append(detection.ClassID)
                a[classId] = detection.Center[1]
            elif (detection.Center[0]>width/3 and detection.Center[0]<width/3*2):
                # b.append(detection.ClassID)
                b[classId] = detection.Center[1]
            elif (detection.Center[0]>width/3*2 and detection.Center[0]<width):
                # c.append(detection.ClassID)
                c[classId] = detection.Center[1]
        
        
        sort_a = sorted(a.items(), key = lambda item: item[1])
        sorted_a_labels = [label[0] for label in sort_a]
        
        sort_b = sorted(b.items(), key = lambda item: item[1])
        sorted_b_labels = [label[0] for label in sort_b]
        
        sort_c = sorted(c.items(), key = lambda item: item[1])
        sorted_c_labels = [label[0] for label in sort_c]
    
    
        print(f"a:{sorted_a_labels}\nb:{sorted_b_labels}\nc:{sorted_c_labels}")
        total_cnt = len(sorted_a_labels) + len(sorted_b_labels) + len(sorted_c_labels)
        if (total_cnt == 4):
            current_state = []
            current_state.append(sorted_a_labels)
            current_state.append(sorted_b_labels)
            current_state.append(sorted_c_labels)
            # 타겟 상태로 이동
            h.invade_state(current_state)

            # flag = 0
            # for i in range(len(h.state_history)):
            #     if flag == 1:
            #         process_hanoi_state(cm, h.state_history[i], coordinates[i - 1])
                    
            #     if i == h.current_state_idx:
            #         flag = 1
            #         print(f"--> {h.state_history[i]}")
            #     else:
            #         print(h.state_history[i])
            process_hanoi_state(cm, h.state_history[h.current_state_idx + 1], coordinates[h.current_state_idx - 1 + 1])
            # 현재 탑 상태 인덱스 출력
            print(h.current_state_idx)
            # print(h.get_moves_to_target())

            # state -> coord -> control motor
            

        
