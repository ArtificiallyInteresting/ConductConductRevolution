import cv2
import numpy as np
from util import *

def drawCircles(image, circles, color=(255,255,255)):
    for circle in circles:
        cv2.circle(image, (circle[0], circle[1]), circle[2], color, 1)

def drawDirection(frame, x, y, direction, textColor, secondCircleRadius=40):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.circle(frame, (x, y), 40, textColor, 1)
    cv2.circle(frame, (x, y), secondCircleRadius, textColor, 1)
    cv2.putText(frame, direction, (x - 15, y + 15), font, 1.5, textColor, 2, cv2.LINE_AA)

