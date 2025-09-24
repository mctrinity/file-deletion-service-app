import boto3
from botocore.config import Config
from .config import settings


def _boto_client():
    # Works with env creds, shared config/role, or task role if running on ECS
    kwargs = {
        "region_name": settings.AWS_REGION,
        "config": Config(retries={"max_attempts": 3}),
    }
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        kwargs.update(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
    return boto3.client("s3", **kwargs)


def delete_object(bucket: str, key: str):
    if not bucket or not key:
        raise ValueError("bucket and key are required")
    s3 = _boto_client()
    # Head first to return 404 if missing (nicer error than silent delete)
    s3.head_object(Bucket=bucket, Key=key)
    s3.delete_object(Bucket=bucket, Key=key)
    return {"bucket": bucket, "key": key}
