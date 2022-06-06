from typing import Set


def job_execution(document_ids: Set[int]) -> dict:
    return {
        "job_name": "preprocess_documents",
        "repository_location_name": "dagster-ucd-document-processing",
        "repository_name": "__repository__preprocess_documents",
        "run_config": {
            "ops": {"preprocess_docs": {"config": {"document_ids": [*document_ids]}}},
            "resources": {
                "document_store": {
                    "config": {
                        "url": "postgresql://webapp_postgres_user:webapp_postgres_password@webapp-postgres:5432/document_store"
                    }
                },
                "raw_documents_repository": {
                    "config": {"url": "http://webapp:8080/documents"}
                },
            },
        },
        "mode": "default",
    }
