import requests
import time


IMAGES_SERVICE_SEARCH_URL = "images/search"


class ImagesRepositoryException(Exception):
    pass


class ImagesRepository():
    def __init__(self, host):
        self.host = host

    def search(self, term):
        query_params = {'term': term}
        api_url = "%s/%s" % (self.host, IMAGES_SERVICE_SEARCH_URL)

        r = requests.get(api_url, params=query_params)
        if r.status_code == 200:
            time.sleep(1)
            return r.json()
        raise ImagesRepositoryException
