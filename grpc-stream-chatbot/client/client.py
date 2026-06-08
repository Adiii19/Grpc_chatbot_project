import os
import sys

# Allow importing protobuf generated modules from the repository root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import grpc

import chatbot_pb2
import chatbot_pb2_grpc


def chat(session_id: str = "user1") -> None:
    channel = grpc.insecure_channel("localhost:50051")
    stub = chatbot_pb2_grpc.ChatBotStub(channel)

    def request_generator():
        while True:
            message = input("You: ")
            if message.strip().lower() in {"exit", "quit"}:
                break
            yield chatbot_pb2.ChatRequest(
                session_id=session_id,
                message=message,
            )

    responses = stub.ChatStream(request_generator())
    assistant_text = ""

    for response in responses:
        if response.completed:
            if assistant_text:
                print("\nAssistant:", assistant_text)
                assistant_text = ""
        else:
            assistant_text += response.token
            print(response.token, end="", flush=True)

    print("\n[chat session ended]")


if __name__ == "__main__":
    session = sys.argv[1] if len(sys.argv) > 1 else "user1"
    chat(session)
