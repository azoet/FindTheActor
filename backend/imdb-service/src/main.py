import os
from flask import Flask, jsonify, request
from service import IMDbService

app = Flask(__name__)

service = IMDbService()

HOST = os.environ.get('HOST') if os.environ.get('HOST') else "0.0.0.0"
PORT = os.environ.get('PORT') if os.environ.get('PORT') else 8080


@app.route("/movie/search")
def search_movie() -> str:
    q = request.args.get('name')
    return jsonify(service.search_movie(q))


@app.route("/movie/<int:movie_id>/cast")
def get_cast(movie_id) -> str:
    return jsonify(service.get_cast_from_movie(movie_id))


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
