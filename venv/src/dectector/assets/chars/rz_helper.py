import cv2
import sys

lettr = sys.argv[1]
img = cv2.imread(lettr + '.png')
rz = cv2.resize(img, (40, 100))
cv2.imwrite(lettr + '.png', rz)
