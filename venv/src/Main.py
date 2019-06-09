import cv2
import os
import time
from multiprocessing import Process

from DetectPlates import detect_plates_in_scene
import PossiblePlate
from contours import read_plate

# variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

IMG_MAX_WIDTH = 1280

SAVE_IMAGE = True
NO_ERROR_PRINT_ENABLED = False
SHOW_IMAGE = False


###################################################################################################
def recognize_plate(img_original_scene):
    if img_original_scene is None:
        print("\n### Error: image not found ### \n\n")
        os.system("pause")
        return

    height, width = img_original_scene.shape[:2]
    img_scale = IMG_MAX_WIDTH / width

    new_x, new_y = img_original_scene.shape[1] * img_scale, img_original_scene.shape[0] * img_scale

    img_original_scene = cv2.resize(img_original_scene, (int(new_x), 720))

    # Paso 1: Detectar las posibles patentes en la imagen
    list_of_possible_plates = detect_plates_in_scene(img_original_scene)

    if len(list_of_possible_plates) == 0:
        print("\n### No license plates were detected ###\n")
    else:
        # Paso 2: Leer los caracteres de las posibles patentes
        for index, plate in enumerate(list_of_possible_plates):
            if SAVE_IMAGE:
                cv2.imwrite("./output/possiblePlate" + str(index) + ".jpg", plate.imgPlate)
            if SHOW_IMAGE:
                cv2.imshow("Muestra" + str(index), plate.imgPlate)
            # plate_chars = read_plate(plate.imgPlate)

        # Si no se encontraron caracteres en la patente
        # if len(plate_chars) == 0:
        #     print("\nno characters were detected\n\n")
        #     return

    #  TODO habria que guardar la imagen con la patente y recuadrar la patente

    cv2.waitKey(0)

    return


###################################################################################################

def draw_rectangle_around_plate(img_original_scene, lic_plate, color):
    p2f_rect_points = cv2.boxPoints(lic_plate.rrLocationOfPlateInScene)
    cv2.line(img_original_scene, tuple(p2f_rect_points[0]), tuple(p2f_rect_points[1]), color, 2)
    cv2.line(img_original_scene, tuple(p2f_rect_points[1]), tuple(p2f_rect_points[2]), color, 2)
    cv2.line(img_original_scene, tuple(p2f_rect_points[2]), tuple(p2f_rect_points[3]), color, 2)
    cv2.line(img_original_scene, tuple(p2f_rect_points[3]), tuple(p2f_rect_points[0]), color, 2)


###################################################################################################

def write_license_plate_chars_on_image(img_original_scene, lic_plate):
    pt_center_of_text_area_x = 0
    pt_center_of_text_area_y = 0

    pt_lower_left_text_origin_x = 0
    pt_lower_left_text_origin_y = 0

    scene_height, scene_width, scene_num_channels = img_original_scene.shape
    plate_height, plate_width, plate_num_channels = lic_plate.imgPlate.shape

    int_font_face = cv2.FONT_HERSHEY_SIMPLEX
    flt_font_scale = float(plate_height) / 30.0
    int_font_thickness = int(round(flt_font_scale * 1.5))

    text_size, baseline = cv2.getTextSize(lic_plate.strChars, int_font_face, flt_font_scale, int_font_thickness)

    # unpack roatated rect into center point, width and height, and angle
    ((int_plate_center_x, int_plate_center_y), (int_plate_width, int_plate_height),
     fltCorrectionAngleInDeg) = lic_plate.rrLocationOfPlateInScene

    int_plate_center_x = int(int_plate_center_x)
    int_plate_center_y = int(int_plate_center_y)

    pt_center_of_text_area_x = int(int_plate_center_x)

    # if the license plate is in the upper 3/4 of the image
    if int_plate_center_y < (scene_height * 0.75):
        pt_center_of_text_area_y = int(round(int_plate_center_y)) + int(round(plate_height * 1.6))
    else:
        pt_center_of_text_area_y = int(round(int_plate_center_y)) - int(round(plate_height * 1.6))

    text_size_width, text_size_height = text_size

    # calculate the lower left origin of the text area
    pt_lower_left_text_origin_x = int(pt_center_of_text_area_x - (text_size_width / 2))

    # based on the text area center, width, and height
    pt_lower_left_text_origin_y = int(pt_center_of_text_area_y + (text_size_height / 2))

    # write the text on the image
    cv2.putText(img_original_scene, lic_plate.strChars, (pt_lower_left_text_origin_x, pt_lower_left_text_origin_y),
                int_font_face, flt_font_scale, SCALAR_YELLOW, int_font_thickness)


def main():
    img1 = cv2.imread("assets/plateSorento.jpg")
    start_time = time.time()
    recognize_plate(img1)
    finish_time = time.time() - start_time
    print("--- Image 1: %s seconds ---" % finish_time)


if __name__ == "__main__":
    main()
