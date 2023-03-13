import json
import uuid

import boto3


def s3_upload_file(json_data, bucket, key):
    s3 = boto3.resource("s3")
    s3object = s3.Object(bucket, key)
    s3object.put(Body=(bytes(json.dumps(json_data).encode("UTF-8"))))


def invoke_async_endpoint(endpoint_name, request_body):
    runtime_client = boto3.client("sagemaker-runtime")
    identifier = str(uuid.uuid4())
    bucket_name = "sagemaker-us-west-2-414059859629"
    key = f"whisper/inputs/{identifier}.json"
    # Upload input model file
    s3_upload_file(request_body, bucket_name, key)
    # Make async prediction
    response = runtime_client.invoke_endpoint_async(
        EndpointName=endpoint_name,
        InputLocation=f"s3://{bucket_name}/{key}",
        InferenceId=identifier,
        ContentType="application/json",
    )
    return response
