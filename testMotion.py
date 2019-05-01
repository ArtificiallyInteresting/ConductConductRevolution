
import cv2
from util import *
import vision
from motion import *

def main():
    vc = startWebcamFeed()
    motionImage = cv2.namedWindow("motionImage")

    rval, oldFrame = vc.read()
    rval, frame = vc.read()
    width = 100
    while rval:
        oldFrameSegment = oldFrame[200:200+width,200:200+width].copy()
        frameSegment = frame[200:200+width,200:200+width].copy()

        magnitudes = getMotions(oldFrameSegment, frameSegment, 100)

        cv2.imshow("motionImage", magnitudes)
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