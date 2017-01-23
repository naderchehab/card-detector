import sys
import cv2
import numpy as np
import os.path as path
import templateMatching

screenCap = cv2.imread("tests/bb1.jpg", cv2.IMREAD_GRAYSCALE)

topLeft = (475L, 111L)
bottomRight = (1072L, 730L)
areaToScan = screenCap[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]]

# things we're looking for
suits = ['heart', 'spade', 'diamond', 'club']
values = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen','king', 'ace']

# for testing
# suits = ['spade']
# values = ['three']

def getImage(name):
    filename = name + '.png';
    image = cv2.imread(path.join("images", filename), cv2.IMREAD_GRAYSCALE)
    return {'image': image, 'name': name}

suits = map(getImage, suits)
values = map(getImage, values)
whitespace = np.full((1L, len(suits[0]['image'][0])), 255L, dtype = "uint8")
allMatches = []

for value in values:
    for suit in suits:
        template = np.concatenate([value['image'], whitespace, suit['image']])
        upsideDownTemplate = np.rot90(template, 2)
        
        matches = templateMatching.getMatches(areaToScan, template)
        # print value['name'], suit['name'], len(matches)
        matchesUpsideDown = templateMatching.getMatches(areaToScan, upsideDownTemplate)
        allMatches = allMatches + matches
        if matchesUpsideDown:
            allMatches = allMatches + matchesUpsideDown
    
if len(allMatches) != 0:
    image = templateMatching.highlightRois(areaToScan, allMatches, template.shape[::-1])
    templateMatching.showImage(image)
            

