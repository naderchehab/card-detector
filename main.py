import sys
import cv2
import numpy as np
import os.path as path
import templateMatching
import screen

matchingThreshold = 0.90
areaToScanTopLeft = (213L, 111L)
areaToScanBottomRight = (1335L, 740L)

# image = screen.capture();

# for testing
image = cv2.imread(path.join('tests', 'test5.png'))

image = screen.imageToBw(image)

areaToScan = image[areaToScanTopLeft[1]:areaToScanBottomRight[1], areaToScanTopLeft[0]:areaToScanBottomRight[0]]

# screen.showImage(areaToScan)

# things we're looking for
suits = ['heart', 'spade', 'diamond', 'club']
values = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen','king', 'ace']

# for testing
# suits = ['spade']
# values = ['nine']

def getImage(name):
    filename = name + '.png';
    image = cv2.imread(path.join('images', filename))
    image = screen.imageToBw(image)
    return image

suitsDict = {}
for suit in suits:
    suitsDict[suit] = getImage(suit)

valuesDict = {}
for value in values:
    valuesDict[value] = getImage(value)
        
allMatches = []
matchesNames = set()

for suit in suitsDict:
    for value in valuesDict:
        template = np.concatenate([valuesDict[value], suitsDict[suit]])
        # screen.showImage(template)
        upsideDownTemplate = np.rot90(template, 2)
        matches = templateMatching.getMatches(areaToScan, template, matchingThreshold)
        cardName = value + ' ' + suit;
        numMatches = len(matches)
        if numMatches > 0:
            matchesNames.add(cardName + ' ' + str(numMatches));
        matchesUpsideDown = templateMatching.getMatches(areaToScan, upsideDownTemplate, matchingThreshold)
        numMatches = len(matchesUpsideDown)
        if numMatches > 0:
            matchesNames.add(cardName + ' ' + str(numMatches));
        allMatches = allMatches + matches + matchesUpsideDown
        
if len(allMatches) != 0:
    image = templateMatching.highlightRois(areaToScan, allMatches, template.shape[::-1])
    screen.showImage(image)
    screen.showCards(matchesNames, valuesDict, suitsDict)