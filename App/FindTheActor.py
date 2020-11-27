from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from Detection import Detection
import cv2
import numpy as np
import pickle
from base64 import b64encode

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = 'gi2tn2k6plnr9th5nad52jgofmp6'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load models
detectionModel = Detection()


def recognitionModel(inputImage):
    return ["Person A", "Person B", "Person C"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/image/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='images/' + filename))


@app.route('/detect/<filename>', methods=['GET'])
def display_detect(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath + '.pickle', 'rb') as handle:
        boxes = pickle.load(handle)
    return render_template('detect.html', filename=filename, boxes=boxes)


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        npimg = np.fromfile(file, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        drawing, boxes = detectionModel.box_faces(img)
        filename = secure_filename(file.filename)
        filename_boxed = "Boxed_"+filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        filepath_boxed = os.path.join(
            app.config['UPLOAD_FOLDER'], filename_boxed)
        with open(filepath + '.pickle', 'wb') as handle:
            pickle.dump(boxes, handle, protocol=pickle.HIGHEST_PROTOCOL)
        cv2.imwrite(filepath, img)
        cv2.imwrite(filepath_boxed, drawing)
        return redirect(url_for('display_detect', filename=filename))
    return


@app.route('/result/<filename>/<boxnumber>')
def result(filename, boxnumber):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    filename_cropped = "Box"+boxnumber+filename
    filepath_cropped = os.path.join(
        app.config['UPLOAD_FOLDER'], filename_cropped)
    with open(filepath + '.pickle', 'rb') as handle:
        boxes = pickle.load(handle)
    x, y, width, height = boxes[int(boxnumber)-1]
    if not os.path.isfile(filepath_cropped):
        image = cv2.imread(filepath)
        cropped = image[y:y+height, x:x+width]
        cv2.imwrite(filepath_cropped, cropped)
    else:
        cropped = cv2.imread(filepath_cropped)
    data = recognitionModel(cropped)
    return render_template('result.html', data=data, filename=filename_cropped)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
