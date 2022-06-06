from dagster_graphql import DagsterGraphQLClient, DagsterGraphQLClientError

from document_processing import utils


def default_client() -> DagsterGraphQLClient:
    """
    Returns a an instance of the configured DagsterGraphQLClient. Configuration is
    pulled from the GRAPHQL_HOST/GRAPHQL_PORT env vars, defaults to the dev environment
    defaults if the env vars are not set.

    :return: A preconfigured graphql client.
    """
    return DagsterGraphQLClient(
        utils.env(str, "GRAPHQL_HOST", default="dagster-dagit"),
        utils.env(int, "GRAPHQL_PORT", default=3000),
    )


class DagsterClient:
    def __init__(self):
        self.graphql_client = default_client()

    def trigger_run(
        self,
        job_name: str,
        repository_location_name: str,
        repository_name: str,
        run_config: dict,
        mode: str = "default",
    ) -> str:
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
