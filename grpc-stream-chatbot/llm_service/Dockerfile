FROM python:3.11-slim

WORKDIR /app

COPY llm_service/server.py .
COPY llm_service/llm.proto ./llm.proto

RUN pip install \
    grpcio \
    grpcio-tools \
    groq \
    python-dotenv

# Generate Python gRPC code from proto at build time
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. llm.proto

EXPOSE 50053

CMD ["python", "server.py"]