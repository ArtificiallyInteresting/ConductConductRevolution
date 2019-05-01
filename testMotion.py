
import cv2
from util import *
import vision
from motion import *
import time

def main():
    vc = startWebcamFeed()
    motionImage = cv2.namedWindow("motionImage")

    rval, oldFrame = vc.read()
    rval, frame = vc.read()
    width = 100
    lastAction = time.time()
    actionCooldown = 1.0
    while rval:
        oldFrameSegment = oldFrame[200:200+width,200:200+width].copy()
        frameSegment = frame[200:200+width,200:200+width].copy()

        if lastAction + actionCooldown < time.time():
            motion = getMotions(oldFrameSegment, frameSegment, 100, .6)
            if motion is not None:
                print(motion)
                lastAction = time.time()

        oldFrame = frame.copy()
        cv2.rectangle(frame, (200,200), (200+width,200+width),  (255,255,0))
        showFrame(frame)
        rval, frame = vc.read()
        key = cv2.waitKey(50)
        if key == 27:  # exit on ESC
            break
        if key == 32:  # space
            showImage(oldFrameSegment)
            showImage(frameSegment)
    endWebcamFeed()

if __name__ == '__main__':
    main()