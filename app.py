from flask import Flask, request, send_file
import boto3
import os

app = Flask(__name__)

# Upload to S3
@app.route('/upload', methods=['POST'])
def upload_to_s3():
    aws_access_key = request.form['aws_access_key']
    aws_secret_key = request.form['aws_secret_key']
    bucket_name = request.form['bucket_name']
    file = request.files['file']

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )
    s3.upload_fileobj(file, bucket_name, file.filename)

    return f"File {file.filename} uploaded successfully!"

# Download from S3
@app.route('/download', methods=['POST'])
def download_from_s3():
    aws_access_key = request.form['aws_access_key']
    aws_secret_key = request.form['aws_secret_key']
    bucket_name = request.form['bucket_name']
    filename = request.form['filename']

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )

    local_filename = f"/tmp/{filename}"
    s3.download_file(bucket_name, filename, local_filename)

    return send_file(local_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
