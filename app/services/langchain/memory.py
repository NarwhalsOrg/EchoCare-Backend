from langchain.memory import ConversationBufferMemory

# For demo: a single memory instance (use session_id for multi-user)
_memory_store = {}

def get_memory(session_id="default"):
    if session_id not in _memory_store:
        _memory_store[session_id] = ConversationBufferMemory(return_messages=True)
    return _memory_store[session_id]

def clear_memory(session_id="default"):
    if session_id in _memory_store:
        del _memory_store[session_id]
