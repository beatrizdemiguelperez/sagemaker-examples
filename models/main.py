import argparse
import time

import boto3
import sagemaker
from deploy_async_inference_model import deploy_async_inf_model
from deploy_serverless_model import deploy_serverless_model
from upload_model_s3 import upload_model_s3

"""
Take a TSV file with texts and return the analysis
where texts are tagged with a negativity score
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--size", help="Whisper model size", type=str, required=True
    )
    parser.add_argument(
        "-d",
        "--deployment",
        help="Wether to deploy with async or serverless inference",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    # Setup
    client = boto3.client(service_name="sagemaker")
    runtime = boto3.client(service_name="sagemaker-runtime")
    sagemaker_session = sagemaker.Session()
    role = sagemaker.get_execution_role()
    model_s3_path = upload_model_s3(sagemaker_session.default_bucket(), args.size)

    if args.deployment is "serverless":
        model_name = deploy_serverless_model(model_s3_path, role, args.size)
    else:
        model_name = deploy_async_inf_model(model_s3_path, role, args.size)

    # Monitor creation
    describe_endpoint_response = client.describe_endpoint(EndpointName=model_name)
    while describe_endpoint_response["EndpointStatus"] == "Creating":
        describe_endpoint_response = client.describe_endpoint(EndpointName=model_name)
        print(describe_endpoint_response["EndpointStatus"])
        time.sleep(15)
    print(describe_endpoint_response)
