from collections import OrderedDict
from typing import List, Dict

import json
import requests
from langchain_openai.embeddings import AzureOpenAIEmbeddings

from config import config

embedder = AzureOpenAIEmbeddings(azure_endpoint=config["AZURE_OPENAI_ENDPOINT"], deployment=config["EMBEDDING_MODEL"],
                                 chunk_size=1, openai_api_key=config["AZURE_OPENAI_API_KEY"])


def get_semantic_query(query: str, k: int = 50):
    return {
        "search": query,
        "queryType": "semantic",
        "semanticConfiguration": "my-semantic-config",
        "count": "true",
        "captions": "extractive",
        "answers": "extractive",
        "top": k
    }


# note removed the non-semantic query from here as it was not tested with the latest api version.

def get_search_results(query: str, indexes: list,
                       k: int = 5,
                       reranker_threshold: float = 1.5,
                       sas_token: str = "",
                       vector_search: bool = True,
                       similarity_k: int = 5,
                       semantic: bool = False,
                       filter: str = None,
                       extra_fields: Dict[str, List[str]] = {},
                       query_vector: list = []) -> List[dict]:
    headers = {'Content-Type': 'application/json', 'api-key': config["AZURE_SEARCH_KEY"]}
    params = {'api-version': config['AZURE_SEARCH_API_VERSION']}

    agg_search_results = dict()

    for index in indexes:
        # Don't use the k for semantic query, the reranker works best if you fetch 50 results and then filter
        # the best ones (k with reranker_threshold)
        search_payload = get_semantic_query(query, 50)
        search_payload["vectorQueries"] = [
            {"kind": "vector", "vector": query_vector, "fields": "contentVector", "k": k}]
        search_payload["select"] = "id, title, content, url"
        search_payload["semanticConfiguration"] = "default"

        if filter:
            search_payload['filter'] = filter

        if index in extra_fields:
            search_payload["select"] = search_payload["select"] + ", " + ','.join(extra_fields[index])

        resp = requests.post(config['AZURE_SEARCH_ENDPOINT'] + "/indexes/" + index + "/docs/search",
                             data=json.dumps(search_payload), headers=headers, params=params)

        search_results = resp.json()
        agg_search_results[index] = search_results
    content = dict()
    ordered_content = OrderedDict()

    for index, search_results in agg_search_results.items():
        if not 'value' in search_results:
            continue
        for result in search_results['value']:
            # Figure out if this is semantic search or not
            if '@search.rerankerScore' in result:
                if result['@search.rerankerScore'] < reranker_threshold:
                    continue
            else:
                if result['@search.score'] < 0.015:
                    continue

            caption = ""
            if '@search.captions' in result:
                caption = result['@search.captions'][0]['text']
            # add only if no other result with same title exists in content
            if not any(existing_result['title'] == result['title'] for existing_result in content.values()):
                content[result['id']] = {
                    "title": result['title'],
                    "chunk": result['content'],
                    "url": result['url'] + sas_token if result['url'] else "",
                    "caption": caption,
                    "index": index
                }
                if index in extra_fields:
                    for field in extra_fields[index]:
                        content[result['id']][field] = result[field]

                if vector_search:
                    content[result['id']]["score"] = result['@search.score']  # Uses the Hybrid RRF score
                else:
                    content[result['id']]["score"] = result['@search.rerankerScore']  # Uses the reranker score

    # After results have been filtered, sort and add the top k to the ordered_content
    #  Todo: needs to be rethinked with reranker
    topk = similarity_k

    count = 0  # To keep track of the number of results added
    for id in sorted(content, key=lambda x: content[x]["score"], reverse=True):
        ordered_content[id] = content[id]
        count += 1
        if count >= topk:
            break
    return ordered_content
