# @describe: This is a module of realtime detection of pose. Learned from @murtaza's workshop.
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
#
# update 22.2.22 @Magical-Doge
#


import cv2
import mediapipe as mp
import time
import math


class PoseDetector():
    def __init__(self,
                 mode=False,
                 mc=1,
                 slm=True,
                 es=False,
                 ss=True,
                 detectionCon=0.5,
                 trackingCon=0.5):
        self.mode = mode
        self.mc = mc
        self.slm = slm
        self.es = es
        self.ss = ss
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,
                                     self.mc,
                                     self.slm,
                                     self.es,
                                     self.ss,
                                     self.detectionCon,
                                     self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img


    def findLandmark(self, img, draw=True):

        self.lmlist = []

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)

                self.lmlist.append([id, cx, cy])

                if draw:
                    if id == 14:
                        cv2.circle(img, (cx, cy), 10, (255, 255, 0), 2, cv2.FILLED)

        return self.lmlist


    def findAngle(self, img, p1, p2, p3, draw = True):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        x3, y3 = self.lmlist[p3][1:]

        # count angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2(y1-y2, x1-x2))
        if angle < 0:
            angle = angle*(-1)

        if draw:
            # draw points
            cv2.circle(img, (x1, y1), 10, (255, 255, 0), 2)
            cv2.circle(img, (x2, y2), 5, (255, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 255, 0), 2)
            cv2.circle(img, (x3, y3), 10, (255, 255, 0), 2)

            # write angle
            cv2.putText(img, f'Angle:{round(angle, 2)}', (x2+30,y2), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0),2)

        return angle
    
    
    def modeQuite(self):
    trigger = 0
    x1, y1 = self.lmlist[15][1:]
    x2, y2 = self.lmlist[16][1:]

    if x1 in range(x2-30, x2+30):
        if y1 in range(y2-60, y2+60):
            trigger = 1
    return trigger



def main():
    videoPath = r'video\paml2.mp4'

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(10, 500)

    # -----time
    pTime = 0
    cTime = 0

    detector = PoseDetector()

    while True:
        success, img = cap.read()

        img = detector.findPose(img, True)
        img = detector.findLandmark(img,True)


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, 'fps:' + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow('webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()
