import numpy as np

def getMotions(image, oldImage, threshold):
    difference = abs(oldImage.astype('int8') - image.astype('int8'))
    # return difference
    magnitudeDifference = np.linalg.norm(difference, axis=2)
    # changedMask = (magnitudeDifference * 255.0) / (np.max((magnitudeDifference)))
    changedMask = np.zeros_like(image)
    changedMask[magnitudeDifference > threshold] = 255.
    return changedMask