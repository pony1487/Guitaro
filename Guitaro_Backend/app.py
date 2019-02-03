from flask import Flask, jsonify
import guitaroconfig
import boto3, botocore

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


@app.route('/download')
def download():
    wav_name = "E_E_A_G_E_Lesson.wav"
    try:
        obj = s3.get_object(Bucket=guitaroconfig.S3_BUCKET, Key=wav_name)
        return str(obj.get("Body"))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
