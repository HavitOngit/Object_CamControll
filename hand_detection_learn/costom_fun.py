import math
import cv2
import numpy as np
def angle_between_lines(x1, y1, x2, y2, x3, y3, x4, y4):
    # Calculate slopes of the lines

    try:

        m1 = (y2 - y1) / (x2 - x1)
        m2 = (y4 - y3) / (x4 - x3)
        # Convert slopes to degrees
        angle1 = math.atan(m1) * 360 / math.pi
        angle2 = math.atan(m2) * 360 / math.pi
        # Calculate angle between lines
        angle = abs(angle1 - angle2)
    except ZeroDivisionError:
        pass
    return angle

