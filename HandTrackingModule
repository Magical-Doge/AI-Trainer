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


class handDetector():
    def __init__(self, mode=False,
                 maxHands=2,
                 modelComplexity=1,
                 detectionCon=0.5,
                 trackingCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon,
                                        self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):

        # -----mediapipe(object 'hands' using RGB picture)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # -----mediapipe(input picture to frame, and output landmark of hand)
        self.results = self.hands.process(imgRGB)

        # -----mediapipe(test what thing in the output:  <class 'mediapipe.python.solution_base.SolutionOutputs'> or none)
        # print(results)
        # -----mediapipe(test what thing in the output:  get each hands' landmarks(x,y,z))
        # print(results.multi_hand_landmarks)

        # -----mediapipe(draw line)
        if draw:
            if self.results.multi_hand_landmarks:
                # -----mediapipe( 'results.multi_hand_landmarks' get each hand's landmark,
                #                  so we need for..in.. to draw every hands landmark one by one)
                for handLms in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img


    def findLandmark(self, img, hand=0, draw=True):

        lmlist=[]

        if self.results.multi_hand_landmarks:
            # for handlm in self.results.multi_hand_landmark
            myhand = self.results.multi_hand_landmarks[hand]
            # -----mediapipe( 'handLms.landmark' get each point's landmark, such as 'id x y z'
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                # -----mediapipe(draw particular point)
                if draw:
                    if id == 4:
                        cv2.circle(img, (cx, cy), 8, (255, 255, 0), cv2.FILLED)
                    if id == 8:
                        cv2.circle(img, (cx, cy), 8, (255, 255, 0), cv2.FILLED)

        return lmlist



# A template for reference
def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(10, 5000)

    # -----time
    pTime = 0
    cTime = 0

    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img, True)

        # -----display fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, 'fps:' + str(int(fps)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)

        cv2.imshow('webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()
