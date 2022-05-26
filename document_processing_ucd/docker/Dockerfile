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
    python3-pip



WORKDIR /opt/dagster/app

# Add repository code
COPY ./ ./

# Install python dependencies
RUN pip --no-input install -r requirements.txt

# Run dagster gRPC server on port 4000
EXPOSE 4000

# CMD allows this to be overridden from run launchers or executors that want
# to run other commands against your repository
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4001", "-f", "main.py"]
