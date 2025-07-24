import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf']

# Fetch bucket name from env variable
UPLOAD_BUCKET = os.environ.get('UPLOAD_BUCKET')

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']

    logger.info(f"New file uploaded to: s3://{bucket_name}/{object_key}")

    if bucket_name != UPLOAD_BUCKET:
        logger.warning(f"Upload to unexpected bucket: {bucket_name}")
        return {
            'statusCode': 403,
            'body': f"File uploaded to unauthorized bucket: {bucket_name}"
        }

    if not is_valid_file_type(object_key):
        logger.warning(f"Invalid file type: {object_key}")
        return {
            'statusCode': 400,
            'body': f"Unsupported file type uploaded: {object_key}"
        }

    logger.info(f"Valid screenshot received: {object_key}")
    return {
        'statusCode': 200,
        'body': f"File {object_key} processed successfully."
    }

def is_valid_file_type(key):
    for ext in ALLOWED_EXTENSIONS:
        if key.lower().endswith(ext):
            return True
    return False
