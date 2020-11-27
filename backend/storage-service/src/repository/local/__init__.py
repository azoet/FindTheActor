import os
import uuid
from .. import InformalImageStorageInterface


class LocalImageStorage(InformalImageStorageInterface):
    def __init__(self, base_path='~'):
        self.base_path = base_path

    def store_file(self, path, binary_content, on_conflict):
        try:
            with open("%s/%s" % (self.base_path, path), 'xb') as f:
                f.write(binary_content)
        except FileNotFoundError:
            full_path = "%s/%s" % (self.base_path, path)
            base_path = '/'.join(full_path.rsplit('/')[:-1])
            os.makedirs(base_path)
            self.store_image(path, binary_content, on_conflict)
        except FileExistsError:
            # To remove if we want to avoid duplicates
            if on_conflict == "append":
                (file_name, ext) = path.split('.')
                self.store_image("%s_%s.%s" % (file_name, str(uuid.uuid4())[
                                 :8], ext), binary_content, on_conflict)

    def get_file(self, path):
        with open("%s/%s" % (self.base_path, path), 'rb') as f:
            return f.read()
