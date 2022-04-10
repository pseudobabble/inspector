from dagster_graphql import DagsterGraphQLClient
from dagster_graphql import DagsterGraphQLClientError


class DagsterClient:

    def __init__(self, graphql_client: DagsterGraphQLClient = DagsterGraphQLClient(hostname="dagster-dagit", port_number=3000)):
        self.graphql_client = graphql_client

    def trigger_run(
            self,
            job_name: str,
            repository_location_name: str,
            repository_name:str,
            run_config: dict,
            mode: str ="default",
    ) -> None:
        try:
            new_run_id: str = self.graphql_client.submit_pipeline_execution(
                job_name,
                repository_location_name=repository_location_name,
                repository_name=repository_name,
                run_config=run_config,
                mode=mode
            )

            return new_run_id
        except DagsterGraphQLClientError as exc:
            raise exc
