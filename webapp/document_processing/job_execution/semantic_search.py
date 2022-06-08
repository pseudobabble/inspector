def run_config(retrieve_query, semantic_refine_query) -> dict:
    """
    Returns essentially a fixture job config
    """
    return {
        "ops": {
            "retrieve_candidates": {
                "config": {
                    "query": retrieve_query,
                    "top_k": 30,
                },
            },
            "semantic_refine_candidates": {
                "config": {
                    "query": semantic_refine_query,
                    "top_k": 2,
                }
            },
        },
        "resources": {
            "document_store": {
                "config": {
                    "url": "postgresql://webapp_postgres_user:webapp_postgres_password@webapp-postgres:5432/document_store"
                }
            },
            "reader": {
                "config": {
                    "model_name": "deepset/roberta-base-squad2",
                    "use_gpu": True,
                }
            },
            "answer_client": {
                "config": {
                    "url": "http://webapp:8080/hooks/semantic-search",
                }
            },
        },
    }
