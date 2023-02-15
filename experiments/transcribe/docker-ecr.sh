ECR_REPOSITORY=sagemaker-processing-container
ACCOUNT_ID=414059859629
TAG=:latest
REPO_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY$TAG"

docker build -t $ECR_REPOSITORY docker
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
aws ecr create-repository --repository-name $ECR_REPOSITORY
docker tag $ECR_REPOSITORY$TAG $REPO_URI
docker push $REPO_URI