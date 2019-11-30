import os
import cv2

files = os.listdir()
for f in files:
    if '.png' in f:
        im = cv2.imread(f)
        blur = cv2.GaussianBlur(im, (5, 5), 0)
        """gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        coords = cv2.findNonZero(gray)
        x, y, w, h = cv2.boundingRect(coords)
        rect = gray[y:y + h, x:x + w]
        rz = cv2.resize(rect, (40, 100))"""
        cv2.imwrite(f, blur)