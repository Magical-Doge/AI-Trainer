# @describe: This is a project of AI trainer. Learned from @murtaza's workshop.
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
import time
import numpy as np
import AnimationModule as AM
import MusicPlayerModule as MPM
import HandTrackingModule as HTM
import PoseEstimationModule as PEM


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

cTime = 0
pTime = 0

animation = AM.animation()
mplayer = MPM.musicPlayer()
handDetector = HTM.handDetector(detectionCon=0.7)
poseDetector = PEM.PoseDetector(detectionCon=0.65)


fingerTop = [8, 12, 16, 20]
cnt1, cnt2, cnt3 = 0, 0, 0

dir = 0
count = 0


while True:
    success, img = cap.read()


    handDetector.findHands(img)
    lmList = handDetector.findLandmark(img)

    if len(lmList) != 0:
        fingers = []
        # Thumb
        if lmList[4][1] < lmList[5][1]:
            fingers.append(0)
        else:
            fingers.append(1)

        for id in fingerTop:
            if lmList[id][2] < lmList[id-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        print(fingers)

        if fingers == [0, 1, 0, 0, 0]:
            cnt1 = cnt1+1
            print(cnt1)
            animation.ractangleP(cnt1, 0, 30, 0, 640, img)
            if cnt1 == 30:
                cnt1 = 0
                while True:
                    success, img = cap.read()

                    poseDetector.findPose(img)
                    lmList = poseDetector.findLandmark(img)
                    angle = poseDetector.findAngle(img, 11, 13, 15)

                    per = np.interp(angle, (90, 180), (0, 100))
                    if per == 100:
                        if dir == 0:
                            count += 0.5
                            dir = 1
                    if per == 0:
                        if dir == 1:
                            count += 0.5
                            dir = 0
                    cv2.putText(img, f'num:{int(count)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime
                    cv2.putText(img, f'FPS:{int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                    cv2.putText(img, f'Weightlifting Mode Activated', (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2)

                    cv2.imshow('Webcam', img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        elif fingers == [0, 1, 1, 0, 0]:
            cnt2 = cnt2+1
            print(cnt2)
            animation.ractangleP(cnt2, 0, 30, 0, 640, img)
            if cnt2 == 30:
                cnt2 = 0
                while True:
                    success, img = cap.read()

                    poseDetector.findPose(img)
                    lmList = poseDetector.findLandmark(img)
                    angle = poseDetector.findAngle(img, 12, 14, 16)

                    per = np.interp(angle, (45, 180), (0, 100))
                    if per == 100:
                        if dir == 0:
                            count += 0.5
                            dir = 1
                    if per == 0:
                        if dir == 1:
                            count += 0.5
                            dir = 0
                    cv2.putText(img, f'num:{int(count)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime
                    cv2.putText(img, f'FPS:{int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                    cv2.putText(img, f'Standard push-ups Mode Activated', (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 2)

                    cv2.imshow('Webcam', img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        elif fingers == [1, 0, 0, 0, 0]:
            cnt3 = cnt3+1
            animation.ractangleP(cnt3, 0, 30, 0, 640, img)
            if cnt3 == 30:
                cnt3 = 0
                while True:
                    success, img = cap.read()

                    handDetector.findHands(img)
                    mlmList = handDetector.findLandmark(img)

                    if len(mlmList) != 0:
                        mfingers = []
                        # Thumb
                        if mlmList[4][1] < mlmList[5][1]:
                            mfingers.append(0)
                        else:
                            mfingers.append(1)

                        for id in fingerTop:
                            if mlmList[id][2] < mlmList[id - 2][2]:
                                mfingers.append(1)
                            else:
                                mfingers.append(0)

                        if mfingers == [0,1,0,0,0]:
                            cnt1 = cnt1+1
                            animation.ractangleV(cnt1, 0, 30, 0, 300, img)
                            if cnt1 == 30:
                                cnt1 = 0
                                mplayer.music_play()
                                break
                        if mfingers == [0,1,1,0,0]:
                            cnt2 = cnt2+1
                            animation.ractangleV(cnt2, 0, 30, 0, 300, img)
                            if cnt2 == 30:
                                cnt2 = 0
                                mplayer.skip_music()
                                break
                        if mfingers == [0,1,1,1,0]:
                            cnt3 = cnt3+1
                            animation.ractangleV(cnt3, 0, 30, 0, 300, img)
                            if cnt3 == 30:
                                cnt3 = 0
                                mplayer.stop_music()
                                break




                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime
                    cv2.putText(img, f'FPS:{int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

                    cv2.putText(img, f'Music player Mode', (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 255), 2)

                    cv2.imshow('Webcam', img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break






    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

    cv2.putText(img, f'Please select a mode, 1 is Weightlifting', (200, 200), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.putText(img, f'                      2 is Standard push ups', (220, 230), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break





###################################################################################################
#------------------------------    Rectify Log    ------------------------------------------------#
###################################################################################################
# v0  ---   construct a frame of mode switch method
#     ---   rectify camera's fps to 60hz, size to 1280x720, solved webcam's view dark problem
#
# v1  ---   add music player function, allow using hand pose to play\stop\pause music.
#
#
# v2  ---   add animation, makes interface more acceptable.
#


