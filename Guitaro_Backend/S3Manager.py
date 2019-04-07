import guitaroconfig
import boto3, botocore.exceptions
from os import path


class S3Manager:
    """
    The chord images that are stored in S3 were generated from here https://chordpix.com/
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

        self.base_path = path.dirname(__file__)
        self.base_path = path.join(self.base_path, "chord_images")

    def listallbuckets(self):
        """
        :return: returns a list of dicts containing name and creation date for each bucket
        """
        response = self.s3.list_buckets()
        return response.get("Buckets")

    def get_chord_diagram(self,chord_name):
        try:
            self.s3.download_file(self.bucket, chord_name, self.base_path + "/" + chord_name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise


