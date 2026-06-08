FROM python:3.11-slim

WORKDIR /app

COPY server.py .
COPY memory.proto ./memory.proto

RUN pip install\
        grpcio \
        grpcio-tools \
        redis

# Generate Python gRPC code from proto at build time
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. memory.proto

EXPOSE 50052

CMD ["python","server.py"]