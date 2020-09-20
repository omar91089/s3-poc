# generate files and upload to S3
# alternate between using consumer API and message queue to give file metadata

import json
import logging
import requests
import sys
import time

from lib.redis import RedisSingleton
from lib.s3 import upload_file_to_s3

GENERATE_WAIT_TIME = 60  # seconds
PROCESSOR_URL = 'http://127.0.0.1:5001/process_file/'
PUBLISH_CHANNEL = 'file_metadata_queue'
SUBSCRIBE_CHANNEL = 'file_status_queue'
S3_BUCKET_NAME = 'tc-app-integration-testing'
S3_KEY_NAME = 'omar_testing/'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class TransferStrategy:
    def __init__(self):
        self._state = False
        self._payload = None
        self._redis = RedisSingleton.get_instance()

    def rest_api_strategy(self):
        try:
            r = requests.post(PROCESSOR_URL, json=self._payload)
            r.raise_for_status()
            logger.info('Successfully submitted file processing request through processor API')
        except requests.exceptions.RequestException as err:
            logger.error('Problem in reaching out to processor API', err)

    def message_queue_strategy(self):
        num = self._redis.publish(PUBLISH_CHANNEL, json.dumps(self._payload))
        logger.info('File metadata delivered to subscribers: %s', num)

    def send_for_processing(self, file_name):
        self._payload = {
            'file_name': file_name,
            'bucket_name': S3_BUCKET_NAME,
            'key_name': S3_KEY_NAME
        }
        if self._state:
            logger.info('Calling processor API: %s', PROCESSOR_URL)
            self.rest_api_strategy()
        else:
            logger.info('Publishing the file metadata on the channel: %s', PUBLISH_CHANNEL)
            self.message_queue_strategy()
        self._state = not self._state


def generate_file():
    file_name = 'mountains.jpg'
    logger.info('Generated file: %s', file_name)
    return file_name


def generate_and_transfer(transfer_strategy):
    file_name = generate_file()
    is_file_uploaded = upload_file_to_s3(file_name, S3_BUCKET_NAME, S3_KEY_NAME, logger)
    if is_file_uploaded:
        transfer_strategy.send_for_processing(file_name)


def process_queue_message(queue):
    message = queue.get_message()
    logger.info('Received message from generator: %s', message)

    json_data = json.loads(message)
    file_name = json_data.get('file_name')
    status = json_data.get('status')
    logger.info('File: %s, was processed with status: %s', file_name, status)


def main():
    logger.info('Starting generator and status message queue...')
    r = RedisSingleton.get_instance()
    queue = r.pubsub()
    queue.subscribe(SUBSCRIBE_CHANNEL)

    transfer_strategy = TransferStrategy()
    is_generate = True
    while True:
        if is_generate:
            generate_and_transfer(transfer_strategy)
            time.sleep(GENERATE_WAIT_TIME)
        else:
            process_queue_message(queue)


if __name__ == '__main__':
    main()
