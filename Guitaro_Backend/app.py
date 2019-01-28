from flask import Flask, jsonify
import guitaroconfig
import boto3

app = Flask(__name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id=guitaroconfig.S3_KEY,
    aws_secret_access_key=guitaroconfig.S3_SECRET
)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/listbucketcontents')
def test_debug():
    response = s3.list_buckets()
    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run()
