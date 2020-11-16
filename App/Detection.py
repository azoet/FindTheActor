from mtcnn.mtcnn import MTCNN
import cv2

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
            drawing = cv2.rectangle(drawing, (x, y), (x+width, y+height), (0, 0, 255), thickness)
            drawing = cv2.putText(drawing, "Box " + str(i+1), (x, y-5), cv2.FONT_HERSHEY_COMPLEX,
                                  fontscale, (0, 0, 255), thickness)
            boxes.append(box)
        return drawing, boxes

    def get_fontscale(self, text, width):
        for scale in reversed(range(0, 60, 1)):
            textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale / 10, thickness=1)
            new_width = textSize[0][0]
            if new_width <= width:
                return scale / 10
        return 1

