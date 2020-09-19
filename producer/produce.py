# generate files and upload to S3
# alternate between using consumer API and message queue to give file metadata

import boto3
import logging
import redis
import requests
import time

CONSUMER_URL = 'http://localhost/process-file/'
PRODUCE_WAIT_TIME = 60  # seconds
S3_BUCKET_NAME = 'tc-app-integration-testing'
S3_KEY_NAME = 'omar_testing/'

redis_client = redis.Redis()
logger = logging.getLogger(__file__)


class TransferStrategy:
    def __init__(self):
        self._state = False

    def rest_api_strategy(self):
        r = requests.post(CONSUMER_URL)

    def message_queue_strategy(self):
        redis_client.publish()

    def send_for_processing(self, file_name):
        if self._state:
            self.rest_api_strategy()
        else:
            self.message_queue_strategy()
        self._state = not self._state


def upload_file_to_s3(file_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, S3_BUCKET_NAME, S3_KEY_NAME + file_name)
    except Exception as err:
        logger.error('Problem in uploading file to S3', err)


def generate_file():
    file_name = r'C:\Users\omar9\Desktop\tika_drf_s3.png'
    return file_name


def send_for_processing(file_name):
    pass


def produce():
    transfer_strategy = TransferStrategy()
    while True:
        file_name = generate_file()
        upload_file_to_s3(file_name)
        transfer_strategy.send_for_processing(file_name)
        time.sleep(PRODUCE_WAIT_TIME)


if __name__ == '__main__':
    produce()
