from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv, find_dotenv
from document_loaders import DocumentIngestionPipeline
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

load_dotenv(find_dotenv())

# Configuration
data_path = 'data/'
db_faiss_path = 'vectorstore/deb_faiss'
metadata_path = 'vectorstore/document_metadata.json'

def get_file_hash(file_path):
    """Calculate hash of a file to detect changes."""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def load_metadata():
    """Load document metadata if it exists."""
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    """Save document metadata."""
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)

def file_loader(data_dir: str):
    """Load files and track their metadata."""
    pipeline = DocumentIngestionPipeline()
    metadata = load_metadata()
    new_metadata = {}
    new_documents = []
    
    # Walk through the directory and process all supported files
    for root, _, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if Path(file).suffix.lower() in pipeline.supported_extensions:
                file_hash = get_file_hash(file_path)
                last_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                
                # Check if document is new or modified
                if (file_path not in metadata or 
                    metadata[file_path]['hash'] != file_hash or 
                    metadata[file_path]['last_modified'] != last_modified):
                    
                    # Process the file
                    documents = pipeline.process_file(file_path)
                    new_documents.extend(documents)
                    
                    # Update metadata
                    new_metadata[file_path] = {
                        'hash': file_hash,
                        'last_modified': last_modified,
                        'processed_at': datetime.now().isoformat(),
                        'type': Path(file).suffix.lower()
                    }
    
    # Save updated metadata
    save_metadata(new_metadata)
    return new_documents

def chunk_creation(extracted_data):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

def get_embedding_model():
    """Initialize the embedding model."""
    embedding_model = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2'
    )
    return embedding_model

def main():
    # Initialize embedding model
    embedding_model = get_embedding_model()
    
    # Load and process new documents
    new_documents = file_loader(data_path)
    
    if not new_documents:
        print("No new or modified documents to process.")
        return
    
    print(f"Found {len(new_documents)} new or modified documents to process.")
    
    # Create chunks from new documents
    text_chunks = chunk_creation(extracted_data=new_documents)
    print(f"Created {len(text_chunks)} text chunks.")
    
    # Load existing FAISS database if it exists
    if os.path.exists(db_faiss_path):
        print("Loading existing vector database...")
        db = FAISS.load_local(db_faiss_path, embedding_model, allow_dangerous_deserialization=True)
        # Add new chunks to existing database
        print("Adding new documents to the database...")
        db.add_documents(text_chunks)
    else:
        print("Creating new vector database...")
        # Create new database if it doesn't exist
        db = FAISS.from_documents(text_chunks, embedding_model)
    
    # Save the updated database
    print("Saving vector database...")
    db.save_local(db_faiss_path)
    print(f"Successfully processed {len(new_documents)} documents.")

if __name__ == "__main__":
    main()
