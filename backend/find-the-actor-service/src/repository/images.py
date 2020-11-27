import requests
import time
import base64


IMAGES_SERVICE_SEARCH_URL = "images/search"
IMAGES_SERVICE_FACEREC_URL = "images/facerec"
IMAGES_SERVICE_CROP_URL = "images/crop"

ENCODING = 'utf-8'


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

    def face_recognition(self, file_name, file_content):
        api_url = "%s/%s" % (self.host, IMAGES_SERVICE_FACEREC_URL)

        b64_bytes = base64.b64encode(file_content)
        b64_string = b64_bytes.decode(ENCODING)

        r = requests.post(api_url, json={
            'file_name': file_name,
            'file_content': b64_string,
        })
        if r.status_code == 200:
            content = r.json()
            return (base64.b64decode(content['boxed_image']), content['boxes'])
        raise ImagesRepositoryException

    def crop_image(self, encoded_content, box):
        api_url = "%s/%s" % (self.host, IMAGES_SERVICE_CROP_URL)

        r = requests.post(api_url, json={
            'binary_encoded_content': encoded_content,
            'box': box
        })
        if r.status_code == 200:
            return r.json()
        raise ImagesRepositoryException
