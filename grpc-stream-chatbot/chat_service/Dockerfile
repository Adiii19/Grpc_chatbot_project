FROM python:3.11-slim

WORKDIR /app

COPY chat_service/server.py .
COPY chat_service/chatbot.proto ./chatbot.proto
COPY llm_service/llm.proto ./llm.proto
COPY memory_service/memory.proto ./memory.proto

RUN pip install \
    grpcio \
    grpcio-tools

# Generate Python gRPC code from proto files at build time
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chatbot.proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. llm.proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. memory.proto

EXPOSE 50051

CMD ["python", "server.py"]