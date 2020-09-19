# generate files and upload to S3
# alternate between using consumer API and message queue to give file metadata

import boto3
import logging
import redis
import requests
import time

CONSUMER_URL = 'http://127.0.0.1:6000/process-file/'
PRODUCE_WAIT_TIME = 60  # seconds
PUBLISH_CHANNEL = 'file_metadata_queue'
S3_BUCKET_NAME = 'tc-app-integration-testing'
S3_KEY_NAME = 'omar_testing/'

redis_client = redis.Redis('localhost')
logger = logging.getLogger(__file__)


class TransferStrategy:
    def __init__(self):
        self._state = False
        self._payload = None

    def rest_api_strategy(self):
        try:
            r = requests.post(CONSUMER_URL, json=self._payload)
            r.raise_for_status()
            logger.info('Successfully submitted file processing request through consumer API')
        except requests.exceptions.RequestException as e:
            logger.error('Problem in reaching out to consumer API', e)

    def message_queue_strategy(self):
        redis_client.publish(PUBLISH_CHANNEL, self._payload)

    def send_for_processing(self, file_name):
        self._payload = {
            'file_name': file_name,
            'bucket_name': S3_BUCKET_NAME,
            'key_name': S3_KEY_NAME
        }
        if self._state:
            logger.info('Calling consumer API: {}', CONSUMER_URL)
            self.rest_api_strategy()
        else:
            logger.info('Publishing the file metadata on the channel: {}', PUBLISH_CHANNEL)
            self.message_queue_strategy()
        self._state = not self._state


def upload_file_to_s3(file_name):
    s3_client = boto3.client('s3')
    try:
        logger.info('Uploading file to S3: {}', file_name)
        s3_client.upload_file(file_name, S3_BUCKET_NAME, S3_KEY_NAME + file_name)
        return True
    except Exception as err:
        logger.error('Problem in uploading file to S3', err)
        return False


def generate_file():
    file_name = r'C:\Users\omar9\Desktop\tika_drf_s3.png'
    logger.info('Generated file: {}', file_name)
    return file_name


def produce():
    logger.info('Starting producer...')
    transfer_strategy = TransferStrategy()
    while True:
        file_name = generate_file()
        is_file_uploaded = upload_file_to_s3(file_name)
        if is_file_uploaded:
            transfer_strategy.send_for_processing(file_name)
        time.sleep(PRODUCE_WAIT_TIME)


if __name__ == '__main__':
    produce()
