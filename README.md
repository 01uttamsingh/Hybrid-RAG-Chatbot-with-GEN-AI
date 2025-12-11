

#  Hybrid RAG Chatbot (PDF + Google Gemini)

A smart **Retrieval-Augmented Generation (RAG)** chatbot that answers questions based on uploaded PDF documents.
It features a **Hybrid Mode**:

1.  **Document Mode:** If the answer is found in the PDFs, it answers strictly from the context.
2.  **General Mode:** If the answer is missing, it seamlessly switches to a "General Assistant" (configured as Indian Railways Support) to answer politely using General AI (Google Gemini).

-----

##  Features

  * **Hybrid Intelligence:** Uses a **Cosine Similarity Threshold (0.28)** to decide if a query matches the document or needs general AI.
  * **Vector Search:** Powered by **FAISS** (Facebook AI Similarity Search) for millisecond-speed retrieval.
  * **Embeddings:** Uses `all-MiniLM-L6-v2` (SentenceTransformers) for high-accuracy semantic search.
  * **Secure Frontend:** Built with **JS** & **DOMPurify** to prevent XSS attacks while rendering Markdown.
  * **No External DB Required:** Runs entirely locally using FAISS indices.

-----

##  Tech Stack

### Backend

  * **Framework:** FastAPI
  * **PDF Processing:** PyMuPDF (Fitz)
  * **Vector Database:** FAISS (CPU)
  * **LLM:** Google Gemini Flash
  * **Embeddings:** SentenceTransformers

### Frontend

  * **Core:** HTML5, CSS3, JavaScript
  * **Security:** DOMPurify (HTML Sanitization)
  * **Formatting:** Marked.js (Markdown to HTML)

-----

##  Project Structure

```text
/project-root
│
├── /dataset                # Stores PDFs & Database (Shared by Backend)
│   ├── /uploaded_pdfs      # Place your PDF files here
│   └── /vector_store       # Generated FAISS index & metadata
│
├── /backend                
│   ├── app.py              # Main FastAPI application entry point
│   ├── config.py           # Configuration & Environment variables
│   ├── gemini_client.py    # Handles interaction with Google Gemini API
│   ├── pdf_loader.py       # Extracts text & creates chunks from PDFs
│   ├── vector_store.py     # Handles Embeddings & FAISS Vector DB
│   ├── prompts.py          # System prompts for the AI
│   └── requirements.txt    # Python dependencies
│
├── /frontend               
│   ├── index.html          # Frontend UI
│   ├── style.css           # Styling
│   └── script.js           # Frontend Logic
│
└── README.md
```

-----

##  Installation & Setup

### 1\. Clone the Repository

```bash
git clone https://github.com/01uttamsingh/Hybrid-RAG-Chatbot-with-GEN-AI.git
cd Hybrid-RAG-Chatbot-with-GEN-AI
```

### 2\. Backend Setup

Navigate to the backend folder and set up the Python environment.

```bash
cd backend
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 3\. Set Up API Keys

Inside the `backend` folder, create a `.env` file and add your Google Gemini API key:

```ini
GEMINI_API_KEY=your_actual_api_key_here
```

### 4\. Add Your Documents

Go back to the root folder and open the `dataset` folder.
Place your PDF files inside `project-root/dataset/uploaded_pdfs`.
*(Note: If the folders don't exist, the code will automatically create them when you run it for vector_store)*.

-----

## Usage

### 1\. Start the Backend Server

Make sure you are inside the `backend` folder and your virtual environment is activated:

```bash
uvicorn app:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### 2\. Build the Knowledge Base (Run Once)

Before asking questions, you need to process the PDFs. Open your browser or Postman and visit:

```
http://127.0.0.1:8000/build
```

*You should see a JSON response: `{"status": "Vector database built successfully"}`*.

### 3\. Launch the Frontend

Navigate to the `frontend` folder and simply open `index.html` in your browser.

-----

##  How It Works (The Logic)

1.  **Ingestion:** The system reads PDFs, splits text into 400-word chunks (with overlap), and converts them into vectors.
2.  **Search:** When you ask a question, it calculates the **Cosine Similarity** between your question and the stored PDF vectors.
3.  **Decision Gate:**
      * **Score \> 0.28:** The system determines the answer is in the PDF. It retrieves the text and asks Gemini to answer *only* using that text.
      * **Score \< 0.28:** The system determines the PDF is irrelevant. It switches to "General Mode" and answers using general knowledge.

-----

##  Security Note

The frontend uses `DOMPurify` to sanitize the HTML response from the AI. This ensures that even if the AI generates malicious code (like `<script>`), it is stripped out before being rendered in the browser.

-----
