import os
from dotenv import dotenv_values

default_envs = {
    "AZURE_SEARCH_INDEX": "default",
    "EMBEDDING_MODEL": "text-embedding-ada-002",
    "AZURE_SEARCH_API_VERSION": "2023-11-01"
}

default_envs_gpt4_32k = {
    "MODEL": "gpt-4-32k",
    "LLM_MAX_TOKENS": "4000",
    "CHUNK_SIZE": "20000",
    "CHUNK_OVERLAP": "1000",
    "MAP_REDUCE_DOCUMENT_CHUNK_SIZE": "5000"
}

default_envs_gpt4_o = {
    "MODEL": "gpt-4o",
    "LLM_MAX_TOKENS": "4000",
    "CHUNK_SIZE": "2000",
    "CHUNK_OVERLAP": "500",
    "MAP_REDUCE_DOCUMENT_CHUNK_SIZE": "5000"
}

default_envs_gpt3_4k = {
    "MODEL": "gpt-35-turbo",
    "LLM_MAX_TOKENS": "1000",
    "CHUNK_SIZE": "10000",
    "CHUNK_OVERLAP": "500",
    "MAP_REDUCE_DOCUMENT_CHUNK_SIZE": "3000"
}

default_envs_gpt3_16k = {
    "MODEL": "gpt-35-turbo-16k",
    "LLM_MAX_TOKENS": "4000",
    "CHUNK_SIZE": "16000",
    "CHUNK_OVERLAP": "500",
    "MAP_REDUCE_DOCUMENT_CHUNK_SIZE": "10000"
}

cosmos_config = {
    "MONGODB_CONNECTION_STRING": None
}


config = {
    **cosmos_config,
    **default_envs,
    **default_envs_gpt4_o,
    **dotenv_values(),
    **os.environ,  # override loaded values with environment variables
}

os.environ["AZURE_OPENAI_API_KEY"] = config["AZURE_OPENAI_API_KEY"]
os.environ["AZURE_OPENAI_API_VERSION"] = config["AZURE_OPENAI_API_VERSION"]
os.environ["OPENAI_API_TYPE"] = "azure"
