Multilingual IP & Regulatory AI Assistant

A RAG-based AI assistant that provides IP and regulatory information using a PDF knowledge base.

## Features

- National and International regulatory information
- Multilingual question answering
- PDF-based knowledge retrieval
- AI-generated answers
- Source/document references
- FastAPI backend
- React frontend
- Swagger API documentation

## Technologies Used

- Python
- FastAPI
- React
- RAG (Retrieval-Augmented Generation)
- Vector Database
- LLM
- PDF Documents

## Project Structure

```text
project/
│
├── main.py
├── backend/
│   ├── api/
│   │   └── chat.py
│   ├── rag/
│   │   └── retriever.py
│   └── llm/
│       └── generator.py
│
├── frontend/
├── data/
│   └── pdfs/
├── requirements.txt
└── README.md
How It Works
User Question
     ↓
Select Language
     ↓
Select National / International
     ↓
FastAPI
     ↓
Document Retrieval
     ↓
Relevant PDF Content
     ↓
LLM
     ↓
Answer + Sources
National / International
The system supports two regulatory scopes:
National – retrieves national/India-related documents.
International – retrieves international/WHO-related documents.
The selected scope is passed to the retriever so that the correct documents are searched.
Run Backend
Install dependencies:
pip install -r requirements.txt
Start the FastAPI server:
uvicorn main:app --reload
Backend:
http://127.0.0.1:8000
Swagger API:
http://127.0.0.1:8000/docs
Health check:
http://127.0.0.1:8000/health
Run Frontend
Go to the frontend folder:
cd frontend
Install dependencies:
npm install
Run the frontend:
npm run dev
Example
Input
Scope: International
Language: English

Question:
What are the international regulations for Ayurveda?
Output
Answer:
International regulatory information based on the available documents.

Sources:
05_Ayurveda_International_Regulation_and_WHO.pdf
Important
The PDF documents must contain the correct metadata:
National
International
This ensures that National questions retrieve National documents and International questions retrieve International documents.
Disclaimer
This AI assistant provides information based on the available knowledge base. It should not be considered a replacement for professional legal or regulatory advice.