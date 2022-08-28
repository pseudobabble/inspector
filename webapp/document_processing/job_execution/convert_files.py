from typing import Set


def convert_files_to_text(
        file_keys: Set[str],
        blob_client_url: str,
        access_key: str,
        secret_key: str,
        tika_host: str,
        tika_port: str,
        tika_endpoint: str
) -> dict:
    return {
        "job_name": "convert_files_to_text",
        "repository_location_name": "dagster-ucd-document-processing",
        "repository_name": "__repository__convert_files_to_text",
        "run_config": {
            "ops": {
                "get_file_keys": {
                    "config": {
                        "keys": [*file_keys]
                    }
                }
            },
            "resources": {
                "blob_client": {
                    "config": {
                        "url": blob_client_url
                        "bucket_name": "files",
                        "access_key": access_key,
                        "secret_key": secret_key
                    }
                },
                "tika_client": {
                    "config": {
                        "host": tika_host,
                        "port": tika_port,
                        "endpoint": tika_endpoint
                    }
                },
            },
        },
        "mode": "default",
    }
