"""This module is the top level for document processing pipeline code"""
from dagster import job, repository, op


@op
def success():
    1

@job()
def somejob():
    success()

@repository
def somerepo():
    return [
        somejob
    ]
