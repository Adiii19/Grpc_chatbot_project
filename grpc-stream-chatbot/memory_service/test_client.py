import grpc

import memory_pb2
import memory_pb2_grpc

channel=grpc.insecure_channel(
    "localhost:50052"
)

stub=memory_pb2_grpc.MemoryServiceStub(
    channel
)

stub.SaveMessage(
    memory_pb2.SaveRequest(
        session_id="user1",
        role="user",
        content="hello"
    )
)

history=stub.GetHistory(

    memory_pb2.HistoryRequest(
        session_id="user1"
    )

)

# response=stub.DelHistory(
#     memory_pb2.HistoryRequest(
#         session_id="user1"
#     )
# )

# print(response.success)

for msg in history.messages:

    print(msg.session_id,msg.role,":",
    msg.content)
    