import requests
import re
from repository.s3 import S3ImageStorage
from repository.local import LocalImageStorage

class DownloadError(Exception):
    pass


class StorageService():
    def __init__(self, config):
        if "local" in config['repository']:
            self.repository = LocalImageStorage(**config['repository']['local'])
        elif "s3" in config['repository']:
            self.repository = S3ImageStorage(**config['repository']['s3'])
        else:
            # Raise
            pass

    def store_image(self, url, path, on_conflict="drop"):
        (file_name, binary_content, content_type) = download_image(url)
        self.repository.store_image("%s/%s" % (path, file_name), binary_content, content_type, on_conflict)

def download_image(file_url,timeout=10):
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