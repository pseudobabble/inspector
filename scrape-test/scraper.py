from dagster import job, op
import requests


@op
def get_data():
    return requests.get("https://jsonplaceholder.typicode.com/todos/1").json()


@op
def process_data(data: dict):
    if "title" in data:
        data["title"] = data["title"] + "_modified"

    return data


@job
def data_job():
    process_data(get_data())
