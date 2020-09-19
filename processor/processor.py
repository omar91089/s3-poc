# get file from S3
# process the file
# use message queue to give back processed file metadata

import boto3
import redis


PROCESSOR_URL = 'http://127.0.0.1:5000/submit_status/'
PUBLISH_CHANNEL = 'file_status_queue'


def get_file_from_s3(file_name, bucket_name, key_name):
    pass


def process_file(file_name, bucket_name, key_name):
    get_file_from_s3(file_name, bucket_name, key_name)


def consume():
    pass


if __name__ == '__main__':
    consume()
