

#!/usr/bin/env python3
import pathlib

import boto3
import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput


print(f"%%%% Sagemaker Version is: {sagemaker.__version__}")

INPUT_BUCKET = "sandbox-pdx-414059859629-voiceai-lab-inputs"
OUTPUT_BUCKET = "sandbox-pdx-414059859629-voiceai-lab-output-artifacts"
PROFILE_NAME = "user1"
ROLE_NAME = "pdx-sandbox-voiceai-sm-execution-role"
PREFIX = "low-confidence/"

session = boto3.session.Session()
sts = session.client("sts")
account_number = sts.get_caller_identity().get("Account")
role = f"arn:aws:iam::{account_number}:role/{ROLE_NAME}"
sagemaker_session = sagemaker.Session(boto_session=session, default_bucket=OUTPUT_BUCKET)
processing_repository_uri = "414059859629.dkr.ecr.us-west-2.amazonaws.com/sagemaker-processing-container"
print(f"%%%% Default bucket is: {sagemaker_session.default_bucket()}")

# Initialize the ScriptProcessor
script_processor = ScriptProcessor(
    # Your script that kicks off the program.
    command=["python3"],
    image_uri=processing_repository_uri,
    role=role,
    instance_count=1,
    instance_type="ml.m5.xlarge",
    base_job_name="whisper-processing-job",
    sagemaker_session=sagemaker_session,
)

# Run the processing job
script_processor.run(
    code="whisper_process_scripts/evaluate.py",
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
            destination=f"s3://{OUTPUT_BUCKET}/{PREFIX}output",
        ),
    ],
    arguments=["-i", "/opt/ml/processing/input", "-o", "/opt/ml/processing/valid"],
)

script_processor.jobs[-1].describe()