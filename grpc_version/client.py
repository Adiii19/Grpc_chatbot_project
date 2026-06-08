import grpc
import logging

import chatbot_pb2
import chatbot_pb2_grpc

def run():
    channel=grpc.insecure_channel(
    "localhost:50051"
       )

    stub=chatbot_pb2_grpc.ChatBotStub(
        channel
    )   


    while True:
        user_input=input("You :")

        if user_input.lower() =="exit":
            break

        request=chatbot_pb2.ChatRequest(
            message=user_input
        )

        response=stub.Chat(request)

        print("Bot:",response.reply)


if __name__=='__main__':
    run()
