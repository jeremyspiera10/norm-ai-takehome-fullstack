# Westeros Law Query System

This repository contains a client and server codebase for a legal compliance chatbot that can answer questions about Westeros laws by using AI to understand the query and retrieve relevant laws from the document.

## Prerequisites

- Docker
- OpenAI API Key
- Node.js (for frontend)

## Running the Application

### 1. Backend Setup (Docker)

1. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t norm-ai-takehome .
   docker run -p 8000:8000 --env OPENAI_API_KEY=your_openai_api_key norm-ai-takehome
   ```

3. The API will be available at `http://localhost:8000`
4. You can access the Swagger UI documentation at `http://localhost:8000/docs`

### 2. Frontend Setup

1. In a new terminal, navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or yarn dev
   ```

4. Visit http://localhost:3000 in your browser

### API Endpoints

- **GET /query**: Query the laws with a question
  - Query Parameters:
    - `query` (string, required): The question about laws

- **GET /test-docs**: Test endpoint to confirm document parsing is working

## How It Works

1. The system parses the laws from the PDF document
2. When a query is received, it uses OpenAI embeddings to find the most relevant laws
3. The system then formulates a response using a citation-based query engine
4. The response includes the answer to the question and citations of the relevant laws

## Implementation Details

- The `DocumentService` class parses the PDF and creates Document objects
- The `QdrantService` class connects to a in-memory Qdrant vector store, loads the documents, and handles queries
- FastAPI provides the HTTP endpoints
- The frontend offers a user-friendly interface for querying the laws

## Technical Stack

- **Backend**: Python, FastAPI, Llama Index, OpenAI, Qdrant
- **Frontend**: Next.js, Chakra UI, Tailwind CSS
- **Containerization**: Docker