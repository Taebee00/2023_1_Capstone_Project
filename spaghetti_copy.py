import jetson.inference
import jetson.utils

net = jetson.inference.detectNet(argv=["--model=../jetson-inference/python/training/detection/ssd/models/hanoi_05_04_3000/ssd-mobilenet.onnx",
                                 "--labels=../jetson-inference/python/training/detection/ssd/models/hanoi_05_04_3000/labels.txt", "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes", "--threshold=0.2"])
camera = jetson.utils.videoSource("/dev/video0")      # "/dev/video0" for V4L2
display = jetson.utils.videoOutput("display://0")  # "my_video.mp4" for file


class HanoiTower:
    def __init__(self, n):
        # 초기 상태 설정
        self.state = {"A": list(range(1, n + 1)), "B": [], "C": []}
        # 상태 변화 기록
        self.state_history = [[self.state["A"][:],
                               self.state["B"][:], self.state["C"][:]]]
        # 탑의 크기
        self.num_disks = n
        # 현재 탑의 상태 인덱스
        self.current_state_idx = 0
        # 하노이 탑 해결
        self.solve_hanoi(self.num_disks, "A", "C", "B")

    def solve_hanoi(self, num_disks, from_peg, to_peg, via_peg):
        # 탑 크기가 1일 경우
        if num_disks == 1:
            # 디스크 이동
            # print(from_peg, "->", to_peg)
            self.state[to_peg].insert(0, self.state[from_peg][0])
            self.state[from_peg].pop(0)
            # 상태 변화 기록
            self.state_history.append(
                [self.state["A"][:], self.state["B"][:], self.state["C"][:], [from_peg, to_peg]])
        else:
            # 탑 크기가 1이 아닐 경우 재귀 호출을 통해 문제 해결
            self.solve_hanoi(num_disks - 1, from_peg, via_peg, to_peg)
            # 디스크 이동
            # print(from_peg, "->", to_peg)
            self.state[to_peg].insert(0, self.state[from_peg][0])
            self.state[from_peg].pop(0)
            # 상태 변화 기록
            self.state_history.append(
                [self.state["A"][:], self.state["B"][:], self.state["C"][:], [from_peg, to_peg]])
            # 다음 재귀 호출
            self.solve_hanoi(num_disks - 1, via_peg, to_peg, from_peg)

    def get_state_history(self):
        # 상태 변화 기록 반환
        return self.state_history

    def invade_state(self, target_state):
        # 타겟 상태로 이동
        for idx, state in enumerate(self.state_history):
            if state[:3] == target_state:
                self.current_state_idx = idx
                return
        if self.current_state_idx == 0:
            self.current_state_idx = -1

    def get_moves_to_target(self):
        # 현재 상태에서 타겟 상태로 이동하기 위해 수행해야 할 이동 리스트 반환
        moves = []
        for state in self.state_history[self.current_state_idx+1:]:
            moves.append(state[3])
        return moves


while display.IsStreaming():
    a = {}
    b = {}
    c = {}
    img = camera.Capture()
    detections = net.Detect(img)
    height = display.GetHeight()
    width = display.GetWidth()
    jetson.utils.cudaDrawLine(
        img, (width/3, 0), (width/3, height), (255, 255, 255, 255), 5)
    jetson.utils.cudaDrawLine(
        img, (width/3*2, 0), (width/3*2, height), (255, 255, 255, 255), 5)

    for detection in detections:
        if (detection.Center[0] > 0 and detection.Center[0] < width/3):
            # a.append(detection.ClassID)
            a[detection.ClassID] = detection.Center[1]
        elif (detection.Center[0] > width/3 and detection.Center[0] < width/3*2):
            # b.append(detection.ClassID)
            b[detection.ClassID] = detection.Center[1]
        elif (detection.Center[0] > width/3*2 and detection.Center[0] < width):
            # c.append(detection.ClassID)
            c[detection.ClassID] = detection.Center[1]

    sort_a = sorted(a.items(), key=lambda item: item[1])
    sorted_a_labels = [label[0] for label in sort_a]

    sort_b = sorted(b.items(), key=lambda item: item[1])
    sorted_b_labels = [label[0] for label in sort_b]

    sort_c = sorted(c.items(), key=lambda item: item[1])
    sorted_c_labels = [label[0] for label in sort_c]

    print(f"a:{sorted_a_labels} b:{sorted_b_labels} c:{sorted_c_labels}")

    total_cnt = len(sorted_a_labels) + \
        len(sorted_b_labels) + len(sorted_c_labels)
    if (total_cnt == 4):
        current_state = []
        current_state.append(sorted_a_labels)
        current_state.append(sorted_b_labels)
        current_state.append(sorted_c_labels)

        h = HanoiTower(4)

        # 타겟 상태로 이동
        h.invade_state(current_state)

        # 모든 상태 변화 기록 출력
        if h.current_state_idx != -1:
            for x in range(len(h.state_history)):
                if x == h.current_state_idx:
                    print(f"--> {h.state_history[x]}")

                else:
                    print(h.state_history[x])

        # 현재 탑 상태 인덱스 출력
        print(h.current_state_idx)
        # print(h.get_moves_to_target())

    display.Render(img)
    display.SetStatus(
        "Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
