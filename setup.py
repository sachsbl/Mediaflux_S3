from setuptools import setup
setup(
    name='python-s3-client',
    packages=['python_s3_client'],
    version='0.1.0',
    author='Oculus',
    author_email='DL-GCS-Oculus@digitalglobe.com',
    description='Python client for interacting with both AWS and Mediaflux S3 services in an abstracted manner',
    url='https://github.digitalglobe.com/p20-20-common/python-s3-client',
    install_requires=['boto3', 'botocore'],
    tests_require=['pytest']
)
