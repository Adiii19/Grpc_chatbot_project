import json
import redis

redis_client=redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

SYSTEM_PROMPT={
    "role":"system",
    "content":"you are a helpful assistant"
}

def get_history(session_id):

    data =redis_client.get(session_id)

    if data :
        return json.loads(data)
    
    history=[SYSTEM_PROMPT]

    redis_client.set(session_id,
                     json.dumps(history),ex=86400)
    
    return history




def save_message(session_id,role,content):
    history=get_history(session_id)

    history.append(
        {
            "role":role,
            "content":content
        }
    )

    redis_client.set(
        session_id,
        json.dumps(history,ex=86400)
    )

def delete_session(session_id):

    redis_client.delete(
        session_id
    )

def get_sessions():
    return redis_client.keys("*")

def print_memory():

    print("\n == MEMORY STORE ==")

    for session_id,history in conversation_store.items():
        print(f"\n Session:{session_id}")
        

        for msg in history:
            print(msg)

    print("========================")

if __name__=='__main__':
    save_message(
        "user1",
        "user",
        "hello"
    )

    print(get_history(
        "user1"
    ))