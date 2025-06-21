# MindEase - Mental Health Chatbot

A compassionate AI-powered mental health companion that provides support and resources for mental well-being.

## Features

- Interactive chat interface
- AI-powered responses using Ollama
- Secure and private conversations
- Responsive design for all devices

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Ollama (for local AI model serving)

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd MindEase-Mental_Health_Chatbot
```

### 2. Install Dependencies

#### Backend (Python)

```bash
# Create and activate virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install Python dependencies
pip install -r requirements-minimal.txt
```

#### Frontend (React)

```bash
cd frontend
npm install
cd ..
```

### 3. Start Ollama

Make sure Ollama is installed and running:

```bash
# Start Ollama server (if not already running)
ollama serve

# In a separate terminal, pull the required model
ollama pull mistral  # or your preferred model
```

### 4. Start the Application

Make the startup script executable and run it:

```bash
# Make the script executable
chmod +x start.sh

# Start the application
./start.sh
```

The script will:
1. Start the FastAPI backend server on port 8001
2. Start the React development server on port 5175
3. Open the application in your default browser

## Accessing the Application

- **Frontend**: http://localhost:5175
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## Project Structure

```
MindEase-Mental_Health_Chatbot/
├── frontend/               # React frontend
│   ├── public/             # Static files
│   └── src/                # React source code
│       ├── components/      # React components
│       ├── services/        # API services
│       └── App.jsx         # Main App component
├── logs/                   # Application logs
├── main.py                 # FastAPI backend
├── connect_memory_ollama.py # AI model integration
├── requirements-minimal.txt # Python dependencies
└── start.sh                # Startup script
```

## Troubleshooting

- If you get port conflicts, you can change the ports in `start.sh`
- Check logs in the `logs/` directory for errors
- Make sure Ollama is running and the model is downloaded

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
