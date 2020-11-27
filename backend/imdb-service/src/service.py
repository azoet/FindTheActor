from repository import IMDbRepository


def deserialize_movie(movie):
    return {
        'id': movie.movieID,
        'title': movie['smart long imdb canonical title']
    }


def deserialize_actor(actor):
    return {
        'id': actor.personID,
        'name': actor['name']
    }


class IMDbService():
    def __init__(self):
        self.repository = IMDbRepository()

    def search_movie(self, q):
        return [deserialize_movie(m) for m in self.repository.search_movie(q)]

    def get_cast_from_movie(self, movie_id):
        return [deserialize_actor(c) for c in self.repository.get_cast_from_movie_id(movie_id)]
