# get file from S3
# process the file
# alternate between using generator API and message queue to give back processed file metadata

import json
import logging
import redis

from common.s3_utils import get_file_from_s3, upload_file_to_s3


PROCESSOR_URL = 'http://127.0.0.1:5000/submit_status/'
PUBLISH_CHANNEL = 'file_status_queue'

logger = logging.getLogger(__file__)
r = redis.Redis('localhost')
queue = r.pubsub()
queue.subscribe('file_metadata_queue')


def process_file(file_name, bucket_name, key_name):
    get_file_from_s3(file_name, bucket_name, key_name, logger)
    # processing logic here
    upload_file_to_s3(file_name, bucket_name, key_name, logger)
    

def consume():
    logger.info('Starting processor message queue...')
    while True:
        message = queue.get_message()
        logger.info('Received message from generator: %s', message)
        json_data = json.loads(message)
        file_name = json_data.get('file_name')
        bucket_name = json_data.get('bucket_name')
        key_name = json_data.get('key_name')
        process_file(file_name, bucket_name, key_name)


if __name__ == '__main__':
    consume()
