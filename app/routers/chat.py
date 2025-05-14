from fastapi import APIRouter, HTTPException
from app.services.redis.session_store import get_session
from app.services.langchain.memory import get_memory
from app.schemas.chat import ChatMessage, ChatResponse
from langchain.chat_models import init_chat_model

router = APIRouter(tags=["Chatbot"])

# Initialize the model
model = init_chat_model(model="gemini-2.0-flash", model_provider="google_genai")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(chat_msg: ChatMessage):
    session_id = chat_msg.session_id

    # Get user data from Redis
    user_data = get_session(session_id)
    if not user_data:
        raise HTTPException(
            status_code=400,
            detail="User data is not available for this session. Please start with the health form."
        )

    # Get or create memory for the session
    memory = get_memory(session_id)

    # Compose prompt
    prompt = (
        f"Patient Info: {user_data}\n"
        f"User Question: {chat_msg.message}\n"
        "Provide a helpful, health-focused answer."
    )

    try:
        # Get response from model
        response = model.invoke(prompt)

        # Save context in memory (optional)
        memory.save_context({"input": chat_msg.message}, {"output": response.content})

        return ChatResponse(session_id=session_id, response=response.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
