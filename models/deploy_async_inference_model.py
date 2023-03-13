from time import gmtime, strftime

from sagemaker.async_inference.async_inference_config import AsyncInferenceConfig
from sagemaker.huggingface.model import HuggingFaceModel


def deploy_async_inf_model(model_s3_path, role, size):
    date = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    model_name = f"bea-whisper-async-inf-{size}-{date}"
    print(f"Model name will be: {model_name} using code {model_s3_path}")
    huggingface_model = HuggingFaceModel(
        model_data=model_s3_path,
        role=role,
        transformers_version="4.17",
        pytorch_version="1.10",
        py_version="py38",
    )
    async_config = AsyncInferenceConfig(
        output_path="s3://sagemaker-us-west-2-414059859629/whisper/output",  # Where our results will be stored
    )
    huggingface_model.deploy(
        initial_instance_count=1,
        instance_type="ml.g4dn.xlarge",
        endpoint_name=model_name,
        async_inference_config=async_config,
    )
    return model_name
