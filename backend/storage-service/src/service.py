import requests
import re
import json
from repository.s3 import S3ImageStorage
from repository.local import LocalImageStorage


class DownloadError(Exception):
    pass


class StorageService():
    def __init__(self, config):
        if "local" in config['repository']:
            self.repository = LocalImageStorage(
                **config['repository']['local'])
        elif "s3" in config['repository']:
            self.repository = S3ImageStorage(**config['repository']['s3'])
        else:
            # Raise
            pass

    def store_image(self, url, path, on_conflict="drop"):
        (file_name, binary_content, _) = download_image(url)
        self.repository.store_file(
            "%s/%s" % (path, file_name), binary_content, on_conflict)

    def store_blob(self, path, content):
        self.repository.store_file(path, content, "drop")

    def store_json(self, path, content):
        self.repository.store_file(
            path, bytes(json.dumps(content).encode('UTF-8')),
            "drop"
        )

    def get_file(self, path):
        file_name = path
        content = self.repository.get_file(path)
        return (file_name, content)


def download_image(file_url, timeout=10):
    r = requests.get(file_url, timeout=timeout)
    img_reg = re.compile(r"([\w-]+\.(jpe?g|png|gif|bmp))")
    if r.headers.get('content-disposition') is not None:
        file_name = r.headers.get('content-disposition')
    else:
        file_name = img_reg.findall(file_url)
    '''
    We might want to use a hash of the file as name
    to avoid storing multiple times the same image
    '''
    if len(file_name) > 0:
        return (file_name[0][0], r.content, r.headers.get('content-type'))
    raise DownloadError
