FROM ubuntu:20.04

# Basic provisioning
RUN apt-get update \
    && apt-get install -y software-properties-common\
    && apt-add-repository -y ppa:libreoffice \
    && apt-get update \
    && apt-get install -y libreoffice python3-pip python3-dev

# For polling upstream services
RUN apt-get install -y netcat

# Upgrade pip
RUN cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 --no-cache-dir install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r /backend/requirements.txt

# Copy polling entrypoint script & make executable
COPY ./docker/await_upstream.sh /start.sh
RUN chmod +x /start.sh

# Switch to the app directory
WORKDIR backend

# Start the server
ENTRYPOINT ["/start.sh"]
CMD ["python", "-u", "app.py"]
