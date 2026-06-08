import grpc

import llm_pb2
import llm_pb2_grpc

channel=grpc.insecure_channel(
    "localhost:50053"
)

stub=llm_pb2_grpc.LLMServiceStub(
    channel
)

request=llm_pb2.GenerateRequest()

request.history.extend(
    [
        llm_pb2.LLMMessage(
            role="system",
            content="You are helpful"
        ),
        
            llm_pb2.LLMMessage(
            role="user",
            content="Explain grpc in one sentence"
        )


    ]
)

responses=stub.Generate(
    request
)

for response in responses:

    if response.completed:
        print("\n\n Done")

    else:

        print(response.token,
              end="",
              flush=True
              )
