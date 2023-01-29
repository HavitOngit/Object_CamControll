import cv2
import mediapipe as mp

class handDetetor():
    def __int__(self, maxHand=2, detectCon=0.5, trackCon=0.5):
        self.maxHand = maxHand
        self.detectCon = detectCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(False, self.mpHands, )