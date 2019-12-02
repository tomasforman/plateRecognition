import base64
import os
import time
import paho.mqtt.client as mqtt
import cv2
import json
import PossiblePlate
import io
from imageio import imread
from DetectPlates import detect_plates_in_scene

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

PLATES_TOPIC = os.getenv("PLATES_TOPIC")

###################################################################################################
def recognize_plate(img_original_scene) -> [PossiblePlate]:
    if img_original_scene is None:
        print("\n### Error: image not found ### \n\n")
        os.system("pause")
        return
    list_of_possible_plates: [PossiblePlate] = []

    img_resized = resize_image(img_original_scene)

    # Detectar las posibles patentes en la imagen
    list_of_possible_plates = detect_plates_in_scene(img_resized)

    return list_of_possible_plates


###################################################################################################
def resize_image(img):
    height, width = img.shape[:2]

    img_scale = IMG_MAX_WIDTH / width

    new_x, new_y = img.shape[1] * img_scale, img.shape[0] * img_scale

    return cv2.resize(img, (int(new_x), 720))


def save_image(img, path):
    if img is None:
        print("\n### Error: image not found ### \n\n")
        os.system("pause")
        return
    cv2.imwrite(path, img)


###################################################################################################
# NO SE USA

def draw_rectangle_around_plate(img_original_scene, lic_plate, color):
    p2f_rect_points = cv2.boxPoints(lic_plate.rrLocationOfPlateInScene)
    cv2.line(img_original_scene, tuple(p2f_rect_points[0]), tuple(p2f_rect_points[1]), color, 2)
    cv2.line(img_original_scene, tuple(p2f_rect_points[1]), tuple(p2f_rect_points[2]), color, 2)
    cv2.line(img_original_scene, tuple(p2f_rect_points[2]), tuple(p2f_rect_points[3]), color, 2)
    cv2.line(img_original_scene, tuple(p2f_rect_points[3]), tuple(p2f_rect_points[0]), color, 2)


###################################################################################################
# NO SE USA

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


###################################################################################################

def process(b64):
    img = imread(io.BytesIO(base64.b64decode(b64)))
    cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return recognize_plate(cv2_img)


def on_message(client, userdata, msg):
    start_time = time.time()
    payload = json.loads(msg.payload)
    print(msg.payload)
    print(payload["id"])
    b64_img = payload["image"]
    img = imread(io.BytesIO(base64.b64decode(b64_img)))
    cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    list_of_possible_plates = recognize_plate(cv2_img)
    print(len(list_of_possible_plates))
    if len(list_of_possible_plates) > 0:
        plate_img = list_of_possible_plates[0].imgPlate
        _, buffer = cv2.imencode('.jpg', plate_img)
        jpg_as_text = base64.b64encode(buffer)
        finish_time = time.time() - start_time
        print("--- Time to process: %s seconds ---" % finish_time)
        to_publish = '"{"plate": "' + jpg_as_text + '" "id": "' + payload["id"] + '"}"'
        client.publish(PLATES_TOPIC, to_publish)
        # file_name = f'/tmp/plates/{payload["id"]}.jpg'
        # cv2.imwrite(file_name, buffer)
        # upload_to_s3(file_name)


def main():
    mq_host = os.getenv('MQTT_HOST')
    mq_port = os.getenv('MQTT_PORT')
    mq_topic = os.getenv('MQTT_TOPIC')
    print(f"[SETUP] MQTT host {mq_host} MQTT port {mq_port}")
    client = mqtt.Client()
    client.connect(host=mq_host, port=int(mq_port))
    client.subscribe(mq_topic)

    client.on_message = on_message

    print("Waiting for messages .....")
    client.loop_forever()


if __name__ == "__main__":
    main()
