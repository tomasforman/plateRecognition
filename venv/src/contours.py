import cv2
import pytesseract
import math
import numpy as np
import time

start = time.time()

kv = [
    ('W', [[2.03588111e-03], [1.47481652e-06], [4.81346100e-10], [1.36998533e-10], [2.61159089e-20], [5.11671159e-14], [
        -2.35718114e-20]]),
    ('3',
     [[1.24590574e-03], [6.42156666e-08], [2.14886124e-11], [3.29675630e-11], [-7.50108612e-22], [-8.29285181e-15], [
         -4.55300326e-22]]),
    (
    'A', [[1.63505956e-03], [3.37360433e-07], [3.31251001e-10], [2.77690495e-11], [-3.44114634e-22], [7.70712362e-15], [
        -2.64097578e-21]]),
    ('6', [[1.60477933e-03], [4.51164126e-07], [2.18426096e-10], [1.39082322e-10], [1.88173655e-20], [7.36821751e-14], [
        -1.52826339e-20]]),
    (
    'B', [[1.73352784e-03], [1.63627367e-07], [1.52538025e-10], [8.06747844e-12], [4.11696727e-23], [-3.10783581e-15], [
        -2.79995543e-22]]),
    ('M', [[1.51121711e-03], [7.25377109e-07], [1.82980458e-10], [1.25418736e-10], [1.89533897e-20], [9.72388338e-14], [
        1.32527427e-21]]),
    (
    '2', [[1.18322886e-03], [7.73922736e-08], [4.06898559e-11], [1.60586428e-11], [-1.00901793e-22], [2.50851656e-15], [
        -3.97899206e-22]])
]


def distance(hu1, hu2):
    if len(hu1) != len(hu2):
        return 100000000
    dst = 0.0
    for idx, item in enumerate(hu1):
        dst = dst + (math.fabs(item[0] - hu2[idx][0]))
    return dst


def findChar(hu):
    distances = [(k, distance(hu, v)) for (k, v) in kv]
    return min(distances, key=lambda a: a[1])[0]


def read_plate(img):
    # small = cv2.imread("../assets/patentes/possiblePlate2.jpg")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imshow('blurred', blurred)
    thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow('thresh', thresh)

    blur2 = cv2.GaussianBlur(thresh, (5, 5), 0)
    cv2.imshow('blur2', blur2)

    cnts, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    tup = [(c, cv2.contourArea(c)) for c in cnts]

    tup.sort(key=lambda x: x[1])
    filtered = [c for c in cnts if 200 < cv2.contourArea(c) < 500]

    if len(filtered) < 5:
        return

    chars = []
    for i, c in enumerate(filtered):
        (x, y, w, h) = cv2.boundingRect(c)
        crp = img[y:y + h, x:x + w]
        cv2.imshow('rect' + str(i), crp)
        crp_gray = cv2.cvtColor(crp, cv2.COLOR_BGR2GRAY)
        cv2.imshow('gray' + str(1), crp_gray)
        crp_blur = cv2.GaussianBlur(crp_gray, (5, 5), 0)
        cv2.imshow('blur' + str(i), crp_blur)
        crp_thresh = cv2.threshold(crp_blur, 127, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow('thresh' + str(i), crp_thresh)
        huMoments = cv2.HuMoments(cv2.moments(crp_thresh))
        ch = findChar(huMoments)
        print('hu char:', ch)
        chars.append(ch)

    chars.reverse()
    print('Plate with hu moments', ''.join(chars))

    print('processing text')
    rz = cv2.resize(img, (300, 50))
    cv2.imshow('rz', rz)
    text = pytesseract.image_to_string(rz, config='--psm 11')
    cv2.imshow('cnts', img)
    print('result', text)
    cv2.waitKey(0)
