import math
import cv2
from costom_fun import angle_between_lines
import mediapipe as mp
import numpy as np

# mediapipe conf
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# mp drawing method
mp_draw = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)

while True:
    success, frame = cam.read()
    frame = cv2.flip(frame, 1)
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
                cirx, ciry = lmlist[0][1], lmlist[0][2]
                #draw
                #cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                #cv2.circle(frame, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # circle
                #r = math.hypot(x2 - cirx, y2 - ciry)
                #cv2.circle(frame, (cirx, ciry), int(30), (215, 15, 45), 5)

                # legth
                legth = math.hypot(x2 - x1, y2 - y1)
                #print(angle_between_lines(x1, y1, x2, y2, 0, 200, 200, 200))
                # print(legth)

                #cx, cy = (x1 + x2) // 2,  (y1 + y2) // 2

                if legth < 25:
                    cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(frame, (x2, y2), 15, (0, 255, 0), cv2.FILLED)

                # convert lenght in 1 2 100 format
                conLen = np.interp(legth, [15, 200], [0, 100])
                print(f"{legth}...Converted to...{conLen}")

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, str((x2, y1)), (x2, y2), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

            mp_draw.draw_landmarks(frame, hand_mark, mpHands.HAND_CONNECTIONS)
    # draw reference line


    cv2.imshow('Hand_Detector', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()


