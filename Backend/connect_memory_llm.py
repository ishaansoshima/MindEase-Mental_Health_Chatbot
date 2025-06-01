import os
from huggingface_hub import HfApi, HfFolder
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Configuration constants
HF_TOKEN = os.environ.get("HF_TOKEN2")
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
DB_FAISS_PATH = "vectorstore/deb_faiss"

def load_llm(huggingface_repo_id):
    """Initialize and return the HuggingFace LLM."""
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        huggingfacehub_api_token=HF_TOKEN,
        temperature=0.5,
        max_length=512,
        task="text-generation"
    )
    return llm

CUSTOM_PROMPT_TEMPLATE ="""
Use the provided context to answer the user's question with empathy, clarity, and accuracy. Prioritize these steps:

Understand & Relate: Acknowledge the user’s concern with compassion before answering.

Context-Based Response: Strictly use only the given context to formulate your answer. Do not speculate or add unsupported advice.

Humanized Tone: Respond in a warm, conversational, and supportive manner—avoid robotic or overly clinical language.

Safety & Transparency:

If the context doesn’t contain enough information, say: "I don’t have enough information to answer this, but I’m here to listen. Could you share more?"

For crisis situations (e.g., self-harm), gently guide the user to professional help (e.g., "This sounds really tough, and I care about your safety. Please reach out to [crisis hotline/trusted person] for support.").

Context: {context}
Question: {question}

Respond directly—no preambles or disclaimers.
"""

def set_custom_prompt():
    """Create and return a prompt template."""
    prompt = PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE,
        input_variables=["context", "question"]
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

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=load_llm(HUGGINGFACE_REPO_ID),
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={'k': 3}),
        return_source_documents=False,
        chain_type_kwargs={'prompt': set_custom_prompt()}
    )

    # Get user input and generate response
    while True:
        user_query = input("\nWrite Query Here (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
            
        try:
            response = qa_chain({'query': user_query})
            print("\nResponse:", response["result"])
        except Exception as e:
            print(f"Error processing query: {e}")

if __name__ == "__main__":
    main()