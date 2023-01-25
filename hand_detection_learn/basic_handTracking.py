import cv2
import mediapipe as mp
import time

# mediapipe conf
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# mp drawing method
mp_draw = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)

while True:
    success, frame = cam.read()

    # bgr->rgb for batter detection
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # draw landmarks if hand detected
    if result.multi_hand_landmarks:
        for hand_mark in result.multi_hand_landmarks:\
            mp_draw.draw_landmarks(frame, hand_mark)

    cv2.imshow('Hand_Detector', frame)

    cv2.waitKey(1)



