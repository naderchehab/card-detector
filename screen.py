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
    cv2.imshow('result', image)
    cv2.waitKey(0)

def showCards(cardNames, valuesDict, suitsDict):
    played = np.full((100L, 1800L), 255L, dtype = 'uint8')
    index = 0
    for cardName in cardNames:
        split = cardName.split(' ')
        value = split[0]
        suit = split[1]
        valueImg = valuesDict[value]
        suitImg = suitsDict[suit]
        cardImg = np.concatenate([valueImg, suitImg])
        topLeft = (0L, index)
        bottomRight = (cardImg.shape[0], index + cardImg.shape[1])
        played[topLeft[0]:bottomRight[0], topLeft[1]:bottomRight[1]] = cardImg
        index = index + cardImg.shape[1];
    showImage(played)
