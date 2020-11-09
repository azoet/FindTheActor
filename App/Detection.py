from mtcnn.mtcnn import MTCNN
import cv2

class Detection:
    def __init__(self):
        self.model = MTCNN()

    def box_faces(self, image):
        faces = self.model.detect_faces(image)
        drawing = image.copy()
        for face in faces:
            x, y, width, height = face['box']
            drawing = cv2.rectangle(drawing, (x, y), (x+width, y+height), (0, 0, 255), 5)
        return drawing
