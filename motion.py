import numpy as np
import cv2
import time
from conductMode import *

class Motion:
    def __init__(self):
        self.actionCooldown = 1.0
        self.lastAction = time.time()
        self.conduct = conductMode("jazzConduct")
        self.lastFrame = None
    def getMotionMask(self, image, oldImage, threshold):
        difference = abs(oldImage.astype('int8') - image.astype('int8'))
        # return difference
        magnitudeDifference = np.linalg.norm(difference, axis=2)
        # changedMask = (magnitudeDifference * 255.0) / (np.max((magnitudeDifference)))
        changedMask = np.zeros_like(image)
        changedMask[magnitudeDifference > threshold] = 255.
        # cv2.imshow("motionImage", changedMask)
        return changedMask

    #top, bottom, left, right
    def getMotions(self, image, oldImage, thresholdChange, thresholdPercentage):
        changedMask = self.getMotionMask(image, oldImage, thresholdChange)
        width = image.shape[1]
        height = image.shape[0]
        size = width * height / 2
        thresholdSize = size * thresholdPercentage
        top = np.count_nonzero(changedMask[0:int(height/2)])
        bottom = np.count_nonzero(changedMask[int(height/2):])
        left = np.count_nonzero(changedMask[:,0:int(width/2)])
        right = np.count_nonzero(changedMask[:,int(width/2):])
        retVal = []
        bestMotion = None
        bestMotionScore = thresholdSize
        motionScores = (top, bottom, left, right)
        motionNames = ("up", "down", "right", "left")
        for val in range(len(motionScores)):
            motionScore = motionScores[val]
            if (motionScore > bestMotionScore):
                bestMotionScore = motionScore
                bestMotion = motionNames[val]
        return bestMotion

    def onFrame(self, frame):
        if (self.lastFrame is None):
            self.lastFrame = frame
            return frame
        width = 100
        motion = None
        currentlyPlaying, currentlyPlayingX, currentlyPlayingY = self.conduct.getCurrentNote()
        if currentlyPlaying != 'wait':
            oldFrameSegment = self.lastFrame[currentlyPlayingX:currentlyPlayingX+width,currentlyPlayingY:currentlyPlayingY+width].copy()
            self.lastFrame = frame
            frameSegment = frame[currentlyPlayingX:currentlyPlayingX+width,currentlyPlayingY:currentlyPlayingY+width].copy()
            if self.lastAction + self.actionCooldown < time.time():
                motion = self.getMotions(oldFrameSegment, frameSegment, 100, .6)
                if motion is not None:
                    print(motion)
                    self.lastAction = time.time()

        self.conduct.onFrame(frame, motion)
        return frame