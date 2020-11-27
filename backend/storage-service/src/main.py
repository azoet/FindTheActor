import os
import sys
import base64
from flask import Flask, jsonify, request
from service import StorageService

app = Flask(__name__)

ENCODING = 'utf-8'

HOST = os.environ.get('HOST') if os.environ.get('HOST') else "0.0.0.0"
PORT = os.environ.get('PORT') if os.environ.get('PORT') else 8082

conf = {
    'repository': {}
}

if os.environ.get('REPOSITORY_LOCAL_BASE_PATH'):
    conf['repository']['local'] = {
        'base_path': os.environ.get('REPOSITORY_LOCAL_BASE_PATH')
    }
if os.environ.get('REPOSITORY_S3_BASE_PATH'):
    conf['repository']['s3'] = {
        'base_path': os.environ.get('REPOSITORY_S3_BASE_PATH'),
        'access_key_id': os.environ.get('REPOSITORY_S3_ACCESS_KEY_ID'),
        'secret_access_key': os.environ.get('REPOSITORY_S3_SECRET_ACCESS_KEY')
    }

service = StorageService(conf)


@app.route("/storage/download/image", methods=['POST'])
def download_file() -> str:
    url = request.json['url']
    path = request.json['path']
    on_conflict = request.json['onConflict']  # replace,append,
    try:
        service.store_image(url, path, on_conflict)
    except:
        e = sys.exc_info()[0]
        app.logger.error(e)
        return jsonify({
            'result': 'NO',
        }), 500
    return jsonify({
        'result': 'YES',
    })


@app.route("/storage/store/blob", methods=['POST'])
def store_blob() -> str:
    path = request.json['path']
    content = base64.b64decode(request.json['encoded_content'])
    service.store_blob(path, content)
    return jsonify({
        'result': 'YES',
    })


@app.route("/storage/store/json", methods=['POST'])
def store_json() -> str:
    path = request.json['path']
    content = request.json['json_content']
    service.store_json(path, content)
    return jsonify({
        'result': 'YES',
    })


@app.route("/storage/image")
def get_image() -> str:
    path = request.args.get('path')
    (file_name, content) = service.get_file(path)
    b64_bytes = base64.b64encode(content)
    b64_string = b64_bytes.decode(ENCODING)
    return jsonify({
        'file_name': file_name,
        'encoded_binary_content': b64_string
    })


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
