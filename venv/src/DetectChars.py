# DetectChars.py
import os

import cv2
import numpy as np
import math
import random

import Preprocess
import PossibleChar

# module level variables ##########################################################################

kNearest = cv2.ml.KNearest_create()

# constants for checkIfPossibleChar, this checks one possible char only (does not compare to another char)
MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8

MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 80

# constants for comparing two chars
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

# other constants
MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100

SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)


###################################################################################################
# Se carga el KNN y se lo entrena
# def loadKNNDataAndTrainKNN():
#     allContoursWithData = []  # declare empty lists,
#     validContoursWithData = []  # we will fill these shortly
#
#     try:
#         npaClassifications = np.loadtxt("classifications.txt", np.float32)  # read in training classifications
#     except:  # if file could not be opened
#         print("error, unable to open classifications.txt, exiting program\n")  # show error message
#         os.system("pause")
#         return False  # and return False
#     # end try
#
#     try:
#         npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)  # read in training images
#     except:  # if file could not be opened
#         print("error, unable to open flattened_images.txt, exiting program\n")  # show error message
#         os.system("pause")
#         return False  # and return False
#     # end try
#
#     npaClassifications = npaClassifications.reshape(
#         (npaClassifications.size, 1))  # reshape numpy array to 1d, necessary to pass to call to train
#
#     kNearest.setDefaultK(1)  # set default K to 1
#
#     kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)  # train KNN object
#
#     return True  # if we got here training was successful so return true
#

# end function

###################################################################################################
# def detectCharsInPlates(listOfPossiblePlates):
#     intPlateCounter = 0
#     imgContours = None
#     contours = []
#
#     if len(listOfPossiblePlates) == 0:  # if list of possible plates is empty
#         return listOfPossiblePlates  # return
#     # end if
#
#     # at this point we can be sure the list of possible plates has at least one plate
#
#     for possiblePlate in listOfPossiblePlates:  # for each possible plate, this is a big for loop that takes up most of the function
#
#         possiblePlate.imgGrayscale, possiblePlate.imgThresh = Preprocess.preprocess(
#             possiblePlate.imgPlate)  # preprocess to get grayscale and threshold images
#
#         cv2.imshow("5a", possiblePlate.imgPlate)
#         cv2.imshow("5b", possiblePlate.imgGrayscale)
#         cv2.imshow("5c", possiblePlate.imgThresh)
#         # end if # show steps #####################################################################
#
#         # increase size of plate image for easier viewing and char detection
#         possiblePlate.imgThresh = cv2.resize(possiblePlate.imgThresh, (0, 0), fx=1.6, fy=1.6)
#
#         # threshold again to eliminate any gray areas
#         thresholdValue, possiblePlate.imgThresh = cv2.threshold(possiblePlate.imgThresh, 0.0, 255.0,
#                                                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#
#         cv2.imshow("5d", possiblePlate.imgThresh)
#         # end if # show steps #####################################################################
#
#         # find all possible chars in the plate,
#         # this function first finds all contours, then only includes contours that could be chars (without comparison to other chars yet)
#         listOfPossibleCharsInPlate = findPossibleCharsInPlate(possiblePlate.imgGrayscale, possiblePlate.imgThresh)
#
#         height, width, numChannels = possiblePlate.imgPlate.shape
#         imgContours = np.zeros((height, width, 3), np.uint8)
#         del contours[:]  # clear the contours list
#
#         for possibleChar in listOfPossibleCharsInPlate:
#             contours.append(possibleChar.contour)
#         # end for
#
#         cv2.drawContours(imgContours, contours, -1, SCALAR_WHITE)
#
#         cv2.imshow("6", imgContours)
#         # end if # show steps #####################################################################
#
#         # given a list of all possible chars, find groups of matching chars within the plate
#         listOfListsOfMatchingCharsInPlate = find_list_of_lists_of_matching_chars(listOfPossibleCharsInPlate)
#
#         imgContours = np.zeros((height, width, 3), np.uint8)
#         del contours[:]
#
#         for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
#             intRandomBlue = random.randint(0, 255)
#             intRandomGreen = random.randint(0, 255)
#             intRandomRed = random.randint(0, 255)
#
#             for matchingChar in listOfMatchingChars:
#                 contours.append(matchingChar.contour)
#             # end for
#             cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
#         # end for
#         cv2.imshow("7", imgContours)
#         # end if # show steps #####################################################################
#
#         if (len(listOfListsOfMatchingCharsInPlate) == 0):  # if no groups of matching chars were found in the plate
#
#             print("chars found in plate number " + str(
#                 intPlateCounter) + " = (none), click on any image and press a key to continue . . .")
#             intPlateCounter = intPlateCounter + 1
#             cv2.destroyWindow("8")
#             cv2.destroyWindow("9")
#             cv2.destroyWindow("10")
#             cv2.waitKey(0)
#             # end if # show steps #################################################################
#
#             possiblePlate.strChars = ""
#             continue  # go back to top of for loop
#         # end if
#
#         for i in range(0, len(listOfListsOfMatchingCharsInPlate)):  # within each list of matching chars
#             listOfListsOfMatchingCharsInPlate[i].sort(
#                 key=lambda matchingChar: matchingChar.intCenterX)  # sort chars from left to right
#             listOfListsOfMatchingCharsInPlate[i] = removeInnerOverlappingChars(
#                 listOfListsOfMatchingCharsInPlate[i])  # and remove inner overlapping chars
#         # end for
#
#         imgContours = np.zeros((height, width, 3), np.uint8)
#
#         for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
#             intRandomBlue = random.randint(0, 255)
#             intRandomGreen = random.randint(0, 255)
#             intRandomRed = random.randint(0, 255)
#
#             del contours[:]
#
#             for matchingChar in listOfMatchingChars:
#                 contours.append(matchingChar.contour)
#             # end for
#
#             cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
#         # end for
#         cv2.imshow("8", imgContours)
#         # end if # show steps #####################################################################
#
#         # within each possible plate, suppose the longest list of potential matching chars is the actual list of chars
#         intLenOfLongestListOfChars = 0
#         intIndexOfLongestListOfChars = 0
#
#         # loop through all the vectors of matching chars, get the index of the one with the most chars
#         for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
#             if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfLongestListOfChars:
#                 intLenOfLongestListOfChars = len(listOfListsOfMatchingCharsInPlate[i])
#                 intIndexOfLongestListOfChars = i
#             # end if
#         # end for
#
#         # suppose that the longest list of matching chars within the plate is the actual list of chars
#         longestListOfMatchingCharsInPlate = listOfListsOfMatchingCharsInPlate[intIndexOfLongestListOfChars]
#
#         imgContours = np.zeros((height, width, 3), np.uint8)
#         del contours[:]
#
#         for matchingChar in longestListOfMatchingCharsInPlate:
#             contours.append(matchingChar.contour)
#         # end for
#
#         cv2.drawContours(imgContours, contours, -1, SCALAR_WHITE)
#
#         cv2.imshow("9", imgContours)
#         # end if # show steps #####################################################################
#
#         possiblePlate.strChars = recognizeCharsInPlate(possiblePlate.imgThresh, longestListOfMatchingCharsInPlate)
#
#         print("chars found in plate number " + str(
#             intPlateCounter) + " = " + possiblePlate.strChars + ", click on any image and press a key to continue . . .")
#         intPlateCounter = intPlateCounter + 1
#         cv2.waitKey(0)
#         # end if # show steps #####################################################################
#
#     # end of big for loop that takes up most of the function
#
#     print("\nchar detection complete, click on any image and press a key to continue . . .\n")
#     cv2.waitKey(0)
#     # end if
#
#     return listOfPossiblePlates


# end function

###################################################################################################
def findPossibleCharsInPlate(imgGrayscale, imgThresh):
    listOfPossibleChars = []  # this will be the return value
    contours = []
    imgThreshCopy = imgThresh.copy()

    # find all contours in plate
    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:  # for each contour
        possibleChar = PossibleChar.PossibleChar(contour)

        if check_if_possible_char(
                possibleChar):  # if contour is a possible char, note this does not compare to other chars (yet) . . .
            listOfPossibleChars.append(possibleChar)  # add to list of possible chars
        # end if
    # end if

    return listOfPossibleChars


# end function

###################################################################################################
def check_if_possible_char(possible_char):
    # Es un primer paso para ver si el contorno puede ser un caracter.
    # No estamos comparando contra otros caracteres
    if (possible_char.intBoundingRectArea > MIN_PIXEL_AREA
            and possible_char.intBoundingRectWidth > MIN_PIXEL_WIDTH
            and possible_char.intBoundingRectHeight > MIN_PIXEL_HEIGHT
            and MIN_ASPECT_RATIO < possible_char.fltAspectRatio < MAX_ASPECT_RATIO):
        return True
    else:
        return False


###################################################################################################
def find_list_of_lists_of_matching_chars(list_of_possible_chars):
    # with this function, we start off with all the possible chars in one big list
    # the purpose of this function is to re-arrange the one big list of chars into a list of lists of matching chars,
    # note that chars that are not found to be in a group of matches do not need to be considered further
    list_of_lists_of_matching_chars = []  # this will be the return value

    for possible_char in list_of_possible_chars:
        list_of_matching_chars = find_list_of_matching_chars(possible_char, list_of_possible_chars)

        # also add the current char to current possible list of matching chars
        list_of_matching_chars.append(possible_char)

        # if current possible list of matching chars is not long enough to constitute a possible plate
        if len(list_of_matching_chars) < MIN_NUMBER_OF_MATCHING_CHARS:
            continue  # jump back to the top of the for loop and try again with next char, note that it's not necessary
            # to save the list in any way since it did not have enough chars to be a possible plate
        # end if

        # if we get here, the current list passed test as a "group" or "cluster" of matching chars
        list_of_lists_of_matching_chars.append(list_of_matching_chars)  # so add to our list of lists of matching chars

        list_of_possible_chars_with_current_matches_removed = []

        # remove the current list of matching chars from the big list so we don't use those same chars twice,
        # make sure to make a new big list for this since we don't want to change the original big list
        list_of_possible_chars_with_current_matches_removed = list(
            set(list_of_possible_chars) - set(list_of_matching_chars))

        recursive_list_of_lists_of_matching_chars = find_list_of_lists_of_matching_chars(
            list_of_possible_chars_with_current_matches_removed)  # recursive call

        for recursive_list_of_matching_chars in recursive_list_of_lists_of_matching_chars:
            list_of_lists_of_matching_chars.append(
                recursive_list_of_matching_chars)  # add to our original list of lists of matching chars
        break

    return list_of_lists_of_matching_chars


###################################################################################################
def find_list_of_matching_chars(possible_char, list_of_chars):
    # the purpose of this function is, given a possible char and a big list of possible chars,
    # find all chars in the big list that are a match for the single possible char,
    # and return those matching chars as a list
    list_of_matching_chars = []  # this will be the return value

    for possible_matching_char in list_of_chars:
        # if the char we attempting to find matches for is the exact same char as the char in the big list we are
        # currently checking
        if possible_matching_char == possible_char:
            # then we should not include it in the list of matches b/c that would end up double
            # including the current char
            continue

        # compute stuff to see if chars are a match
        flt_distance_between_chars = distanceBetweenChars(possible_char, possible_matching_char)

        flt_angle_between_chars = angleBetweenChars(possible_char, possible_matching_char)

        flt_change_in_area = float(
            abs(possible_matching_char.intBoundingRectArea - possible_char.intBoundingRectArea)) / float(
            possible_char.intBoundingRectArea)

        flt_change_in_width = float(
            abs(possible_matching_char.intBoundingRectWidth - possible_char.intBoundingRectWidth)) / float(
            possible_char.intBoundingRectWidth)

        flt_change_in_height = float(
            abs(possible_matching_char.intBoundingRectHeight - possible_char.intBoundingRectHeight)) / float(
            possible_char.intBoundingRectHeight)

        # check if chars match
        if (flt_distance_between_chars < (possible_char.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
                flt_angle_between_chars < MAX_ANGLE_BETWEEN_CHARS and
                flt_change_in_area < MAX_CHANGE_IN_AREA and
                flt_change_in_width < MAX_CHANGE_IN_WIDTH and
                flt_change_in_height < MAX_CHANGE_IN_HEIGHT):
            # if the chars are a match, add the current char to list of matching chars
            list_of_matching_chars.append(possible_matching_char)

    return list_of_matching_chars


###################################################################################################
# use Pythagorean theorem to calculate distance between two chars
def distanceBetweenChars(firstChar, secondChar):
    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))


# end function

###################################################################################################
# use basic trigonometry (SOH CAH TOA) to calculate angle between chars
def angleBetweenChars(firstChar, secondChar):
    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0.0:  # check to make sure we do not divide by zero if the center X positions are equal, float division by zero will cause a crash in Python
        fltAngleInRad = math.atan(fltOpp / fltAdj)  # if adjacent is not zero, calculate angle
    else:
        fltAngleInRad = 1.5708  # if adjacent is zero, use this as the angle, this is to be consistent with the C++ version of this program
    # end if

    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)  # calculate angle in degrees

    return fltAngleInDeg

# end function

###################################################################################################
# if we have two chars overlapping or to close to each other to possibly be separate chars, remove the inner (smaller) char,
# this is to prevent including the same char twice if two contours are found for the same char,
# for example for the letter 'O' both the inner ring and the outer ring may be found as contours, but we should only include the char once
# def removeInnerOverlappingChars(listOfMatchingChars):
#     listOfMatchingCharsWithInnerCharRemoved = list(listOfMatchingChars)  # this will be the return value
#
#     for currentChar in listOfMatchingChars:
#         for otherChar in listOfMatchingChars:
#             if currentChar != otherChar:  # if current char and other char are not the same char . . .
#                 # if current char and other char have center points at almost the same location . . .
#                 if distanceBetweenChars(currentChar, otherChar) < (
#                         currentChar.fltDiagonalSize * MIN_DIAG_SIZE_MULTIPLE_AWAY):
#                     # if we get in here we have found overlapping chars
#                     # next we identify which char is smaller, then if that char was not already removed on a previous pass, remove it
#                     if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:  # if current char is smaller than other char
#                         if currentChar in listOfMatchingCharsWithInnerCharRemoved:  # if current char was not already removed on a previous pass . . .
#                             listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)  # then remove current char
#                         # end if
#                     else:  # else if other char is smaller than current char
#                         if otherChar in listOfMatchingCharsWithInnerCharRemoved:  # if other char was not already removed on a previous pass . . .
#                             listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)  # then remove other char
#                         # end if
#                     # end if
#                 # end if
#             # end if
#         # end for
#     # end for
#
#     return listOfMatchingCharsWithInnerCharRemoved


# end function

###################################################################################################
# this is where we apply the actual char recognition
# def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
#     strChars = ""  # this will be the return value, the chars in the lic plate
#
#     height, width = imgThresh.shape
#
#     imgThreshColor = np.zeros((height, width, 3), np.uint8)
#
#     listOfMatchingChars.sort(key=lambda matchingChar: matchingChar.intCenterX)  # sort chars from left to right
#
#     cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR,
#                  imgThreshColor)  # make color version of threshold image so we can draw contours in color on it
#
#     for currentChar in listOfMatchingChars:  # for each char in plate
#         pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
#         pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth),
#                (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))
#
#         cv2.rectangle(imgThreshColor, pt1, pt2, SCALAR_GREEN, 2)  # draw green box around the char
#
#         # crop char out of threshold image
#         imgROI = imgThresh[
#                  currentChar.intBoundingRectY: currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
#                  currentChar.intBoundingRectX: currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]
#
#         imgROIResized = cv2.resize(imgROI, (
#             RESIZED_CHAR_IMAGE_WIDTH,
#             RESIZED_CHAR_IMAGE_HEIGHT))  # resize image, this is necessary for char recognition
#
#         npaROIResized = imgROIResized.reshape(
#             (1, RESIZED_CHAR_IMAGE_WIDTH * RESIZED_CHAR_IMAGE_HEIGHT))  # flatten image into 1d numpy array
#
#         npaROIResized = np.float32(npaROIResized)  # convert from 1d numpy array of ints to 1d numpy array of floats
#
#         retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized,
#                                                                      k=1)  # finally we can call findNearest !!!
#
#         strCurrentChar = str(chr(int(npaResults[0][0])))  # get character from results
#
#         strChars = strChars + strCurrentChar  # append current char to full string
#
#     # end for
#
#     cv2.imshow("10", imgThreshColor)
#     # end if # show steps #########################################################################
#
#     return strChars
# # end function
