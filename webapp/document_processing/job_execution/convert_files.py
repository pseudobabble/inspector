from typing import Set


def job_execution(file_keys: Set[str]) -> dict:
    return {
        "job_name": "convert_files_to_text",
        "repository_location_name": "dagster-ucd-document-processing",
        "repository_name": "__repository__convert_files_to_text",
        "run_config": {
            "ops": {"get_file_keys": {"config": {"keys": [*file_keys]}}},
            "resources": {
                "blob_client": {
                    "config": {
                        "url": ""
                    }
                },
                "tika_client": {
                    "config": {
                        "host": "tika",
                        "port": "9998"
                    }
                },
            },
        },
        "mode": "default",
    }
