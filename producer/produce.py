# generate files and upload to S3
# alternate between using consumer API and message queue to give file metadata

import boto3
import random
import time

WAIT_TIME = 60  # seconds


def upload_file_to_s3(file_name):
    s3_url = ''
    return s3_url


def generate_file():
    file_name = ''
    return file_name


def send_for_processing(file_name):
    pass


def produce():
    while True:
        file_name = generate_file()
        upload_file_to_s3(file_name)
        send_for_processing(file_name)
        time.sleep(WAIT_TIME)


if __name__ == '__main__':
    produce()
