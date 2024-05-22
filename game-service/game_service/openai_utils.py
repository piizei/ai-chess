import os

from openai.lib.azure import AzureOpenAI


def get_openai(instance_id: str = "1"):
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY" + instance_id),
        api_version="2024-02-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT" + instance_id)
    )
