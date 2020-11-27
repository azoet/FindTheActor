import requests
import base64


ENCODING = "utf-8"
STORAGE_DOWNLOAD_IMAGE_URL = "storage/download/image"
STORAGE_STORE_BLOB_URL = "storage/store/blob"
STORAGE_STORE_JSON_URL = "storage/store/json"
STORAGE_IMAGE_GET_URL = "storage/image"


class StorageRepositoryException(Exception):
    pass


class StorageRepository():
    def __init__(self, host):
        self.host = host

    def download(self, folder, url):
        r = requests.post("%s/%s" % (self.host, STORAGE_DOWNLOAD_IMAGE_URL), json={
            'url': url,
            'path': folder,
            'onConflict': 'drop'
        })
        if r.status_code == 200:
            return r.json()
        raise StorageRepositoryException

    def store(self, folder, file_name, content, encode=True):
        if encode:
            b64_bytes = base64.b64encode(content)
            content = b64_bytes.decode(ENCODING)
        r = requests.post("%s/%s" % (self.host, STORAGE_STORE_BLOB_URL), json={
            'path': '%s/%s' % (folder, file_name),
            'encoded_content': content
        })
        if r.status_code == 200:
            return r.json()
        raise StorageRepositoryException

    def store_json(self, folder, file_name, json_content):
        r = requests.post("%s/%s" % (self.host, STORAGE_STORE_JSON_URL), json={
            'path': '%s/%s' % (folder, file_name),
            'json_content': json_content
        })
        if r.status_code == 200:
            return r.json()
        raise StorageRepositoryException

    def get_file(self, path):
        r = requests.get("%s/%s" % (self.host, STORAGE_IMAGE_GET_URL), params={
            'path': path
        })
        if r.status_code == 200:
            return r.json()
        raise StorageRepositoryException
