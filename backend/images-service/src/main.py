import os
import base64
from flask import Flask, jsonify, request
from service import ImageService

ENCODING = 'utf-8'

app = Flask(__name__)

HOST = os.environ.get('HOST') if os.environ.get('HOST') else "0.0.0.0"
PORT = os.environ.get('PORT') if os.environ.get('PORT') else 8081

conf = {
    'repository': {}
}

if os.environ.get('REPOSITORY_BING_API_KEY'):
    conf['repository']['bing'] = {
        'api_key': os.environ.get('REPOSITORY_BING_API_KEY'),
        'custom_config_id': os.environ.get('REPOSITORY_BING_CUSTOM_CONFIG_ID'),
        'max_results': int(os.environ.get('REPOSITORY_BING_MAX_RESULTS'))
    }

service = ImageService(conf)


@app.route("/images/search")
def search_images() -> str:
    q = request.args.get('term')
    return jsonify(service.search(q))


@app.route("/images/facerec", methods=['POST'])
def face_recognition() -> str:
    decoded_content = base64.b64decode(request.json['file_content'])
    (boxed_image, boxes) = service.face_recognition(
        request.json['file_name'], decoded_content)
    b64_bytes = base64.b64encode(boxed_image)
    return jsonify({
        'boxed_image': b64_bytes.decode(ENCODING),
        'boxes': boxes,
    })


@app.route("/images/crop", methods=['POST'])
def crop_image() -> str:
    decoded_content = base64.b64decode(request.json['binary_encoded_content'])
    box = request.json['box']
    cropped_image = service.crop_image(decoded_content, box)
    b64_bytes = base64.b64encode(cropped_image)
    return jsonify({
        'binary_encoded_content': b64_bytes.decode(ENCODING)
    })


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
