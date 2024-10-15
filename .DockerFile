# We are using CUDA 12.6.0 runtime Ubuntu 22.04 as the base image
FROM nvidia/cuda:12.6.0-devel-ubuntu22.04

# Installing Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Installing required Python packages
RUN pip3 install \
    cudf-cu12 --extra-index-url=https://pypi.nvidia.com && \
    pip3 install datasets emoji nltk sentence_transformers grpcio grpcio-tools

# Copying the data and src folders to the Docker image
COPY proto/ /app/proto/
COPY data/ /app/data/
COPY src/ /app/src/

# Building Protobuf files
RUN python3 -m grpc_tools.protoc \
    -I/app/proto \
    --python_out=/app/src \
    --grpc_python_out=/app/src \
    /app/proto/opinion_analyzer.proto

# Setting the working directory
WORKDIR /app/src/

# Running the main.py file
CMD ["python3", "main.py"]