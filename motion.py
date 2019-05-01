import numpy as np
import cv2

def getMotionMask(image, oldImage, threshold):
    difference = abs(oldImage.astype('int8') - image.astype('int8'))
    # return difference
    magnitudeDifference = np.linalg.norm(difference, axis=2)
    # changedMask = (magnitudeDifference * 255.0) / (np.max((magnitudeDifference)))
    changedMask = np.zeros_like(image)
    changedMask[magnitudeDifference > threshold] = 255.
    cv2.imshow("motionImage", changedMask)
    return changedMask

#top, bottom, left, right
def getMotions(image, oldImage, thresholdChange, thresholdPercentage):
    changedMask = getMotionMask(image, oldImage, thresholdChange)
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
    motionNames = ("top", "bottom", "left", "right")
    for val in range(len(motionScores)):
        motionScore = motionScores[val]
        if (motionScore > bestMotionScore):
            bestMotionScore = motionScore
            bestMotion = motionNames[val]
    return bestMotion

