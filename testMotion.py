
import cv2
from util import *
import vision
from motion import *
import time
from conductMode import *

def main():
    vc = startWebcamFeed()
    # motionImage = cv2.namedWindow("motionImage")
    motionController = Motion()
    rval, frame = vc.read()
    motionController.onFrame(frame)
    rval, frame = vc.read()
    while rval:
        # cv2.rectangle(frame, (200,200), (200+width,200+width),  (255,255,0))
        frame = motionController.onFrame(frame)
        showFrame(frame)
        rval, frame = vc.read()
        key = cv2.waitKey(50)
        if key == 27:  # exit on ESC
            break
    endWebcamFeed()

if __name__ == '__main__':
    main()