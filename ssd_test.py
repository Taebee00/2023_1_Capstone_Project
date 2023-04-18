import jetson.inference
import jetson.utils
import cv2

# 객체 감지 모델 초기화
net = jetson.inference.detectNet('ssd-mobilenet-v2', threshold=0.5)

# 카메라 또는 비디오 스트림 열기
cap = cv2.VideoCapture(0)  # 카메라 사용

# 색상 추출을 위한 OpenCV 유틸리티 함수
def get_color(image):
    # 색상 범위 지정
    lower_red = (0, 0, 100)
    upper_red = (80, 80, 255)
    lower_yellow = (0, 80, 80)
    upper_yellow = (80, 255, 255)
    lower_green = (0, 100, 0)
    upper_green = (80, 255, 80)
    lower_blue = (100, 0, 0)
    upper_blue = (255, 80, 80)
    lower_purple = (80, 0, 80)
    upper_purple = (255, 80, 255)

    # 이미지를 HSV 색상 공간으로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 색상 범위 내의 모든 픽셀을 추출하여 마스크 생성
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)

    # 가장 많은 픽셀을 갖는 색상을 선택하여 반환
    max_pixels = max(cv2.countNonZero(mask) for mask in [mask_red, mask_yellow, mask_green, mask_blue, mask_purple])
    if max_pixels == 0:
        return "Unknown"
    elif cv2.countNonZero(mask_red) == max_pixels:
        return "Red"
    elif cv2.countNonZero(mask_yellow) == max_pixels:
        return "Yellow"
    elif cv2.countNonZero(mask_green) == max_pixels:
        return "Green"
    elif cv2.countNonZero(mask_blue) == max_pixels:
        return "Blue"
    elif cv2.countNonZero(mask_purple) == max_pixels:
        return "Purple"
