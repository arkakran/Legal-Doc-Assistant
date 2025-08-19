# ⚖️ Legal Document Assistant Pro

> An AI-powered legal research platform providing instant guidance on Indian law through advanced RAG architecture

![Legal Assistant](https://img.shields.io/badge/AI-Legal%20Assistant-blue?style=for-the-badge&logo=balance-scale)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

## ✨ Features

- 🤖 **AI-Powered Chat Interface** - Interactive legal guidance with LLaMA-3.3-70B
- 📚 **Comprehensive Legal Database** - 6 major Indian legal acts indexed
- 🔍 **Semantic Search** - Advanced FAISS vector database with precise retrieval
- 📱 **Modern UI** - Responsive chatbot with markdown rendering and source citations
- ⚡ **Real-time Processing** - Instant responses with thinking indicators
- 📄 **Document Coverage** - Consumer Protection, Income Tax, IPC, Motor Vehicle, CPC, Evidence Act

## 🚀 Quick Start

### Prerequisites
Python 3.8+

pip install -r requirements.txt

### Setup
1. **Clone the repository**


2. **Install dependencies**
pip install -r requirements.txt

3. **Configure environment**
Create .env file

GROQ_API_KEY=your_groq_api_key_here


4. **Run the application**
python app.py


5. **Access the app** at `http://localhost:7860`

## 🏗️ Architecture



|PDF Documents| ───▶│ Vector Database │───▶│ Chat Interface │

                       │ │ │
                       ▼ ▼ ▼
                       
Text Processing Semantic Search LLM Response
(Chunking + Embedding) (Sentence Transformers) (Groq + LLaMA)


## 📁 Project Structure

legal-document-assistant/

📂 data/ # Legal PDF documents

📂 static/ # CSS, JS assets

📂 templates/ # HTML templates

📂 utils/ # Core processing modules

📂 vector_store/ # FAISS index files

🐍 app.py # Main Flask application

📋 requirements.txt # Dependencies

📖 README.md # This file


## 🛠️ Tech Stack

**Backend** - Flask, LangChain 
**LLM** - LLaMA-3.3-70B (via Groq) 
**Vector DB** - FAISS HNSW 
**Embeddings** - Sentence Transformers 
**Frontend** - HTML, CSS, JS 
**Processing** - PyPDF, NumPy 

## 📊 Performance

- ⚡ **Query Response**: < 3 seconds
- 🎯 **Accuracy**: High precision with source citations
- 📈 **Scalability**: Optimized FAISS indexing
- 💾 **Memory**: Efficient embedding caching

## 🎨 Screenshots

### Chat Interface
- Modern full-screen design
- Real-time thinking indicators  
- Markdown-formatted responses
- Source citations with page numbers

### Key Features Demo
- Suggestion chips for quick queries
- Professional legal formatting
- Mobile-responsive design


## 🙏 Acknowledgments

- **Groq** for LLaMA API access
- **LangChain** for RAG framework
- **FAISS** for efficient vector search
- **Sentence Transformers** for embeddings

