from concurrent import futures
import grpc



import chatbot_pb2
import chatbot_pb2_grpc

import memory_pb2
import memory_pb2_grpc

import llm_pb2
import llm_pb2_grpc

memory_channel=grpc.insecure_channel(
    "memory-service:50052"
)

memory_stub=(
    memory_pb2_grpc.MemoryServiceStub(
        memory_channel
    )
)

llm_channel=grpc.insecure_channel(
    "llm-service:50053"
)

llm_stub=(
    llm_pb2_grpc.LLMServiceStub(
        llm_channel
    )
)




class ChatBotService(chatbot_pb2_grpc.ChatBotServicer):
    
    def ChatStream(self, request_iterator, context):
        history = [
            {
                "role": "system",
                "content": "you are a helpful assistant"
            }
        ]
        for request in request_iterator:

            session_id=(
                request.session_id
            )

            user_message =(
                request.message
            ) 

            print(
                f"\n[{session_id}] "
                f"{user_message}"
                
            )


            memory_stub.SaveMessage(

                memory_pb2.SaveRequest(
                    session_id=session_id,
                    role="user",
                    content=user_message
                )

            )
            
            history_response=(
                memory_stub.GetHistory(

                    memory_pb2.HistoryRequest(
                        session_id=session_id
                    )

                )
            )
            
            history=[]

            for msg in history_response.messages:

                history.append(
                    llm_pb2.LLMMessage(
                        role=msg.role,
                        content=msg.content
                    )
                )

            llm_request=(
                llm_pb2.GenerateRequest(
                    history=history
                )
            )

            try:
                responses=llm_stub.Generate(
                    llm_request
                )
                assistant_response = ""
                
                for response in responses:
                    if response.completed:
                        break
                    
                    assistant_response += response.token
                    yield chatbot_pb2.ChatResponse(
                        token=response.token,
                        completed=False
                    )
                
                # Save final response to memory
                memory_stub.SaveMessage(
                    memory_pb2.SaveRequest(
                        session_id=session_id,
                        role="assistant",
                        content=assistant_response
                    )
                )
                
                # Send completion signal
                yield chatbot_pb2.ChatResponse(
                    token="",
                    completed=True
                )
                
            except grpc.RpcError as e:
                # upstream LLM RPC error — send error and end stream
                yield chatbot_pb2.ChatResponse(
                    token=f"[LLM ERROR: {e.details()}]",
                    completed=True
                )
            except Exception as e:
                # any other error
                yield chatbot_pb2.ChatResponse(
                    token=f"[ERROR: {str(e)}]",
                    completed=True
                )

           
            


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chatbot_pb2_grpc.add_ChatBotServicer_to_server(ChatBotService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("streaming server started")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
