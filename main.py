import sys
import cv2
import numpy as np
import os.path as path
import templateMatching
import screen
from functools import cmp_to_key

# in test mode, use a test image as input, otherwise use live screen capture
testMode = False
testImage = 'test9.png'

# how good does the match have to be? value between 0 and 1.
# 1 means it has to be a perfect match
matchingThreshold = 0.88

# it's faster to scan a smaller area rather than the whole screen
areaToScanTopLeft = (200L, 80L)
areaToScanBottomRight = (1380L, 800L)

# things we're looking for
suits = ['spade', 'heart', 'club', 'diamond']
values = ['ace', 'king', 'queen', 'jack', 'ten', 'nine', 'eight', 'seven', 'six', 'five', 'four', 'three', 'two']

# for testing specific cards
# suits = ['club']
# values = ['queen']

allCards = {v + ' ' + s for s in suits for v in values}

# cards found so far
cardsFound = set()

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
    
# used for sorting a hand of cards
def getCardPosition(cardName):
    cardNameArr = cardName.split(' ')
    value = cardNameArr[0]
    suit = cardNameArr[1]
    valueIndex = values.index(value)
    suitIndex = suits.index(suit)
    return suitIndex * 13 + valueIndex

# used for sorting a hand of cards
def cardComparer(a, b):
    return getCardPosition(a) - getCardPosition(b)

# This is the main function that is executed continuously to watch for new cards and display them
def watchAndDisplayCards():
    if testMode:
        image = cv2.imread(path.join('tests', testImage))
    else:
        image = screen.capture();

    image = screen.imageToBw(image)

    areaToScan = image[areaToScanTopLeft[1]:areaToScanBottomRight[1], areaToScanTopLeft[0]:areaToScanBottomRight[0]]

    # for testing
    # screen.showImage(areaToScan)
            
    allMatches = []

    for suit in suitsDict:
        suitTemplate = suitsDict[suit]
        suitMatches = templateMatching.getMatches(areaToScan, suitTemplate, matchingThreshold)
        suitMatches = map(lambda match: {'topLeft': match, 'name': suit}, suitMatches)
        
        # We found a suit, now find the associated value above it (if any)
        allValueMatches = []
        for suitMatch in suitMatches:
            suitMatchTopLeft = suitMatch['topLeft']
            topLeft = (suitMatchTopLeft[0] - 5L, suitMatchTopLeft[1] - 50L)
            bottomRight = (suitMatchTopLeft[0] + 40L, suitMatchTopLeft[1] + 5L)
            searchArea = areaToScan[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]]
            # screen.showImage(searchArea)
            for value in valuesDict:
                valueTemplate = valuesDict[value]
                valueMatches = templateMatching.getMatches(searchArea, valueTemplate, matchingThreshold)
                valueMatches = map(lambda match: {'topLeft': (topLeft[0] + match[0], topLeft[1] + match[1]), 'name': value}, valueMatches)
                if (len(valueMatches) > 0):
                    cardsFound.add(value + ' ' + suit)
                allValueMatches = allValueMatches + valueMatches

        # also find upside down suits and values
        upsideDownSuitTemplate = np.rot90(suitTemplate, 2)
        suitMatchesUpsideDown = templateMatching.getMatches(areaToScan, upsideDownSuitTemplate, matchingThreshold)
        suitMatchesUpsideDown = map(lambda match: {'topLeft': match, 'name': suit}, suitMatchesUpsideDown)
        
        # We found a suit upside down, now find the associated value below it (if any)
        # TODO: refactor this, reuse code above
        allUpsidedownValueMatches = []
        for suitMatch in suitMatchesUpsideDown:
            suitMatchTopLeft = suitMatch['topLeft']
            topLeft = (suitMatchTopLeft[0] - 10L, suitMatchTopLeft[1] + 25L)
            bottomRight = (suitMatchTopLeft[0] + 50L, suitMatchTopLeft[1] + 70L)
            searchArea = areaToScan[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]]
            for value in valuesDict:
                valueTemplate = np.rot90(valuesDict[value], 2)
                valueMatches = templateMatching.getMatches(searchArea, valueTemplate, matchingThreshold)
                valueMatches = map(lambda match: {'topLeft': (topLeft[0] + match[0], topLeft[1] + match[1]), 'name': value}, valueMatches)
                if (len(valueMatches) > 0):
                    cardsFound.add(value + ' ' + suit)
                allUpsidedownValueMatches = allUpsidedownValueMatches + valueMatches
        
        allMatches = allMatches + suitMatches + allValueMatches + suitMatchesUpsideDown + allUpsidedownValueMatches

    if len(allMatches) != 0:
        if testMode:
            image = templateMatching.highlightRois(areaToScan, allMatches, (30L, 30L))
            screen.showImage(image)
        else:
            cardsToShow = allCards.difference(cardsFound)
            sortedCards = sorted(cardsToShow, key=cmp_to_key(cardComparer))
            screen.showCards(sortedCards, valuesDict, suitsDict)

        
if testMode:
    watchAndDisplayCards()
else:
    # keep watching for cards forever
    while True:
        watchAndDisplayCards()