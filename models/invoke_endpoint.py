import json

import boto3


def invoke_endpoint(endpoint_name, request_body):
    runtime_client = boto3.client("sagemaker-runtime")
    content_type = "application/json"
    data = json.loads(json.dumps(request_body))
    payload = json.dumps(data)

    response = runtime_client.invoke_endpoint(
        EndpointName=endpoint_name, ContentType=content_type, Body=payload
    )
    result = json.loads(response["Body"].read().decode())["Output"]
    print(result)
    return result
