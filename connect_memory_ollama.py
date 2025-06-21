import os
import time
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Configuration constants
OLLAMA_MODEL = "qwen2.5:1.5b"  # Using a stable model
DB_FAISS_PATH = "vectorstore/deb_faiss"

def load_llm(model_name, max_retries=3):
    """Initialize and return the Ollama LLM with retry logic."""
    for attempt in range(max_retries):
        try:
            llm = Ollama(
                model=model_name,
                temperature=0.7,
            )
            # Test the connection with a simple prompt
            llm("test")
            return llm
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in 5 seconds...")
                time.sleep(5)
                # Restart Ollama service
                os.system("ollama stop > /dev/null 2>&1")
                time.sleep(2)
                os.system("ollama serve > /dev/null 2>&1 &")
                time.sleep(3)
            else:
                raise Exception(f"Failed to initialize LLM after {max_retries} attempts: {str(e)}")

CUSTOM_PROMPT_TEMPLATE ="""
Use the provided context and chat history to answer the user's question with empathy, clarity, and accuracy. Prioritize these steps:

Understand & Relate: Acknowledge the user's concern with compassion before answering.

Context-Based Response: Strictly use only the given context to formulate your answer. Do not speculate or add unsupported advice.

Humanized Tone: Respond in a warm, conversational, and supportive manner—avoid robotic or overly clinical language.

Safety & Transparency:

If the context doesn't contain enough information, say: "I don't have enough information to answer this, but I'm here to listen. Could you share more?"

For crisis situations (e.g., self-harm), gently guide the user to professional help (e.g., "This sounds really tough, and I care about your safety. Please reach out to [crisis hotline/trusted person] for support.").

Chat History:
{chat_history}

Context: {context}
Question: {question}

Respond directly—no preambles or disclaimers.
"""

def set_custom_prompt():
    """Create and return a prompt template."""
    prompt = PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE,
        input_variables=["context", "question", "chat_history"]
    )
    return prompt

def main():
    # Initialize embedding model and load the vector database
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    try:
        db = FAISS.load_local(
            DB_FAISS_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f"Error loading vector database: {e}")
        return

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
        combine_docs_chain_kwargs={
            'prompt': set_custom_prompt()
        },
        verbose=True
    )

    # Get user input and generate response
    print("\nWelcome to the Medical Chatbot! Type 'quit' to exit.")
    while True:
        user_query = input("\nWrite Query Here: ")
        if user_query.lower() == 'quit':
            break
            
        try:
            response = qa_chain({"question": user_query})
            print("\nResponse:", response["answer"])
        except Exception as e:
            print(f"Error processing query: {e}")

if __name__ == "__main__":
    main() 