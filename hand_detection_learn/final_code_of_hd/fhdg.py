import math
import cv2
import mediapipe as mp
import numpy as np
from google.protobuf.json_format import MessageToDict
from ursina import *
import random
import threading

# mediapipe conf
mpHands = mp.solutions.hands
hands = mpHands.Hands()
# mp drawing method
mp_draw = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)

tip_id = [4, 8, 12, 16, 20]

legth = 1
def cam_fuc():
    while True:
        success, frame = cam.read()

        # bgr->rgb for batter detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        rgb_frame.flags.writeable = False
        result = hands.process(rgb_frame)
        rgb_frame.flags.writeable = True

        # draw landmarks if hand detected
        if result.multi_hand_landmarks:

            # r vs l
            if len(result.multi_handedness) == 2:
                both_hand = True
            else:
                both_hand = False

                for i in result.multi_handedness:
                    hand_side = MessageToDict(i)['classification'][0]['label']

                    if hand_side == 'Left':
                        hand_side = 'Right'
                    elif hand_side == 'Right':
                        hand_side = 'Left'

                    print(hand_side)

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

                    print(fingers)

                    # draw circuls on tip
                    x1, y1 = lmlist[4][1], lmlist[4][2]
                    x2, y2 = lmlist[8][1], lmlist[8][2]
                    cirx, ciry = lmlist[0][1], lmlist[0][2]

                    # draw

                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    # legth

                    global legth
                    legth = math.hypot(x2 - x1, y2 - y1)

                    if legth < 25:
                        cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                        cv2.circle(frame, (x2, y2), 15, (0, 255, 0), cv2.FILLED)

                    # convert lenght in 1 2 100 format
                    conLen = np.interp(legth, [15, 200], [0, 100])
                    print(f"{legth}...Converted to...{conLen}")

                mp_draw.draw_landmarks(frame, hand_mark, mpHands.HAND_CONNECTIONS)
        # draw reference line

        frame = cv2.flip(frame, 1)

        cv2.imshow('Hand_Detector', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

t = threading.Thread(target=cam_fuc)
t.start()
# game code
def camera_mov():
    if held_keys['q']:
        camera.position += (0, time.dt, 0)
    if held_keys['w']:
        camera.position -= (0, time.dt, 0)


random_ganaretor = random.Random()
print(str(random_ganaretor), random_ganaretor.random())
app = Ursina()

window.title = "Havit Game"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enable = True


def update():
    cube.rotation_y += int(legth) * time.dt * 10
    camera_mov()

    if int(legth) > 80:
        cube.scale = cube.scale.x + 1
    if held_keys['z']:
        cube.rotation_z += time.dt * 50
    if held_keys['x']:
        cube.rotation_x += time.dt * 50

    if held_keys['t']:
        red = random_ganaretor.random() * 255
        blue = random_ganaretor.random() * 255
        green = random_ganaretor.random() * 255
        cube.color = color.rgb(red, green, blue)


def input(key):
    if key == 'space':
        red = random_ganaretor.random() * 255
        blue = random_ganaretor.random() * 255
        green = random_ganaretor.random() * 255
        cube.color = color.rgb(red, green, blue)
    if held_keys['a']:
        cube.scale = cube.scale.x + 1
        print(cube.scale.x)



cube = Entity(model='cube', color=color.orange, scale=(2, 2, 2), texture='cube_texture')

app.run()
#######


