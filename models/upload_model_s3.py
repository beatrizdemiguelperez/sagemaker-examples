import subprocess
from time import gmtime, strftime

import boto3


def make_tarfile(output_filename, source_dir):
    subprocess.call(["tar", "-C", source_dir, "-zcvf", output_filename, "."])


def upload_model_s3(bucket, size):
    # Setup
    boto_session = boto3.session.Session()
    s3 = boto_session.resource("s3")
    date = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    tar_filename = f"model-bea-whisper-{size}-{date}.tar.gz"
    model_folder = f"model-{size}"
    print(model_folder)
    make_tarfile(tar_filename, model_folder)

    # Upload tar.gz to bucket
    model_s3_path = f"s3://{bucket}/{tar_filename}"
    print(f"uploading tar.gz to bucket: {model_s3_path}")
    s3.meta.client.upload_file(tar_filename, bucket, tar_filename)
    return model_s3_path
