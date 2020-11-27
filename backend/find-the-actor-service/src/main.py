import sys
import os
import base64
import io
import json
from flask import Flask, jsonify, request, render_template, redirect, url_for, send_file
from service import FindTheActorService

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

HOST = os.environ.get('HOST') if os.environ.get('HOST') else "0.0.0.0"
PORT = os.environ.get('PORT') if os.environ.get('PORT') else 8083

conf = {
    'repository': {
        'imdb': {
            'host': 'http://localhost:8080'
        },
        'images': {
            'host': 'http://localhost:8081'
        },
        'storage': {
            'host': 'http://localhost:8082'
        }
    }
}

# Amir's mock function. Return actor's name


def recognitionModel(inputImage):
    return ["Person A", "Person B", "Person C"]


if os.environ.get('REPOSITORY_IMDB_HOST'):
    conf['repository']['imdb']['host'] = os.environ.get('REPOSITORY_IMDB_HOST')
if os.environ.get('REPOSITORY_IMAGES_HOST'):
    conf['repository']['images']['host'] = os.environ.get(
        'REPOSITORY_IMAGES_HOST')
if os.environ.get('REPOSITORY_STORAGE_HOST'):
    conf['repository']['storage']['host'] = os.environ.get(
        'REPOSITORY_STORAGE_HOST')

service = FindTheActorService(conf)

# Checking file's format


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/movie/search")
# Return a Json file with the movie list
def search_movie():
    q = request.args.get('q')
    return jsonify(service.search_movie(q))

# Get the images of actors in the show


@app.route("/movie/<int:movie_id>/prepare", methods=['POST'])
def movie_prepare(movie_id) -> str:
    return jsonify(service.prepare_movie_db(movie_id))

# Index of the website


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
# Uploading image
def upload():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        service.run_image_facerec(file.filename, file.read())
        return redirect(url_for('display_detect', filename=file.filename))
    return

# Display boxes choices


@app.route('/detect/<string:filename>')
def display_detect(filename):
    file_name_wo_ext = filename.rsplit('.')[0]
    boxes = service.get_file("Boxes_%s.json" % file_name_wo_ext)
    decoded_json = json.loads(base64.b64decode(
        boxes['encoded_binary_content']))
    return render_template('detect.html', filename=filename, boxes=decoded_json)


@app.route('/image/<string:filename>')
def display_image(filename):
    file = service.get_file(filename)
    decoded_image = base64.b64decode(file['encoded_binary_content'])
    return send_file(
        io.BytesIO(decoded_image),
        attachment_filename=filename,
        mimetype='image/jpg'
    )


@app.route('/result/<string:filename>/<int:boxnumber>')
def result(filename, boxnumber):
    cropped_image = service.get_cropped_image(filename, boxnumber)
    file_name_cropped = 'BOX_%i_%s' % (boxnumber, filename)
    service.store_image(file_name_cropped,
                        cropped_image['binary_encoded_content'])
    data = recognitionModel(cropped_image['binary_encoded_content'])
    return render_template('result.html', data=data, filename=file_name_cropped)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
