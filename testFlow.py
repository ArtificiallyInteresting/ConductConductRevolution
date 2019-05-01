
import cv2
from util import *
import vision
import audio
from flow import *
from danceMode import *


def main(trackName = None):
    vc = startWebcamFeed()
    flowImage = cv2.namedWindow("flow")

    rval, oldFrame = vc.read()
    rval, frame = vc.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255.
    oldFrame = cv2.cvtColor(oldFrame, cv2.COLOR_BGR2GRAY) / 255.
    width = 100
    while rval:
        oldFrameSegment = oldFrame[200:200+width,200:200+width]
        frameSegment = frame[200:200+width,200:200+width]
        # u,v = optic_flow_lk(oldFrameSegment, frameSegment, 15, "uniform", 5)
        interpolation = cv2.INTER_CUBIC
        border_mode = cv2.BORDER_REFLECT101
        levels = 10
        ksize = 75
        sigma = 25
        u,v = hierarchical_lk(oldFrameSegment, frameSegment, levels, ksize, "uniform", sigma, interpolation, border_mode)

        threshold = 100
        ucopy = np.copy(u)
        ucopy[ucopy < 0] = 0
        print("Positive U: " + str(np.count_nonzero((ucopy))))
        ucopy = np.copy(u)
        ucopy[ucopy > 0] = 0
        print("Negative U: " + str(np.count_nonzero((ucopy))))
        np.count_nonzero(ucopy)
        # v[(v < threshold) & (v > -threshold)] = 0
        # print("U: " + str(np.mean(u)))
        # print("V: " + str(np.mean(v)))
        vision.drawUandV(frame, u, v)
        cv2.imshow("flow", vision.quiver(u, v, .1, 10))
        cv2.rectangle(frame, (200,200), (200+width,200+width),  (255,255,0))
        showFrame(frame)
        oldFrame = frame
        rval, frame = vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255.
        key = cv2.waitKey(50)
        if key == 27:  # exit on ESC
            break
    endWebcamFeed()

if __name__ == '__main__':
    # main()
    main("jazz")
    # main("track1")