import grpc

from concurrent import futures
import time
import logging

import chatbot_pb2
import chatbot_pb2_grpc

class ChatBotService(chatbot_pb2_grpc.ChatBotServicer):

    def Chat(self,request,context):
        message=request.message.lower()

        if "hello" in message:
            reply="Hi! How are you ?"

        elif "name" in message:
            reply="i am a grpc chatbot!!"

        else:
            reply=f"You said:{request.message}"

        return chatbot_pb2.ChatResponse(
            reply=reply
        )
    
def serve():
    server=grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    chatbot_pb2_grpc.add_ChatBotServicer_to_server(
        ChatBotService(),
        server
    )

    server.add_insecure_port("[::]:50051")

    server.start()

    print("Server running on prt 50051")

    server.wait_for_termination()

if __name__=='__main__':
    serve()

