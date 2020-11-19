import requests
import re
from repository import ImageRepository

class ImageService():
    def __init__(self, config):
        self.repository = ImageRepository(config['repository'])

    def search(self, term):
        return self.repository.search(term)

    def download(self, url, timeout=10):
        r = requests.get(url, timeout=timeout)
        img_reg = re.compile("([\w-]+\.(jpe?g|png|gif|bmp))")
        file_name = img_reg.findall(url)
        '''
        We might want to use a hash of the file as name
        to avoid storing multiple times the same image
        '''
        if len(file_name) > 0:
            return {
                'file_name': file_name[0][0],
                # 'content': r.content,
                'content_type': r.headers.get('content_type')
            }
        raise Error("No image found")