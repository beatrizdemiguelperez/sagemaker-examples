#!/usr/bin/env python3
import pathlib

import boto3
import sagemaker
from sagemaker.pytorch.processing import PyTorchProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput

INPUT_BUCKET = "sandbox-pdx-414059859629-voiceai-lab-inputs"
OUTPUT_BUCKET = "sandbox-pdx-414059859629-voiceai-lab-output-artifacts"
PROFILE_NAME = "user1"
ROLE_NAME = "pdx-sandbox-voiceai-sm-execution-role"
PREFIX = "sentiment-test/"

session = boto3.session.Session()
sts = session.client("sts")
account_number = sts.get_caller_identity().get("Account")
role = f"arn:aws:iam::{account_number}:role/{ROLE_NAME}"
sagemaker_session = sagemaker.Session(boto_session=session, default_bucket=OUTPUT_BUCKET)

print(f"%%%% Default bucket is: {sagemaker_session.default_bucket()}")

# Initialize the PyTorchProcessor
pytorch_processor = PyTorchProcessor(
    framework_version="1.8",
    role=role,
    instance_type="ml.t3.medium",
    instance_count=1,
    base_job_name="sentiment-processing-job",
    sagemaker_session=sagemaker_session,
    code_location=f"s3://{OUTPUT_BUCKET}"
)

# Run the processing job
pytorch_processor.run(
    code="evaluate.py",
    source_dir=str(pathlib.Path(__file__).parent / "evaluation_process_scripts"),
    inputs=[
        ProcessingInput(
            input_name="data",
            source=f"s3://{INPUT_BUCKET}/{PREFIX}",
            destination="/opt/ml/processing/input",
        )
    ],
    outputs=[
        ProcessingOutput(
            output_name="validation",
            source="/opt/ml/processing/valid",
            destination=f"s3://{OUTPUT_BUCKET}/{PREFIX}",
        ),
    ],
    arguments=["-i", "/opt/ml/processing/input/test.csv", "-o", "/opt/ml/processing/valid/output_test.csv"],
)

pytorch_processor.jobs[-1].describe()