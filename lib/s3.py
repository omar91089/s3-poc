import boto3


def get_file_from_s3(file_name, bucket_name, key_name, logger):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    try:
        bucket.download_file(key_name + file_name, file_name)
    except Exception as err:
        logger.error('Problem in downloading file from S3', err)


def upload_file_to_s3(file_name, bucket_name, key_name, logger):
    s3_client = boto3.client('s3')
    try:
        logger.info('Uploading file to S3: %s', file_name)
        s3_client.upload_file(file_name, bucket_name, key_name + file_name)
        return True
    except Exception as err:
        logger.error('Problem in uploading file to S3', err)
        return False
