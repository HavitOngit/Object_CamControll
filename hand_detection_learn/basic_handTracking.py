import cv2
import mediapipe as mp

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

    rgb_frame.flags.writeable = False
    result = hands.process(rgb_frame)
    rgb_frame.flags.writeable = True

    # draw landmarks if hand detected
    if result.multi_hand_landmarks:
        for hand_mark in result.multi_hand_landmarks:
            for id, lm in enumerate(hand_mark.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)

            mp_draw.draw_landmarks(frame, hand_mark, mpHands.HAND_CONNECTIONS)

    frame = cv2.flip(frame, 1)
    cv2.imshow('Hand_Detector', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllwindows()

