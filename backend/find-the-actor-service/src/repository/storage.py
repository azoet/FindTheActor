import requests


STORAGE_DOWNLOAD_IMAGE_URL = "storage/download/image"


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
