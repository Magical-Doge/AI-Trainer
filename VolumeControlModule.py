# @describe: This is a module of realtime detection of hand. Learned from @murtaza's workshop.
#
# @Author: Magical-Doge
#
# @Personal URL: Https://github.com/Magical-Doge, if you like plz pity me for a ★star!!
#
# @Environments require:
#
# Package               Version
# --------------------- ---------
# python                3.7.x
# opencv-contrib-python 4.5.5.62
# mediapipe             0.8.9.1
# numpy                 1.21.5
#
#
# !! ATTENTION !! this code for learning and communication, follow MIT open source protocol


import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
import numpy as np

# -----copyfrom github, author: @AndreMiras link: https://github.com/AndreMiras/pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeControl():
    def __init__(self):
        self.detector = htm.handDetector(detectionCon=0.7)

        # -----copyfrom github, author: AndreMiras link: https://github.com/AndreMiras/pycaw
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        # volume.GetMute()
        # volume.GetMasterVolumeLevel()
        volRange = self.volume.GetVolumeRange()
        self.minVolume = volRange[0]
        self.maxVolume = volRange[1]

        self.vol = 0
        self.volBox = 0
        self.lmList = []
        self.lcx, self.lcy = 0, 0
        self.fingerTop = [8, 12, 16, 20]
        self.fingerTopReflect = [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 1, 0, 0], [0, 1, 1, 1, 0]]

        self.cnt =0

    def abs(self, x):
        if x >= 210:
            x = 210
        if x <= 50:
            x = 50
        return x

    def drawCnL(self, img):
        trg = 0
        img = self.detector.findHands(img, True)
        self.lmList = self.detector.findLandmark(img, 0, False)
        if len(self.lmList) != 0:

            # -----quite the loop
            fingers = []

            if self.lmList[4][1] < self.lmList[5][1]:
                fingers.append(0)
            else:
                fingers.append(1)

            for id in self.fingerTop:
                if self.lmList[id][2] < self.lmList[id-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            if fingers[4] == 1:
                self.cnt = self.cnt+1
                if self.cnt == 20:
                    self.cnt = 0
                    trg = 1



            # -----count center of line between fingers
            self.lcx, self.lcy = (self.lmList[4][1] + self.lmList[8][1]) // 2, (
                        self.lmList[4][2] + self.lmList[8][2]) // 2

            # -----draw(finger
            cv2.circle(img, (self.lmList[4][1], self.lmList[4][2]), 6, (255, 255, 0), 2)
            cv2.circle(img, (self.lmList[8][1], self.lmList[8][2]), 6, (255, 255, 0), 2)
            # -----draw(line between finger
            cv2.line(img, (self.lmList[4][1], self.lmList[4][2]), (self.lmList[8][1], self.lmList[8][2]), (255, 255, 0),
                     2)
            # -----draw(center of line
            cv2.circle(img, (self.lcx, self.lcy), 4, (100, 255, 100), 2)
            # -----count length of line between fingers
            length = int(math.hypot(self.lmList[8][1] - self.lmList[4][1], self.lmList[8][2] - self.lmList[4][2]))

            # -----limit length of line
            length = self.abs(length)

            # -----length of line 50 - 120
            # -----volume range  -65 - 0
            # -----cvt line to volume
            vol = np.interp(length, [50, 210], [self.minVolume, self.maxVolume])
            # -----control volume
            self.volume.SetMasterVolumeLevel(vol, None)

            # ------cvt line to volume box
            volBox = np.interp(length, [50, 210], [400, 100])
            # -----draw(volume box and filled
            cv2.rectangle(img, (20, 100), (60, 400), (80, 80, 255), 2)
            cv2.rectangle(img, (20, int(volBox)), (60, 400), (80, 80, 255), cv2.FILLED)

            # -----decorates
            if length == 50:
                cv2.circle(img, (self.lcx, self.lcy), 4, (80, 80, 80), 4)
            if length == 210:
                cv2.circle(img, (self.lcx, self.lcy), 4, (80, 80, 255), 4)

        return img, trg




def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)

    pTime = 0
    cTime = 0

    controler = VolumeControl()

    while True:
        success, img = cap.read()

        img, trg = controler.drawCnL(img)


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.imshow('Webcam', img)

        if cv2.waitKey(1) & trg:
            break


if __name__ == "__main__":
    main()
