
import cv2
from util import *
import vision
from motion import *
import time
from conductMode import *

def main():
    vc = startWebcamFeed()
    # motionImage = cv2.namedWindow("motionImage")
    key = -1
    while (key == -1):
        key = cv2.waitKey(20)
        print(key)
        rval, frame = vc.read()
        frame = np.flip(frame, 1)
        showFrame(frame)
    motionController = Motion()
    rval, frame = vc.read()
    motionController.onFrame(frame)
    rval, frame = vc.read()
    frame = np.flip(frame, 1)
    frame = frame.copy()
    while rval:
        # cv2.rectangle(frame, (200,200), (200+width,200+width),  (255,255,0))
        frame = motionController.onFrame(frame)
        showFrame(frame)
        rval, frame = vc.read()
        frame = np.flip(frame, 1)
        frame = frame.copy()
        key = cv2.waitKey(50)
        if key == 27:  # exit on ESC
            while True:
                key = cv2.waitKey(20)
                print(key)
                rval, frame = vc.read()
                frame = np.flip(frame, 1)
                showFrame(frame)
    endWebcamFeed()

if __name__ == '__main__':
    main()