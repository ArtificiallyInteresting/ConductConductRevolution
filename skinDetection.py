import cv2
import numpy as np

def applySkinMask(image):
    #Remember, this is BGR
    skin_start = (60,60,70)
    skind_end = (225,190,210)
    mask = cv2.inRange(image, skin_start, skind_end)
    # newImage = np.zeros_like(image)
    # newImage[mask] = image[mask]
    result = cv2.bitwise_and(image, image, mask=mask)

    return result