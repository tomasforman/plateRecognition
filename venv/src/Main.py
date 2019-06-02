import cv2
import numpy as np
import os

from DetectChars import loadKNNDataAndTrainKNN
from DetectChars import detectCharsInPlates
from DetectPlates import detect_plates_in_scene
import PossiblePlate

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)


###################################################################################################
def main():
    # knn_training_successful = loadKNNDataAndTrainKNN()  # attempt KNN training
    #
    # if not knn_training_successful:
    #     print("\nError: KNN traning was not successful\n")
    #     return

    # Abrimos la imagen
    img_original_scene = cv2.imread("assets/plate5.jpeg")

    if img_original_scene is None:
        print("\nError: image not read from file \n\n")
        os.system("pause")
        return

    # detect plates
    list_of_possible_plates = detect_plates_in_scene(img_original_scene)

    print(list_of_possible_plates)

    for index, plate in enumerate(list_of_possible_plates):
        cv2.imshow("Muestra" + str(index), plate.imgPlate)
        cv2.imwrite("possiblePlate" + str(index) + ".jpg", plate.imgPlate)

    # # detect chars in plates
    # list_of_possible_plates = detectCharsInPlates(list_of_possible_plates)
    #
    print(list_of_possible_plates)

    if len(list_of_possible_plates) == 0:
        print("\nno license plates were detected\n")
    else:
        # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        list_of_possible_plates.sort(key=lambda possible_plate: len(possible_plate.strChars), reverse=True)

        # Suponemos que la patente con mas caracteres reconocidos es la patente
        lic_plate = list_of_possible_plates[0]

        # show crop of plate and threshold of plate
        cv2.imshow("imgPlate", lic_plate.imgPlate)
        # cv2.imshow("imgThresh", lic_plate.imgThresh)

        # Si no se encontraron caracteres en la patente
        if len(lic_plate.strChars) == 0:
            print("\nno characters were detected\n\n")
            return

        # Dibuja el recuadro de la patente en la imagen original #
        draw_rectangle_around_plate(img_original_scene, lic_plate, SCALAR_RED)

        print("\nlicense plate read from image = " + lic_plate.strChars + "\n")  # write license plate text to std out

        # # Escribe los caracteres encontrados sobre la imagen #
        # write_license_plate_chars_on_image(img_original_scene, lic_plate)
        # cv2.imshow("img_original_scene", img_original_scene)

        # Guarda la imagen con el recuadro y los caracteres de la patente #
        cv2.imwrite("img_original_scene.png", img_original_scene)

    cv2.waitKey(0)

    return


###################################################################################################

def draw_rectangle_around_plate(img_original_scene, lic_plate, color):
    p2f_rect_points = cv2.boxPoints(lic_plate.rrLocationOfPlateInScene)  # get 4 vertices of rotated rect
    cv2.line(img_original_scene, tuple(p2f_rect_points[0]), tuple(p2f_rect_points[1]), color, 2)
    cv2.line(img_original_scene, tuple(p2f_rect_points[1]), tuple(p2f_rect_points[2]), color, 2)
    cv2.line(img_original_scene, tuple(p2f_rect_points[2]), tuple(p2f_rect_points[3]), color, 2)
    cv2.line(img_original_scene, tuple(p2f_rect_points[3]), tuple(p2f_rect_points[0]), color, 2)


###################################################################################################

def write_license_plate_chars_on_image(img_original_scene, lic_plate):
    ptCenterOfTextAreaX = 0  # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0  # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = img_original_scene.shape
    plateHeight, plateWidth, plateNumChannels = lic_plate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX  # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0  # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))  # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(lic_plate.strChars, intFontFace, fltFontScale,
                                         intFontThickness)  # call getTextSize

    # unpack roatated rect into center point, width and height, and angle
    ((intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight),
     fltCorrectionAngleInDeg) = lic_plate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)  # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)  # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(
            round(plateHeight * 1.6))  # write the chars in below the plate
    else:  # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(
            round(plateHeight * 1.6))  # write the chars in above the plate
    # end if

    textSizeWidth, textSizeHeight = textSize  # unpack text size width and height

    ptLowerLeftTextOriginX = int(
        ptCenterOfTextAreaX - (textSizeWidth / 2))  # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(
        ptCenterOfTextAreaY + (textSizeHeight / 2))  # based on the text area center, width, and height

    # write the text on the image
    cv2.putText(img_original_scene, lic_plate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace,
                fltFontScale, SCALAR_YELLOW, intFontThickness)


main()

# https://github.com/MicrocontrollersAndMore/OpenCV_3_License_Plate_Recognition_Python/blob/master/readme.txt
