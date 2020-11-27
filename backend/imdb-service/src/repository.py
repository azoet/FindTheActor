import imdb


class IMDbRepository():
    def __init__(self):
        self.ia = imdb.IMDb()

    def search_movie(self, q):
        return self.ia.search_movie(q)

    def get_cast_from_movie_id(self, movie_id):
        return self.ia.get_movie(movie_id)['cast']
