ECR_REPOSITORY=sagemaker-custom
IMAGE_NAME_REPOSITORY_TAG=sagemaker-cmake
ACCOUNT_ID=414059859629
ROLE_NAME="pdx-sandbox-voiceai-sm-execution-role"

# LOGIN IN AWS ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
# CREATE ECR REPO IF IT DOESNT EXISTS
aws ecr describe-repositories --repository-names ${ECR_REPOSITORY} || aws ecr create-repository --repository-name ${ECR_REPOSITORY}

# PUBLISH IMAGE IN ECR
docker build docker -t ${IMAGE_NAME_REPOSITORY_TAG} -t ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_NAME_REPOSITORY_TAG}
docker push ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_NAME_REPOSITORY_TAG}


# CREATE SAGEMAKER IMAGE POINTING TO ALREADY CREATED ECR IMAGE
ROLE_ARN=arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}
aws --region ${REGION} sagemaker create-image \
    --image-name ${IMAGE_NAME_REPOSITORY_TAG} \
    --role-arn ${ROLE_ARN}

aws --region ${REGION} sagemaker create-image-version \
    --image-name ${IMAGE_NAME_REPOSITORY_TAG} \
    --base-image "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_NAME_REPOSITORY_TAG}"

# Verify the image-version is created successfully. Do NOT proceed if image-version is in CREATE_FAILED state or in any other state apart from CREATED.
aws --region ${AWS_REGION} sagemaker describe-image-version --image-name ${IMAGE_NAME_REPOSITORY_TAG}