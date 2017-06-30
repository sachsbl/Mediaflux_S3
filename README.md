# mediaflux-s3-client

The purpose of this library is to provide a common client for both AWS and Mediaflux flavors of S3.
http://www.arcitecta.com/Products/Mediaflux

It uses monkey-patching to work around an issue with ContentLength headers containing commas in Mediaflux. 
Other operations may work and can be accessed via interacting with the underlying boto3 client directly.  No guarantees.

A full functional-test suite is included for the three wrapped operations (download_file, upload_file, list_objects).
The test suite requires some specific setup which I tried to document in the test suite.  You need AWS and Mediaflux test environments for this to work. 

This package currently supports Python 3.5.  Other versions may work but are not supported.

Collecting the library in your app 
-----
```shell
pip install git+https://github.com/sachsbl/Mediaflux-S3.git@master
```
To statically vendor the client, use the wheel provided in the wheel folder.

Basic Usage
-----
```python
from python_s3_client.s3_client import S3Client, S3ClientException

# for AWS S3
aws_s3_client = S3Client(aws_access_key_id='key', aws_secret_access_key='secret_key')

# for Mediaflux S3
mediaflux_s3_client = S3Client(aws_access_key_id='key', aws_secret_access_key='secret_key',
                     endpoint='http://mediaflux-server', mediaflux=True)
                     
try:
  # list objects, similar to boto3 list_objects_v2
  mediaflux_s3_client.list_objects('my_bucket')

  # upload file
  mediaflux_s3_client.upload_file('/local/path', 'destination_bucket', 'destination_key')

  # download file
  mediaflux_s3_client.download_file('my_bucket', 'my_key', 'destination/file')
  
  #access underlying boto3 client directly (all functionality available, no guarantees it works and no exception wrapping)
  mediaflux_s3_client.s3_client.get_object(Bucket='bucket', Key='key')
  
  

except S3ClientException as s3_error:
    #handle wrapped cient error
except Exception as e:
    #handle unexpected exception

```
