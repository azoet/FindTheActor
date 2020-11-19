import sys
import os
from flask import Flask, jsonify, request
from service import FindTheActorService

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


if os.environ.get('REPOSITORY_IMDB_HOST'):
    conf['repository']['imdb']['host'] = os.environ.get('REPOSITORY_IMDB_HOST')
if os.environ.get('REPOSITORY_IMAGES_HOST'):
    conf['repository']['images']['host'] = os.environ.get('REPOSITORY_IMAGES_HOST')
if os.environ.get('REPOSITORY_STORAGE_HOST'):
    conf['repository']['storage']['host'] = os.environ.get('REPOSITORY_STORAGE_HOST')

service = FindTheActorService(conf)


@app.route("/movie/search")
def search_movie():
    q = request.args.get('q')
    return jsonify(service.search_movie(q))


@app.route("/movie/<int:movie_id>/prepare", methods=['POST'])
def movie_prepare(movie_id) -> str:
    return jsonify(service.prepare_movie_db(movie_id))


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
