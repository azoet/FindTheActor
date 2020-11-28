import requests
import re
import numpy as np
import cv2
from mtcnn.mtcnn import MTCNN
from tensorflow import keras
from repository import ImageRepository


class Detection:
    def __init__(self):
        self.model = MTCNN()

    def box_faces(self, image):
        faces = self.model.detect_faces(image)
        drawing = image.copy()
        boxes = []
        height, width, _ = drawing.shape
        for i, face in enumerate(faces):
            x, y, width, height = box = face['box']
            fontscale = self.get_fontscale("Box " + str(i+1), width)
            thickness = int(fontscale)
            drawing = cv2.rectangle(
                drawing, (x, y), (x+width, y+height), (0, 0, 255), thickness)
            drawing = cv2.putText(drawing, "Box " + str(i+1), (x, y-5), cv2.FONT_HERSHEY_COMPLEX,
                                  fontscale, (0, 0, 255), thickness)
            boxes.append(box)
        return drawing, boxes

    def get_fontscale(self, text, width):
        for scale in reversed(range(0, 60, 1)):
            textSize = cv2.getTextSize(
                text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale / 10, thickness=1)
            new_width = textSize[0][0]
            if new_width <= width:
                return scale / 10
        return 1


class Recognition:
    def __init__(self, config):
        self.model = keras.models.load_model(config['model_path'])
        self.image_width = int(config['image_size_width'])
        self.image_height = int(config['image_size_height'])

    def predict(self, cropped_image):
        nparr = np.fromstring(cropped_image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        resized_img = cv2.resize(img, (self.image_width, self.image_height))
        expanded_resized_img = np.expand_dims(resized_img, axis=0)
        return self.model.predict(expanded_resized_img)


class ImageService():
    def __init__(self, config):
        self.repository = ImageRepository(config['repository'])
        self.face_detection_model = Detection()
        self.face_recognition_model = Recognition(config['recognition'])

    def search(self, term):
        return self.repository.search(term)

    def face_detection(self, file_name, binary_content):
        nparr = np.fromstring(binary_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        drawing, boxes = self.face_detection_model.box_faces(img)
        ext = file_name.rsplit('.', 1)[1]
        success, encoded_image = cv2.imencode('.%s' % ext, drawing)
        if success:
            return (encoded_image, boxes)
        return None

    def face_recognition(self, binary_content):
        pred = self.face_recognition_model.predict(binary_content)[0]
        return np.argsort(-pred)[3:].tolist()

    def crop_image(self, binary_content, box, ext="jpg"):
        nparr = np.fromstring(binary_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        x = int(box['x'])
        y = int(box['y'])
        width = int(box['width'])
        height = int(box['height'])
        cropped = img[y:y+height, x:x+width]
        success, encoded_image = cv2.imencode('.%s' % ext, cropped)
        if success:
            return encoded_image
        return None
