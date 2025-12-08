import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode as dmdecode


class CodeReader:
    def __init__(self, index:int = 0):
        self.index = index
        self.camera = cv2.VideoCapture(index)

    def decode(self):
        image = self.camera.read()[1]
        output = dmdecode(image)
        return output

    