from langchain_community.document_loaders import PyPDFLoader, TextLoader, JSONLoader
from typing import List, Dict, Any
from pathlib import Path
import json

class DocumentIngestionPipeline:
    """Pipeline for ingesting different types of documents."""
    
    def __init__(self):
        self.supported_extensions = {
            '.pdf': self._load_pdf,
            '.txt': self._load_text,
            '.json': self._load_json
        }
    
    def _load_pdf(self, file_path: str) -> List[Any]:
        """Load PDF documents."""
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    def _load_text(self, file_path: str) -> List[Any]:
        """Load text documents."""
        loader = TextLoader(file_path, encoding='utf-8')
        return loader.load()
    
    def _load_json(self, file_path: str) -> List[Any]:
        """Load JSON documents with intents, patterns, and responses."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            documents = []
            if 'intents' in data:
                for intent in data['intents']:
                    # Combine patterns and responses into a single text
                    patterns = ' '.join(intent.get('patterns', []))
                    responses = ' '.join(intent.get('responses', []))
                    text = f"Intent: {intent.get('tag', '')}\nPatterns: {patterns}\nResponses: {responses}"
                    
                    # Create a document with metadata
                    documents.append({
                        'page_content': text,
                        'metadata': {
                            'source': file_path,
                            'intent': intent.get('tag', ''),
                            'type': 'intent'
                        }
                    })
            return documents
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return []
    
    def process_file(self, file_path: str) -> List[Any]:
        """Process a single file based on its extension."""
        ext = Path(file_path).suffix.lower()
        if ext in self.supported_extensions:
            try:
                return self.supported_extensions[ext](file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                return []
        return [] 