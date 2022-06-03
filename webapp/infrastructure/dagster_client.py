from __future__ import annotations

from dagster_graphql import DagsterGraphQLClient, DagsterGraphQLClientError
from document_processing import utils


def default_client() -> DagsterGraphQLClient:
    """
    This returns a preconfigured DagsterGraphQLClient instance and is designed to fall back to dev
    envirnoment defaults if not configured.

    :return: The configured client instance
    """
    return DagsterGraphQLClient(
        utils.env(str, "GRAPHQL_HOST", default="dagster-dagit"),
        utils.env(int, "GRAPHQL_PORT", default=3000),
    )


class DagsterClient:
    _client: DagsterGraphQLClient

    def __init__(self, client=default_client()):
        self._client = client

    def trigger_run(
        self,
        job_name: str,
        repository_location_name: str,
        repository_name: str,
        run_config: dict,
        mode: str = "default",
    ) -> None:
        try:
            new_run_id: str = self.graphql_client.submit_pipeline_execution(
                job_name,
                repository_location_name=repository_location_name,
                repository_name=repository_name,
                run_config=run_config,
                mode=mode,
            )

            return new_run_id
        except DagsterGraphQLClientError as exc:
            raise exc
