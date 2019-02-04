import guitaroconfig
import boto3, botocore
import json


class S3Manager:
    """
    NOT USED
    """
    def __init__(self, bucket):
        self.bucket = bucket
        self.aws_access_key_id = guitaroconfig.S3_KEY
        self.aws_secret_access_key = guitaroconfig.S3_SECRET
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

    def listallbuckets(self):
        """
        :return: returns a list of dicts containing name and creation date for each bucket
        """
        response = self.s3.list_buckets()
        return response.get("Buckets")

    def get_lesson(self, bucket_name):
        """
        :param bucket_name: Unique name of the S3 Bucket
        :return: Bucket object
        """
        response = self.s3.list_buckets()
        bucket_list = response.get("Buckets")
        for bucket in bucket_list:
            if bucket.get("Name") == bucket_name:
                return bucket
        return "No bucket found"

    def test_directory(self):
        response = self.s3.list_objects(Bucket=self.bucket, Delimiter="/",Prefix="Plan/Beginner")
        return str(response)



    def get_tab(self):
        pass

    def get_chord_diagram(self):
        pass
