import botocore
import boto3
import uuid
from .. import InformalImageStorageInterface

class S3ImageStorage(InformalImageStorageInterface):
    def __init__(self, base_path, access_key_id, secret_access_key):
        self.base_path = base_path
        self.client = boto3.client(
            's3',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )

    def store_image(self, path, binary_content, content_type, on_conflict):
        try:
            self.client.head_object(Bucket=self.base_path, Key=path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404" or on_conflict == "replace":
                # The object does not exist.
                self.client.put_object(
                    Body=binary_content,
                    Bucket=self.base_path,
                    Key=path
                )
            else:
                # Something else has gone wrong
                raise
        else:
            # The object does exist.
            if on_conflict == "append":
                (file_name, ext) = path.split('.')
                self.store_image("%s_%s.%s" % (file_name, str(uuid.uuid4())[:8], ext), binary_content, content_type, on_conflict)