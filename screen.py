import numpy as np
from PIL import ImageGrab
import cv2

def imageToBw(image):
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # (thresh, imageBw) = cv2.threshold(imageGray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return imageGray

def capture():
    screen = ImageGrab.grab()
    imageNumpy = np.array(screen)
    return imageNumpy

def showImage(image):
    cv2.imshow("result", image)
    cv2.waitKey(0)
