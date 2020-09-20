# get file from S3
# process the file
# alternate between using generator API and message queue to give back processed file metadata

import json
import logging
import requests
import sys

from lib.redis import RedisSingleton
from lib.s3 import get_file_from_s3, upload_file_to_s3


GENERATOR_URL = 'http://127.0.0.1:5000/submit_status'
PUBLISH_CHANNEL = 'file_status_queue'
SUBSCRIBE_CHANNEL = 'file_metadata_queue'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class TransferStrategy:
    def __init__(self):
        self._state = False
        self._payload = None

    def rest_api_strategy(self):
        try:
            r = requests.post(GENERATOR_URL, json=self._payload)
            r.raise_for_status()
            logger.info('Successfully submitted back processed file through generator API')
        except requests.exceptions.RequestException as err:
            logger.error('Problem in reaching out to generator API', err)

    def message_queue_strategy(self):
        num = RedisSingleton.get_instance().publish(PUBLISH_CHANNEL, json.dumps(self._payload))
        logger.info('File status delivered to subscribers: %s', num)

    def send_processed_file(self, file_name, bucket_name, key_name):
        self._payload = {
            'file_name': file_name,
            'status': 'PROCESSED'
        }
        if self._state:
            logger.info('Calling generator API: %s', GENERATOR_URL)
            self.rest_api_strategy()
        else:
            logger.info('Publishing the file status on the channel: %s', PUBLISH_CHANNEL)
            self.message_queue_strategy()
        self._state = not self._state


def process_file(file_name, bucket_name, key_name):
    get_file_from_s3(file_name, bucket_name, key_name, logger)
    # processing logic here
    upload_file_to_s3(file_name, bucket_name, key_name, logger)


def main():
    logger.info('Starting processor message queue...')
    r = RedisSingleton.get_instance()
    queue = r.pubsub()
    queue.subscribe(SUBSCRIBE_CHANNEL)

    transfer_strategy = TransferStrategy()
    while True:
        message = queue.get_message()
        if not message:
            continue

        logger.info('Received message from generator: %s', message)
        try:
            json_data = json.loads(message['data'])
            file_name = json_data.get('file_name')
            bucket_name = json_data.get('bucket_name')
            key_name = json_data.get('key_name')

            process_file(file_name, bucket_name, key_name)
            transfer_strategy.send_processed_file(file_name, bucket_name, key_name)
        except TypeError as err:
            logger.info('Message could not be loaded as JSON')


if __name__ == '__main__':
    main()
