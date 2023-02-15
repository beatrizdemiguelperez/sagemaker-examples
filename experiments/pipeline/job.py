#!/usr/bin/env python3
import pathlib

import boto3
import sagemaker
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.pytorch.processing import PyTorchProcessor
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep

print(f"%%%% Sagemaker Version is: {sagemaker.__version__}")

INPUT_BUCKET = "sandbox-pdx-414059859629-voiceai-lab-inputs"
OUTPUT_BUCKET = "sandbox-pdx-414059859629-voiceai-lab-output-artifacts"
PROFILE_NAME = "user1"
ROLE_NAME = "pdx-sandbox-voiceai-sm-execution-role"
PREFIX = "sentiment-test/"

session = boto3.session.Session()
sts = session.client("sts")
account_number = sts.get_caller_identity().get("Account")
role = f"arn:aws:iam::{account_number}:role/{ROLE_NAME}"
sagemaker_session = sagemaker.Session(
    boto_session=session, default_bucket=OUTPUT_BUCKET
)
# processing_repository_uri = "809849379942.dkr.ecr.us-west-2.amazonaws.com/ci/python"
processing_repository_uri = (
    "414059859629.dkr.ecr.us-west-2.amazonaws.com/sagemaker-processing-container"
)

print(f"%%%% Default bucket is: {sagemaker_session.default_bucket()}")

script_processor = PyTorchProcessor(
    framework_version="1.8",
    role=role,
    instance_type="ml.t3.medium",
    instance_count=1,
    base_job_name="pipelines-processing-job",
    sagemaker_session=sagemaker_session,
    code_location=f"s3://{OUTPUT_BUCKET}",
)
processing_step_args_1 = script_processor.run(
    code="main.py",
    source_dir=str(pathlib.Path(__file__).parent / "scripts"),
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
            source="/opt/ml/processing/output",
            destination=f"s3://{OUTPUT_BUCKET}/{PREFIX}",
        ),
    ],
    arguments=[
        "-i",
        "/opt/ml/processing/input/test.csv",
        "-o",
        "/opt/ml/processing/output/output_step1.csv",
    ],
)
processing_step_args_2 = script_processor.run(
    code="main.py",
    source_dir=str(pathlib.Path(__file__).parent / "scripts"),
    inputs=[
        ProcessingInput(
            input_name="data",
            source=f"s3://{OUTPUT_BUCKET}/{PREFIX}",
            destination="/opt/ml/processing/input",
        )
    ],
    outputs=[
        ProcessingOutput(
            output_name="validation",
            source="/opt/ml/processing/output",
            destination=f"s3://{OUTPUT_BUCKET}/{PREFIX}",
        ),
    ],
    arguments=[
        "-i",
        "/opt/ml/processing/input/output_step1.csv",
        "-o",
        "/opt/ml/processing/output/output_step2.csv",
    ],
)
step_process1 = ProcessingStep(
    name="Preprocess1",
    step_args=processing_step_args_1,
)
step_process2 = ProcessingStep(
    name="Preprocess2",
    step_args=processing_step_args_2,
)
pipeline = Pipeline(
    name="pipeline_example",
    steps=[step_process1, step_process2],
    sagemaker_session=sagemaker_session,
)
execution = pipeline.start()
execution.describe()
execution.list_steps()
