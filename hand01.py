import mediapipe as mp
import cv2
import numpy as np


mp_drawings = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# cam
cam = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:

    while True:
        ret, frame = cam.read()

        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # set flag
        image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # set flag true
        image.flags.writeable = True

        # RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # rendering Results
        print(results)
        
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawings.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

        image = cv2.flip(image, 1)
        cv2.imshow('Track my hand', image)

        if cv2.waitKey(1) == ord('q'):
            break

cam.release()    
cv2.destroyAllwindows()