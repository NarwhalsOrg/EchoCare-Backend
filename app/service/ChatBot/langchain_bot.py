from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

def get_ai_reply(patient_result: dict, chat_history: list, user_message: str) -> str:
    """
    Compose a system prompt with the patient_result and chat history, then get AI reply.
    """
    system_prompt = (
        "You are a helpful health assistant. "
        "Here is the patient's diabetes risk assessment:\n"
        f"{patient_result['prediction_label']}\n"
        "Explanation:\n" +
        "\n".join(patient_result['explanations']) +
        "\n\nAnswer the user's question based on this information."
    )
    messages = [HumanMessage(content=system_prompt)]
    for msg in chat_history:
        if msg["sender"] == "user":
            messages.append(HumanMessage(content=msg["message"]))
        else:
            messages.append(AIMessage(content=msg["message"]))
    messages.append(HumanMessage(content=user_message))
    llm = ChatOpenAI()  # Uses OPENAI_API_KEY from env
    ai_response = llm.invoke(messages)
    return ai_response.content
