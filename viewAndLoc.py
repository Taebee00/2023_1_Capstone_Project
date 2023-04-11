import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        arr = []
        success, image = cap.read()
        if not success:
            print("웹캠을 찾을 수 없습니다.")
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = face_detection.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)
                location = detection.location_data
                for keypoint in location.relative_keypoints:
                    arr.append([keypoint.x, keypoint.y])

                # 좌우 시점 판별 / 왼쪽 귀와 눈 사이 거리와 오른쪽 귀와 눈 거리 사이를 비교하여 판별
                if abs((arr[0][0] - arr[4][0]) - (arr[5][0] - arr[1][0])) < 0.05:
                    view = "mid "
                elif arr[0][0] - arr[4][0] < arr[5][0] - arr[1][0]:
                    view = "left "
                elif arr[0][0] - arr[4][0] > arr[5][0] - arr[1][0]:
                    view = "right "

                # 상하 시점 판별 / 코와 입 사이 거리와 눈과 코 사이 거리 차이를 비교하여 판별
                if abs((arr[2][1] - arr[0][1]) - (arr[3][1] - arr[2][1])) < 0.05:
                    view += "mid"
                elif arr[2][1] - arr[0][1] < arr[3][1] - arr[2][1]:
                    view += "up"
                elif arr[2][1] - arr[0][1] > arr[3][1] - arr[2][1]:
                    view += "down"

                # 얼굴 위치 좌우 판별
                if arr[2][0] < 0.4:
                    loc = "left "
                elif arr[2][0] > 0.6:
                    loc = "right "
                else:
                    loc = "center "

                # 얼굴 위치 상하 판별
                if arr[2][1] < 0.4:
                    loc += "up"
                elif arr[2][1] > 0.6:
                    loc += "down"
                else:
                    loc += "center"
                cv2.putText(image, "      L/R U/D", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.putText(image, "view: " + view, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.putText(image, "loc : " + loc, (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow('MediaPipe Face Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
