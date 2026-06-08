from concurrent import futures
import grpc
import os


from groq import Groq

import llm_pb2
import llm_pb2_grpc
from dotenv import load_dotenv

load_dotenv()

client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

class LLMServiceImpl(
    llm_pb2_grpc.LLMServiceServicer
):
    def Generate(self,request,context):
        
        history=[]

        for msg in request.history:

            history.append(
                {
                    "role":msg.role,
                    "content":msg.content
                }
            )

        stream=client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=history,
            temperature=0.7,
            stream=True
        )

        for chunk in stream:

            if not chunk.choices:
                continue

            delta=(
            chunk.choices[0].delta
           )
            
            if(delta and delta.content):
                yield llm_pb2.TokenResponse(
                    token=delta.content,
                    completed=False
                )

        yield llm_pb2.TokenResponse(
            token="",
            completed=True
        )


def serve():

    server=grpc.server(
        futures.ThreadPoolExecutor(
            max_workers=10
        )
    )

    llm_pb2_grpc.add_LLMServiceServicer_to_server(
        LLMServiceImpl(),
        server
    )

    server.add_insecure_port(
        "[::]:50053"
    )

    server.start()

    print("LLM service Running on 50053")

    server.wait_for_termination()

if __name__=='__main__':
    serve()
