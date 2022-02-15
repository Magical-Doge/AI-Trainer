import cv2
import numpy as np


class animation():

    def ractangleV(self, x, start1, stop1, start2, stop2, img):
        y = np.interp(x, [start1, stop1], [start2, stop2])

        cv2.rectangle(img, (20, 100), (60, 400), (255, 80, 80), 2)
        cv2.rectangle(img, (20, 400 - int(y)), (60, 400), (255, 80, 80), cv2.FILLED)

    def ractangleP(self, x, start1, stop1, start2, stop2, img):
        x = np.interp(x, [start1, stop1], [start2, stop2])

        cv2.rectangle(img, (320, 60), (960, 90), (255, 80, 80), 2)
        cv2.rectangle(img, (320, 60), (320 + int(x), 90), (255, 80, 80), cv2.FILLED)

