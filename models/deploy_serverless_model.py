from time import gmtime, strftime

from sagemaker.huggingface.model import HuggingFaceModel
from sagemaker.serverless import ServerlessInferenceConfig


def deploy_serverless_model(model_s3_path, role, size):
    date = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    model_name = f"bea-whisper-serverless-{size}-{date}"
    print(f"Model name will be: {model_name} using code {model_s3_path}")
    huggingface_model = HuggingFaceModel(
        model_data=model_s3_path,
        role=role,
        transformers_version="4.17",
        pytorch_version="1.10",
        py_version="py38",
        model_server_workers=1,
    )
    # Specify MemorySizeInMB and MaxConcurrency in the serverless config object
    serverless_config = ServerlessInferenceConfig(
        memory_size_in_mb=6144,
        max_concurrency=10,
    )

    # deploy the endpoint endpoint
    huggingface_model.deploy(
        serverless_inference_config=serverless_config,
        endpoint_name=model_name,
    )
    return model_name
