FROM ubuntu:20.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y tzdata \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    default-jre \
    libreoffice-java-common \
    libreoffice-common \
    libreoffice \
    libreoffice-writer \
    python3.8 \
    python3-pip \
    libcairo2 \
    libcairo2-dev


WORKDIR /opt/dagster/app

# Copy dependencies conf repository code
COPY ./requirements.txt ./requirements.txt
COPY ./infrastructure-1.0.0-py3-none-any.whl ./infrastructure-1.0.0-py3-none-any.whl

# Install python dependencies
RUN pip --no-input install -r requirements.txt

# Pull the source code
COPY ./ ./

# Run dagster gRPC server on port 4000
EXPOSE 4000

# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4002", "-f", "main.py"]
