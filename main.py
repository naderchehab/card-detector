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
# values = ['queen']

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
    suitTemplate = suitsDict[suit]
    suitMatches = templateMatching.getMatches(areaToScan, suitTemplate, matchingThreshold)
    suitMatches = map(lambda match: {'topLeft': match, 'name': suit}, suitMatches)
    
    # We found a suit, now find the associated value above it
    allValueMatches = []
    for suitMatch in suitMatches:
        suitMatchTopLeft = suitMatch['topLeft']
        for value in valuesDict:
            valueTemplate = valuesDict[value]
            topLeft = (suitMatchTopLeft[0] - 5L, suitMatchTopLeft[1] - 50L)
            bottomRight = (suitMatchTopLeft[0] + 50L, suitMatchTopLeft[1] + 5L)
            searchArea = areaToScan[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]]
            valueMatches = templateMatching.getMatches(searchArea, valueTemplate, matchingThreshold)
            valueMatches = map(lambda match: {'topLeft': (topLeft[0] + match[0], topLeft[1] + match[1]), 'name': value}, valueMatches)
            if (len(valueMatches) > 0):
                matchesNames.add(value + ' ' + suit)
            allValueMatches = allValueMatches + valueMatches

    upsideDownSuitTemplate = np.rot90(suitTemplate, 2)
    matchesUpsideDown = templateMatching.getMatches(areaToScan, upsideDownSuitTemplate, matchingThreshold)
    matchesUpsideDown = map(lambda match: {'topLeft': match, 'name': suit}, matchesUpsideDown)
    
    # todo: We found a suit upside down, now find the associated value below it
    
    allMatches = allMatches + suitMatches + allValueMatches + matchesUpsideDown

if len(allMatches) != 0:
    image = templateMatching.highlightRois(areaToScan, allMatches, (30L, 30L))
    screen.showImage(image)
    screen.showCards(matchesNames, valuesDict, suitsDict)