import json
import logging
from typing import List, Dict

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_openai import AzureOpenAIEmbeddings

from config import config
from vector_search import get_search_results


class AISearchRetriever(BaseRetriever):
    """Langchain 'Tool' for Azure Cognitive Search results"""

    name = "search knowledge base"
    description = "search documents in search engine"

    indexes: List[str] = []
    semantic: bool = True
    k: int = 50
    reranker_th: float = 1.35
    similarity_k: int = 3
    extra_fields: Dict[str, List[str]] = {}
    embedding_model: str = config["EMBEDDING_MODEL"]

    def __init__(self, indexes: List[str] = [], k: int = 50, similarity_k: int = 7, reranker_th: float = 1.35,
                 semantic: bool = True, extra_fields: Dict[str, List[str]] = {},
                 embedding_model: str = config["EMBEDDING_MODEL"], **kwargs):
        super().__init__(**kwargs)
        self.indexes = indexes
        self.k = k
        self.reranker_th = reranker_th
        self.similarity_k = similarity_k
        self.semantic = semantic
        self.extra_fields = extra_fields
        self.embedding_model = embedding_model

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:

        ordered_results = self.get_search_results(query)
        # Just take key 'chunk' from these results
        ordered_results = [doc['chunk'] for doc in ordered_results]
        docs = []
        logging.info(f"Retrieved {len(docs)} documents")
        for doc in ordered_results:
            logging.debug(str(doc))
            docs.append(Document(page_content=str(doc)))
        return docs


    def get_search_results(self, query: str):
        embedder = AzureOpenAIEmbeddings(azure_endpoint=config["AZURE_OPENAI_ENDPOINT"],
                                         deployment=self.embedding_model, chunk_size=1,
                                         openai_api_key=config["AZURE_OPENAI_API_KEY"])

        # Search in all vector-based indexes available
        ordered_results = get_search_results(query, indexes=self.indexes, k=self.k,
                                             reranker_threshold=self.reranker_th,
                                             vector_search=False,
                                             similarity_k=self.similarity_k,
                                             query_vector=embedder.embed_query(query),
                                             extra_fields=self.extra_fields,
                                             semantic=self.semantic
                                             )
        ordered_results = self.clean_results(ordered_results)
        print(ordered_results)
        return ordered_results

    def clean_results(self, ordered_results: Dict) -> List[dict]:
        """Clean the results and return a string."""
        results = []
        i = 0
        for key in ordered_results:
            i = i + 1
            item = ordered_results[key]
            results.append({
                'id': str(i),
                'title': item["title"],
                'location': item["url"],
                'chunk': item["chunk"],
                'caption': item["caption"],
            })
        return results
