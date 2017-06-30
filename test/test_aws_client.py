import os
import uuid

import pytest

from python_s3_client.s3_client import S3Client, S3ClientException

s3_client = S3Client(aws_access_key_id='',
                     aws_secret_access_key='')

TEST_BUCKET = 'my-bucket'

'''test setup here expects a bucket that you have PUT_OBJECT and GET_OBJECT credentials for.
It needs a file at /test named testRaster.tif'''


class TestListObjects:
    def test_valid_s3_location_no_prefix_returns_object_dict(self):
        objects = s3_client.list_objects(TEST_BUCKET)
        assert type(objects) == dict
        assert objects['KeyCount'] > 0

    def test_valid_s3_location_existing_prefix_returns_object_dict(self):
        objects = s3_client.list_objects(TEST_BUCKET, 'TEST')
        assert type(objects) == dict
        assert objects['KeyCount'] > 0

    def test_valid_s3_location_random_prefix_returns_empty_object_list(self):
        objects = s3_client.list_objects(TEST_BUCKET, 'zkghkdfgnkdfgjsdfjg')
        assert objects['KeyCount'] == 0

    def test_invalid_s3_bucket_raises(self):
        with pytest.raises(S3ClientException) as context:
            _ = s3_client.list_objects('fake_bucket')

        # depends on auth
        assert "Access Denied" in str(context.value) or "does not exist" in str(context.value)


class TestUploadFile:
    test_file = os.path.dirname(os.path.realpath(__file__)) + '/test_data/testDEM.tif'
    upload_location = 'test'

    def test_valid_s3_location_valid_file_uploads_file(self):
        original_file_count = s3_client.list_objects(TEST_BUCKET, self.upload_location)['KeyCount']

        s3_client.upload_file(self.test_file, TEST_BUCKET, '{}/{}.txt'.format(self.upload_location, uuid.uuid4()))

        file_count = s3_client.list_objects(TEST_BUCKET, self.upload_location)['KeyCount']

        assert file_count > original_file_count

    def test_invalid_s3_bucket_valid_file_raises(self):
        with pytest.raises(S3ClientException) as context:
            s3_client.upload_file(self.test_file, 'fake_bucket', '{}.tif'.format(uuid.uuid4()))

        assert "Failed to upload" in str(context.value)

    def test_valid_s3_bucket_invalid_file_raises(self):
        with pytest.raises(S3ClientException) as context:
            s3_client.upload_file('/fake/path.tif', TEST_BUCKET, '{}.tif'.format(uuid.uuid4()))

        assert "No such file" in str(context.value)


class TestDownloadFile:
    test_dir = os.path.dirname(os.path.realpath(__file__)) + '/test_data'
    test_file_key = 'test/testRaster.tif'

    def test_valid_s3_location_valid_file_downloads_file(self):
        file_path = self.test_dir + '/download_{}'.format(uuid.uuid4())

        assert not os.path.isfile(file_path)

        s3_client.download_file(TEST_BUCKET, self.test_file_key, file_path)

        assert os.path.isfile(file_path)

        os.remove(file_path)

    def test_invalid_s3_bucket_valid_key_raises(self):
        file_path = self.test_dir + '/download_{}'.format(uuid.uuid4())

        with pytest.raises(S3ClientException) as context:
            s3_client.download_file('fake_bucket', self.test_file_key, file_path)

        # depends on auth
        assert 'Forbidden' in str(context.value) or 'Not Found' in str(context.value)

    def test_valid_s3_bucket_invalid_key_raises(self):
        file_path = self.test_dir + '/download_{}'.format(uuid.uuid4())

        with pytest.raises(S3ClientException) as context:
            s3_client.download_file(TEST_BUCKET, 'not/a/key.tif', file_path)

        assert 'Not Found' in str(context.value)

    def test_valid_s3_bucket_valid_key_invalid_destination_file_raises(self):
        with pytest.raises(S3ClientException) as context:
            s3_client.download_file(TEST_BUCKET, self.test_file_key, '/not/a/path')

        assert 'No such file' in str(context.value)
