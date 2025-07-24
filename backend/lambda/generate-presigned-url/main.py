import json
import os
import boto3
import uuid

s3 = boto3.client("s3")
BUCKET_NAME = os.environ["BUCKET_NAME"]

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        filename = body.get("filename")
        content_type = body.get("contentType")

        if not filename or not content_type:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing filename or contentType"})
            }

        key = f"{uuid.uuid4()}_{filename}"

        presigned_url = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": key,
                "ContentType": content_type
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"uploadUrl": presigned_url, "key": key})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error generating URL", "error": str(e)})
        }

