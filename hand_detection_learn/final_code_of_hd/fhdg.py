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

# game var

legth = 1

rot_x = 1
rot_y = 1
stop = False
r_right = False
r_left = False
r_up = False
r_down = False
scaleUp = False
scaleDown = False

ref_x, ref_y = 0, 0
def rotation_hand_X(rot_x):
    if rot_x > 100:
        print('right')
        global r_right
        r_right = True
    elif rot_x < -100:
        print('left')
        global r_left
        r_left = True
    else:
        r_left = False
        r_right = False

def rotation_hand_Y(rot_y):
    # up-down

    if rot_y < 100:
        print('up')
        global r_up
        r_up = True

    elif rot_y < -100:
        print('down')
        global r_down
        r_down = True

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

                    #print(hand_side)

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
                    #rotation_hand_X(rot_x)

                    if sum(fingers) == 5:
                        global stop
                        stop = True
                        global ref_x, ref_y
                        ref_x, ref_y = lmlist[9][1], lmlist[9][2]
                    else:
                        stop = False




                    if sum(fingers) == 1 or sum(fingers) == 0:
                        print('fist')
                        tx, ty = lmlist[9][1], lmlist[9][2]
                        nx, ny = ref_x - tx, ref_y - ty
                        # reference point
                        print(f'{ref_y} - {ty} = {ny}')


                        rot_x = nx
                        rot_y = ny

                        if nx > 100:
                            global r_right
                            r_right = True
                            print('x')
                        elif nx < -100:
                            global r_left
                            r_left = True
                            print('-x')
                        elif ny > 70:
                            global r_up
                            r_up = True
                            print('y')
                        elif ny < -70:
                            global r_down
                            r_down = True
                            print('-y')
                        else:
                            r_left = False
                            r_right = False
                            r_down = False
                            r_up = False









                    # draw circuls on tip
                    x1, y1 = lmlist[4][1], lmlist[4][2]
                    x2, y2 = lmlist[8][1], lmlist[8][2]
                    cirx, ciry = lmlist[0][1], lmlist[0][2]

                    # draw

                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    # legth

                    global legth
                    legth = math.hypot(x2 - x1, y2 - y1)

                    if fingers[4] == 0 & sum(fingers) == 1 & both_hand:
                        print('scale activeted')


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
    #cube.rotation_y += int(legth) * time.dt * 10
    camera_mov()
    print('cube scale:' + str(cube.scale_x))

    # rotation by hand
    if not stop:
        if r_right:
            cube.rotation_y -= time.dt * 1 * np.abs(rot_x)
            print('done')
        elif r_left:
            cube.rotation_y += time.dt * 1 * np.abs(rot_x)
        elif r_up:
            cube.rotation_x -= time.dt * 1 * np.abs(rot_y)
        elif r_down:
            cube.rotation_x += time.dt * 1 * np.abs(rot_y)

    if int(legth) > 80:
        pass
        #cube.scale = cube.scale.x + 1
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


