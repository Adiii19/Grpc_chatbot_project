from concurrent import futures
import grpc
import json
import redis

import memory_pb2
import memory_pb2_grpc

redis_client=redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

SYSTEM_PROMPT={
    "role":"system",
    "content":"You are a hepful AI assistant",
    "session_id":"system"
}

class MemoryServiceImpl(memory_pb2_grpc.MemoryServiceServicer):
    def SaveMessage(
        self,
        request,
        context
    ):
        session_id=request.session_id

        history_json=redis_client.get(
            session_id
        )

        if history_json:
            history=json.loads(
                history_json
            )

        else:
            history=[SYSTEM_PROMPT]

        history.append(
            {
                "role":request.role,
                "content":request.content,
                "session_id":request.session_id
            }
        )

        redis_client.set(
            session_id,
            json.dumps(history),
            ex=86400
        )

        return memory_pb2.SaveResponse(
            success=True
        )
    
    def GetHistory(
            self,
            request,
            context
    ):
        session_id=request.session_id

        history_json=redis_client.get(session_id)

        if history_json:
            history=json.loads(
                history_json
            )
        else:
            history=[SYSTEM_PROMPT]

        messages=[]

        for item in history:
            messages.append(
                memory_pb2.ChatMessage(
                    role=item.get("role", ""),
                    content=item.get("content", ""),
                    session_id=item.get("session_id", "")
                )
            )

        return memory_pb2.HistoryResponse(
            messages=messages,
        )
    
    def DelHistory(
            self,
            request,
            context
    ):
        session_id=request.session_id

        deleted=redis_client.delete(session_id)

        return memory_pb2.SaveResponse(
            success=bool(deleted)
        ) 
        

def serve():

    server=grpc.server(
        futures.ThreadPoolExecutor(
            max_workers=10
        )
    )

    memory_pb2_grpc.add_MemoryServiceServicer_to_server(
        MemoryServiceImpl(),
        server
    )

    server.add_insecure_port(
        "[::]:50052"
    )

    server.start()

    print("Memory Service Running on 50052")

    server.wait_for_termination()

if __name__=="__main__":
    serve()