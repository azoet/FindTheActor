from mtcnn.mtcnn import MTCNN
import cv2

class Detection:
    def __init__(self):
        self.model = MTCNN()

    def box_faces(self, image):
        faces = self.model.detect_faces(image)
        drawing = image.copy()
        boxes = []
        for i, face in enumerate(faces):
            x, y, width, height = box = face['box']
            drawing = cv2.rectangle(drawing, (x, y), (x+width, y+height), (0, 0, 255), 5)
            drawing = cv2.putText(drawing, "Box " + str(i+1), (x, y), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 10)
            boxes.append(box)
        return drawing, boxes
