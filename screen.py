import numpy as np
from PIL import ImageGrab
import cv2

def imageToBw(image):
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return imageGray

def capture():
    screen = ImageGrab.grab()
    imageNumpy = np.array(screen)
    return imageNumpy

def showImage(image):
    cv2.imshow('result', image)
    cv2.waitKey(1) # for testing use 0

def showCards(cardNames, valuesDict, suitsDict):
    played = np.full((100L, 1800L), 255L, dtype = 'uint8')
    index = 0
    for cardName in cardNames:
        split = cardName.split(' ')
        value = split[0]
        suit = split[1]
        valueImg = valuesDict[value]
        suitImg = suitsDict[suit]
        
        # value
        topLeft = (index, 0L)
        bottomRight = (index + valueImg.shape[1], valueImg.shape[0])
        played[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]] = valueImg
        
        # suit
        topLeft = (topLeft[0], bottomRight[1])
        bottomRight = (topLeft[0] + suitImg.shape[1], topLeft[1] + suitImg.shape[0])
        played[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]] = suitImg
        
        index = index + valueImg.shape[1];
    showImage(played)
