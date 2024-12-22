from dagster import graph
from ops.deploy import build_deploy_image, run_deploy_container


@graph
def deploy_graph():
    image_tag = build_deploy_image()
    run_deploy_container(image_tag)
