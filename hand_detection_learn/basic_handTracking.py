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
            lmlist = []
            for id, lm in enumerate(hand_mark.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])


            if len(lmlist) != 0:
                print(lmlist[4])

                # draw circuls on tip
                x1, y1 = lmlist[4][1], lmlist[4][2]
                x2, y2 = lmlist[8][1], lmlist[8][2]

                #draw
                cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

            mp_draw.draw_landmarks(frame, hand_mark, mpHands.HAND_CONNECTIONS)

    frame = cv2.flip(frame, 1)
    cv2.imshow('Hand_Detector', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllwindows()

