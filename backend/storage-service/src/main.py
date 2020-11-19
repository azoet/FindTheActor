import os
import sys
from flask import Flask, jsonify, request
from service import StorageService

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
