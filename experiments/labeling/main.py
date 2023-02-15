#!/usr/bin/env python3
import boto3
import sagemaker

BUCKET = "sandbox-pdx-414059859629-voiceai-lab-inputs"
PROFILE_NAME = "user1"
ROLE_NAME = "pdx-sandbox-voiceai-sm-execution-role"
region = "us-west-2"
session = boto3.session.Session()
sts = session.client("sts")
account_id = sts.get_caller_identity().get("Account")
role = f"arn:aws:iam::{account_id}:role/{ROLE_NAME}"
LABELING_JOB_NAME = 'labeling-example-2'
OUTPUT_BUCKET = "sandbox-pdx-414059859629-voiceai-lab-output-artifacts"
PROFILE_NAME = "user1"
ROLE_NAME = "pdx-sandbox-voiceai-sm-execution-role"
WORKTEAM_ARN = "arn:aws:sagemaker:us-west-2:414059859629:workteam/private-crowd/voiceai-team"
INPUT_MANIFEST_S3_URI = "s3://sandbox-pdx-414059859629-voiceai-lab-inputs/labeling-test/dataset-20230215T113969.manifest"
OUTPUT_S3_PATH = f"s3://{OUTPUT_BUCKET}/labeling-test/dataset-20230215T113969.manifest"

# create label categories
s3 = boto3.client('s3')
s3.upload_file(Filename='labeling-config/categories.json', Bucket=BUCKET, Key='labeling-config/categories.json')
print(f"%%%% Created categories in s3 ")
LABEL_CATEGORIES_S3_URI = f's3://{OUTPUT_BUCKET}/labeling-config/categories.json'
# create template
s3.upload_file(Filename="labeling-config/template.html", Bucket=BUCKET, Key='labeling-config/template.html')
UI_TEMPLATE_S3_URI = f's3://{OUTPUT_BUCKET}/labeling-config/template.html'
print(f"%%%% Created template in s3 ")

createLabelingJob_request = {
  "LabelingJobName": LABELING_JOB_NAME,
  "HumanTaskConfig": {
    "AnnotationConsolidationConfig": {
      # selected from here https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_AnnotationConsolidationConfig.html#SageMaker-Type-AnnotationConsolidationConfig-AnnotationConsolidationLambdaArn
      "AnnotationConsolidationLambdaArn": f"arn:aws:lambda:{region}:{account_id}:function:ACS-TextMultiClassMultiLabel"
    },
    "MaxConcurrentTaskCount": 200,
    "NumberOfHumanWorkersPerDataObject": 1,
    # seleceted from here https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_HumanTaskConfig.html#SageMaker-Type-HumanTaskConfig-PreHumanTaskLambdaArn
    "PreHumanTaskLambdaArn": "arn:aws:lambda:us-west-2:081040173940:function:PRE-TextMultiClass",
    "TaskAvailabilityLifetimeInSeconds": 864000,
    "TaskDescription": "Classify text",
    "TaskKeywords": ["Text Classification","Labeling"],
    "TaskTimeLimitInSeconds": 800,
    "TaskTitle": LABELING_JOB_NAME,
    "UiConfig": {
      "UiTemplateS3Uri": UI_TEMPLATE_S3_URI
    },
    "WorkteamArn": WORKTEAM_ARN
  },
  "InputConfig": {
    "DataAttributes": {
      "ContentClassifiers": [
        "FreeOfPersonallyIdentifiableInformation",
        "FreeOfAdultContent"
      ]
    },
    "DataSource": {
      "S3DataSource": {
        "ManifestS3Uri": INPUT_MANIFEST_S3_URI
      }
    }
  },
  "LabelAttributeName": "Text",
  "LabelCategoryConfigS3Uri": LABEL_CATEGORIES_S3_URI,
  "OutputConfig": {
    "S3OutputPath": OUTPUT_S3_PATH
  },
  "RoleArn": role,
  "StoppingConditions": {
    "MaxPercentageOfInputDatasetLabeled": 100
  }
}
print(createLabelingJob_request)
sm_client = boto3.client('sagemaker')
out = sm_client.create_labeling_job(**createLabelingJob_request)
print(out)