import requests
import re
import numpy as np
import cv2
from mtcnn.mtcnn import MTCNN
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


class ImageService():
    def __init__(self, config):
        self.repository = ImageRepository(config['repository'])
        self.facerec_model = Detection()

    def search(self, term):
        return self.repository.search(term)

    def face_recognition(self, file_name, binary_content):
        nparr = np.fromstring(binary_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        drawing, boxes = self.facerec_model.box_faces(img)

        ext = file_name.rsplit('.', 1)[1]
        success, encoded_image = cv2.imencode('.%s' % ext, drawing)
        if success:
            return (encoded_image, boxes)
        return None

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
