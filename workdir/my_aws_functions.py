import boto3
from botocore.errorfactory import ClientError
import config


def list_buckets():
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)


def list_objects(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.all():
        print(obj.key)


def download_object(bucket_name, object_name):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).download_file(object_name, object_name)


def download_object_to(bucket_name, object_name, local_file_name):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, object_name, local_file_name)


def download_model(version):
    download_object_to(
        config.MODEL_BUCKET,
        f'{config.MODEL_VERSION_PATH}{version}/{config.MODEL_NAME}',
        f'{config.LOCAL_WORK_FOLDER}{config.MODEL_NAME}')
    download_object_to(
        config.MODEL_BUCKET,
        f'{config.MODEL_VERSION_PATH}{version}/{config.MODEL_NAME}.examples',
        f'{config.LOCAL_WORK_FOLDER}{config.MODEL_NAME}.examples')


def upload_object_to(local_file_name, bucket_name, object_name):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(local_file_name, bucket_name, object_name)


def upload_model(version):
    upload_object_to(
        f'{config.LOCAL_WORK_FOLDER}{config.MODEL_NAME}',
        config.MODEL_BUCKET,
        f'{config.MODEL_VERSION_PATH}{version}/{config.MODEL_NAME}')
    upload_object_to(
        f'{config.LOCAL_WORK_FOLDER}{config.MODEL_NAME}.examples',
        config.MODEL_BUCKET,
        f'{config.MODEL_VERSION_PATH}{version}/{config.MODEL_NAME}.examples')


def upload_object(bucket_name, object_name):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).upload_file(object_name, object_name)


def check_for_object(bucket_name, object_name):
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=bucket_name, Key=object_name)
        return True
    except ClientError as e:
        # Not found
        if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
            return False
        else:
            raise


def check_for_model(version):
    return check_for_object(config.MODEL_BUCKET, f'{config.MODEL_VERSION_PATH}{version}/{config.MODEL_NAME}')


def create_bucket(bucket_name):
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=bucket_name)


if __name__ == "__main__":
    list_buckets()

