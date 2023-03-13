import argparse
import time

import boto3
import sagemaker
from deploy_async_inference_model import deploy_async_inf_model
from deploy_serverless_model import deploy_serverless_model
from upload_model_s3 import upload_model_s3


def deploy(deployment, size):
    # Setup
    client = boto3.client(service_name="sagemaker")
    sagemaker_session = sagemaker.Session()
    role = sagemaker.get_execution_role()
    model_s3_path = upload_model_s3(sagemaker_session.default_bucket(), size)

    if deployment is "serverless":
        model_name = deploy_serverless_model(model_s3_path, role, size)
    else:
        model_name = deploy_async_inf_model(model_s3_path, role, size)

    # Monitor creation
    describe_endpoint_response = client.describe_endpoint(EndpointName=model_name)
    while describe_endpoint_response["EndpointStatus"] == "Creating":
        describe_endpoint_response = client.describe_endpoint(EndpointName=model_name)
        print(describe_endpoint_response["EndpointStatus"])
        time.sleep(15)
    print(describe_endpoint_response)
    return model_name
