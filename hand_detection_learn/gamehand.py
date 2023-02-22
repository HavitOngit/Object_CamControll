import pyautogui
import math
import cv2
import mediapipe as mp
import numpy as np
from google.protobuf.json_format import MessageToDict
import threading

# mediapipe conf
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# mp drawing method
mp_draw = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)

tip_id = [4, 8, 12, 16, 20]

# game var

legth = 1

rot_x = 1
rot_y = 1

both_hand = False
r_right = False
r_left = False
r_up = False
r_down = False
hand_side = ''
ref_x, ref_y = 0, 0

nirto = False

pyautogui.alert('Start')


def rotation_hand_X(rot_x):
    if rot_x > 50:
        print('right')
        pyautogui.keyDown('d')
        global r_right
        r_right = True
    elif rot_x < -50:
        print('left')
        pyautogui.keyDown('a')
        global r_left
        r_left = True
    else:
        pyautogui.keyUp('a')
        pyautogui.keyUp('d')

def rotation_hand_Y(rot_y):
    # up-down

    if rot_y < 50:
        print('up')
        global r_up
        r_up = True

    elif rot_y < -50:
        print('down')
        global r_down
        r_down = True

def forward():
    while True:
        pyautogui.write(['w'])
def cam_fuc():
    while True:

        #pyautogui.write(['w'])
        success, frame = cam.read()

        # bgr->rgb for batter detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rgb_frame.flags.writeable = False
        result = hands.process(rgb_frame)
        rgb_frame.flags.writeable = True
        # draw landmarks if hand detected
        if result.multi_hand_landmarks:
            # landmarks
            for hand_mark in result.multi_hand_landmarks:
                lmlist = []
                for id, lm in enumerate(hand_mark.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmlist.append([id, cx, cy])

                if len(lmlist) != 0:
                    # print(lmlist[4])

                    # count fingers
                    fingers = []
                    # for thumb
                    if lmlist[4][1] > lmlist[3][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    # for fingers
                    for id in range(1, 5):
                        if lmlist[tip_id[id]][2] < lmlist[tip_id[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                    #print(fingers)

                    # rotation logic
                    wx, wy = lmlist[0][1], lmlist[0][2]
                    tx, ty = lmlist[12][1], lmlist[12][2]

                    global rot_x, rot_y
                    rot_x = wx - tx
                    rot_y = wy - ty
                    #print(rot_y)
                    rotation_hand_X(rot_x)


                    if sum(fingers) == 1:
                        pyautogui.write(['space'])

                    if sum(fingers) == 0:
                        pyautogui.write(['s'])


























                    # draw circuls on tip
                    x1, y1 = lmlist[4][1], lmlist[4][2]
                    x2, y2 = lmlist[8][1], lmlist[8][2]

                    # legth

                    global legth
                    legth = math.hypot(x2 - x1, y2 - y1)

                    if legth < 25:
                        cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                        cv2.circle(frame, (x2, y2), 15, (0, 255, 0), cv2.FILLED)

                    # convert lenght in 1 2 100 format
                    conLen = np.interp(legth, [15, 200], [0, 100])
                    ##print(f"{legth}...Converted to...{conLen}")

                mp_draw.draw_landmarks(frame, hand_mark, mpHands.HAND_CONNECTIONS)
        # draw reference line

        frame = cv2.flip(frame, 1)

        #cv2.imshow('Hand_Detector', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

t = threading.Thread(target=cam_fuc)
f = threading.Thread(target=forward)
t.start()
f.start()