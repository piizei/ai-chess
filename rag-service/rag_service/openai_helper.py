from typing import List

from langchain_openai.chat_models import AzureChatOpenAI

from config import config


def get_llm(max_tokens: int = int(config["LLM_MAX_TOKENS"]), deployment: str = config["AZURE_OPENAI_DEPLOYMENT_NAME"],
            streaming: bool = True, verbose: bool = True, callbacks: List = [],
            callback_manager: any = None) -> AzureChatOpenAI:
    return AzureChatOpenAI(
        deployment_name=deployment,
        openai_api_version=config["AZURE_OPENAI_API_VERSION"],
        openai_api_key=config["AZURE_OPENAI_API_KEY"],
        max_tokens=max_tokens,
        streaming=streaming,
        verbose=verbose,
        callbacks=callbacks,
        callback_manager=None,

    )
