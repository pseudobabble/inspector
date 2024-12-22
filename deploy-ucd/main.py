"""This module is the top level for document processing pipeline code"""
from dagster import job, repository
from graphs.deploy import deploy_graph

# from dagster_mlflow import mlflow_tracking, end_mlflow_on_run_finished


deploy = deploy_graph.to_job()


@repository
def deploy():
    return [deploy]
