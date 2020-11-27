import requests


IMDB_SERVICE_MOVIE_SEARCH_URL = "movie/search"
IMDB_SERVICE_GET_CAST_URL = "/movie/%s/cast"


class IMDbRepositoryException(Exception):
    pass


class IMDbRepository():
    def __init__(self, host):
        self.host = host

    def search_movies(self, term):
        query_params = {'name': term}
        api_url = "%s/%s" % (self.host, IMDB_SERVICE_MOVIE_SEARCH_URL)
        r = requests.get(api_url, params=query_params)
        if r.status_code == 200:
            return r.json()
        raise IMDbRepositoryException

    def list_cast(self, movie_id):
        api_url = "%s/%s" % (self.host,
                             IMDB_SERVICE_GET_CAST_URL % movie_id)
        r = requests.get(api_url)
        if r.status_code == 200:
            return r.json()
        raise IMDbRepositoryException
