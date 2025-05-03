from app.service.ml.predict import predict_and_explain
from app.service.ChatBot.langchain_bot import get_ai_reply
from app.controllers.ChatControllers import create_chat_message, get_chat_history
from app.core.database import SessionLocal

import json

def register_socketio_events(sio):

    @sio.event
    async def connect(sid, environ):
        print(f"Socket.IO: Client connected: {sid}")

    @sio.event
    async def disconnect(sid):
        print(f"Socket.IO: Client disconnected: {sid}")

    @sio.event
    async def chat_message(sid, data):
        """
        Expected data:
        {
            "user_id": "abc123",
            "session_id": "xyz789",
            "message": "What can I do to reduce my risk?",
            "patient_data": { ...all 21 fields... }
        }
        """
        db = SessionLocal()
        user_id = data["user_id"]
        session_id = data["session_id"]
        user_message = data["message"]
        patient_data = data["patient_data"]

        # Save user message to DB
        create_chat_message(db, user_id, session_id, user_message, "user")

        # Get prediction and explanation
        patient_result = predict_and_explain(patient_data)

        # Get chat history for session
        history_objs = get_chat_history(db, user_id, session_id)
        chat_history = [
            {"sender": msg.sender, "message": msg.message}
            for msg in history_objs
        ]

        # Generate AI reply
        ai_reply = get_ai_reply(patient_result, chat_history, user_message)

        # Save AI reply to DB
        create_chat_message(db, user_id, session_id, ai_reply, "ai")

        await sio.emit("chat_response", {
            "ai_reply": ai_reply,
            "patient_result": patient_result,
            "chat_history": chat_history + [{"sender": "user", "message": user_message}, {"sender": "ai", "message": ai_reply}]
        }, to=sid)

        db.close()
