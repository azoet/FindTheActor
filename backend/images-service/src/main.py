import os
from flask import Flask, jsonify, request
from service import ImageService

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

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)