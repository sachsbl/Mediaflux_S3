import boto3
import botocore


class S3ClientException(Exception):
    pass


class S3Client(object):
    def __init__(self, aws_access_key_id, aws_secret_access_key, endpoint='https://s3.amazonaws.com',
                 region_name='us-east-1', mediaflux=False):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint = endpoint
        self.region_name = region_name
        self.mediaflux=mediaflux

        # monkey patching of the header parsing to fix commas in ContentLength
        if self.mediaflux:
            def _custom_handle_integer(shape, text):
                # remove comma
                text = text.split(',')[0]
                return int(text)

            def _new_parse_shape(self, shape, node):
                if shape.name == 'ContentLength':
                    handler = _custom_handle_integer
                else:
                    handler = getattr(self, '_handle_%s' % shape.type_name,
                                      self._default_handle)
                return handler(shape, node)

            # apply patch
            botocore.parsers.ResponseParser._parse_shape = _new_parse_shape

            # custom signature for mediaflux
            config = botocore.client.Config(signature_version='s3v4', s3={'addressing_style': 'path'})

            self.s3_client = boto3.client(
                service_name='s3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                endpoint_url=self.endpoint,
                region_name=self.region_name,
                config=config
            )
        else:
            self.s3_client = boto3.client(
                service_name='s3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                endpoint_url=self.endpoint,
                region_name=self.region_name
            )

    def list_objects(self, bucket, prefix=''):
        """returns object dictionary. Prefix value filters the results to contain any keys starting with the text
        provided. This is essentially an abstraction of boto3's list_objects_v2"""

        try:
            objects = self.s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
            return objects
        except Exception as list_objects_error:
            raise S3ClientException(list_objects_error)

    def upload_file(self, local_file_path, destination_bucket, destination_key):
        try:
            self.s3_client.upload_file(local_file_path, destination_bucket, destination_key)
        except Exception as upload_error:
            raise S3ClientException(upload_error)

    def download_file(self, bucket, key, destination_path):
        try:
            self.s3_client.download_file(bucket, key, destination_path)
        except Exception as download_error:
            raise S3ClientException(download_error)
