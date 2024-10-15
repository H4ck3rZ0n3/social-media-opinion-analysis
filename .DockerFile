# We are using CUDA 12.6.0 runtime Ubuntu 22.04 as the base image
FROM nvidia/cuda:12.6.0-devel-ubuntu22.04

# Installing Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Installing required Python packages
RUN pip3 install \
    cudf-cu12 --extra-index-url=https://pypi.nvidia.com && \
    pip3 install datasets emoji nltk sentence_transformers

# Copying the data and src folders to the Docker image
COPY data/ /app/data/
COPY src/ /app/src/

# Setting the working directory
WORKDIR /app/src/

# Running the main.py file
CMD ["python3", "main.py"]