
import cv2
from util import *
import vision
from skinDetection import *


def main():
    vc = startWebcamFeed()
    testDisplay = cv2.namedWindow("testDisplay")

    rval, frame = vc.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255.
    # oldFrame = cv2.cvtColor(oldFrame, cv2.COLOR_BGR2GRAY) / 255.
    width = 100
    while rval:
        frameSegment = frame[200:200+width,200:200+width]
        skinMasked = applySkinMask(frameSegment)
        cv2.imshow("testDisplay", skinMasked)
        cv2.rectangle(frame, (200,200), (200+width,200+width),  (255,255,0))
        showFrame(frame)
        rval, frame = vc.read()
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255.
        key = cv2.waitKey(50)
        if key == 27:  # exit on ESC
            break
    endWebcamFeed()

if __name__ == '__main__':
    main()