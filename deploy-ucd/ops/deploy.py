import io

from dagster import In, Out, op

import docker


@op
def build_deploy_image(context):
    client = docker.from_env()
    try:
        image, logs = client.images.build(
            path="../app",  # Path to your Flask app and Dockerfile
            tag="deploy-app:latest",
        )
        for log in logs:
            context.log.info(log.get("stream", "").strip())
        context.log.info(f"Successfully built image: {image.tags[0]}")
        return image.tags[0]
    except docker.errors.BuildError as e:
        context.log.error(f"Error building image: {e}")
        raise


@op(ins={"image_tag": In()})
def run_deploy_container(context, image_tag: str):
    client = docker.from_env()
    try:
        container = client.containers.run(
            image=image_tag,
            name="flask-container",
            ports={"5000/tcp": 5000},  # Map Flask default port
            detach=True,
        )
        context.log.info(f"Container started with ID: {container.id}")
        return container.id
    except docker.errors.ContainerError as e:
        context.log.error(f"Error starting container: {e}")
        raise
