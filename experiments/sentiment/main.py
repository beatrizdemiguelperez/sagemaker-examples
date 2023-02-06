#!/usr/bin/env python3
import pathlib

import boto3
import sagemaker
from sagemaker.pytorch.processing import PyTorchProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput

BUCKET = "sandbox-pdx-414059859629-voiceai-lab-datalake"
PROFILE_NAME = "user1"
ROLE_NAME = "pdx-sandbox-voiceai-sm-execution-role"
PREFIX = "sentiment-test/"

session = boto3.session.Session(profile_name=PROFILE_NAME)
sts = session.client("sts")
account_number = sts.get_caller_identity().get("Account")
role = f"arn:aws:iam::{account_number}:role/{ROLE_NAME}"
sagemaker_session = sagemaker.Session(boto_session=session)

# Initialize the PyTorchProcessor
pytorch_processor = PyTorchProcessor(
    framework_version="1.8",
    role=role,
    instance_type="ml.m5.xlarge",
    instance_count=1,
    base_job_name="frameworkprocessor-PT",
    sagemaker_session=sagemaker_session,
)

# Run the processing job
pytorch_processor.run(
    code="evaluate.py",
    source_dir=str(pathlib.Path(__file__).parent / "evaluation_process_scripts"),
    inputs=[
        ProcessingInput(
            input_name="data",
            source=f"s3://{BUCKET}/{PREFIX}",
            destination="/opt/ml/processing/input",
        )
    ],
    outputs=[
        ProcessingOutput(
            output_name="validation",
            source="/opt/ml/processing/valid",
            destination=f"s3://{BUCKET}/{PREFIX}",
        ),
    ],
    arguments=["-i", "/opt/ml/processing/input/test.csv", "-o", "/opt/ml/processing/valid/output_test.csv"],
)

pytorch_processor.jobs[-1].describe()