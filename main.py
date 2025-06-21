from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
from connect_memory_ollama import load_llm, set_custom_prompt, OLLAMA_MODEL
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import os

app = FastAPI(title="MindEase API",
             description="API for MindEase Mental Health Chatbot",
             version="1.0.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the QA chain and memory
qa_chain = None
memory = None

class ChatMessage(BaseModel):
    sender: str
    text: str

class ChatRequest(BaseModel):
    message: str
    chat_history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str
    chat_history: List[Dict[str, str]]

def initialize_qa_chain():
    global qa_chain, memory
    
    # Initialize embedding model and load the vector database
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    try:
        db = FAISS.load_local(
            "vectorstore/deb_faiss",
            embedding_model,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        raise Exception(f"Error loading vector database: {e}")

    # Initialize conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # Create QA chain with memory
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=load_llm(OLLAMA_MODEL),
        retriever=db.as_retriever(search_kwargs={'k': 3}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": set_custom_prompt()}
    )

@app.on_event("startup")
async def startup_event():
    try:
        initialize_qa_chain()
        print("QA Chain initialized successfully")
    except Exception as e:
        print(f"Error initializing QA chain: {e}")
        raise

@app.get("/")
async def root():
    return {"message": "MindEase API is running"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    global qa_chain, memory
    
    if not qa_chain:
        try:
            initialize_qa_chain()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize QA chain: {str(e)}")
    
    try:
        # Clear previous conversation if starting new chat
        if not chat_request.chat_history:
            memory.clear()
        
        # Prepare chat history for the model
        model_chat_history = []
        for msg in chat_request.chat_history:
            if isinstance(msg, dict) and 'text' in msg and 'sender' in msg:
                role = "Human" if msg['sender'] == "user" else "AI"
                model_chat_history.append(f"{role}: {msg['text']}")
        
        # Get response from QA chain
        response = qa_chain({"question": chat_request.message, "chat_history": model_chat_history})
        
        # Format the response for the frontend
        updated_chat_history = chat_request.chat_history.copy()
        updated_chat_history.append({"sender": "user", "text": chat_request.message})
        updated_chat_history.append({"sender": "bot", "text": response["answer"]})
        
        return {
            "response": str(response["answer"]),
            "chat_history": updated_chat_history
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
