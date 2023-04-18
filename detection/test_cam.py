import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()

    cv2.imshow('Test', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
