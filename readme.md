# BOT GPT - Conversational AI Backend

A production-grade conversational AI platform with LLM integration and RAG (Retrieval-Augmented Generation) support.

## 🎯 Features

- ✅ **Multi-turn Conversations** - Seamless chat experience with context management
- ✅ **Dual Modes** - Normal chat and document-based RAG mode
- ✅ **Progressive Summarization** - Automatic conversation compression every 15 messages
- ✅ **Document Intelligence** - Upload PDF/DOCX/TXT and chat with your documents
- ✅ **Advanced RAG** - Semantic search with cosine similarity and Gemini embeddings
- ✅ **User Management** - Unique email-based authentication
- ✅ **Conversation History** - Track and resume past conversations
- ✅ **Web Interface** - Professional frontend included

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLModel - SQL databases with Python type safety
- SQLite - Lightweight database

**AI/ML:**
- Google Gemini 2.5 Flash Lite - LLM for responses
- text-embedding-004 - Document embeddings
- NumPy - Cosine similarity for vector search
- PyPDF2 - PDF text extraction
- python-docx - DOCX processing

**Frontend:**
- Vanilla HTML/CSS/JavaScript
- Clean, responsive UI with modal interactions

## 📁 Project Structure
```
bot-gpt-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLModel schemas
│   ├── schemas.py           # Pydantic request/response models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── conversations.py # API endpoints
│   └── services/
│       ├── __init__.py
│       ├── llm_service.py   # Gemini integration
│       └── rag_service.py   # Embeddings & retrieval
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Unit tests (15 tests)
├── frontend.html            # Web interface
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🚀 Installation & Setup

### **Prerequisites:**
- Python 3.10+
- Google Gemini API key ([Get it here](https://ai.google.dev/))

### **1. Clone the repository:**
```bash
git clone <your-repo-url>
cd bot-gpt-backend
```

### **2. Create virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### **3. Install dependencies:**
```bash
pip install -r requirements.txt
```

### **4. Configure environment:**

Create `.env` file in project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./bot_gpt.db
```

### **5. Run the server:**
```bash
uvicorn app.main:app --reload
```

Server will start at: `http://localhost:8000`

## 🎨 Using the Application

### **Option 1: Web Interface (Recommended)**

1. Open `frontend.html` in your browser
2. Login with name and email
3. Click "**+ New Conversation**"
4. Choose conversation mode:
   - **💬 Normal Chat** - General AI conversation
   - **📄 Document Chat (RAG)** - Upload document and chat with it
5. Start chatting!

**Features:**
- View conversation history in sidebar
- Switch between conversations
- Upload documents (PDF, DOCX, TXT)
- Delete conversations
- Logout

### **Option 2: API (Postman/curl)**

**Interactive API Documentation:** `http://localhost:8000/docs`

#### **Example API Calls:**

**1. Create User:**
```bash
POST http://localhost:8000/api/users?name=John Doe&email=john@example.com
```

**Response:**
```json
{
  "user_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "message": "User created successfully"
}
```

---

**2. Create Chat Conversation:**
```bash
POST http://localhost:8000/api/conversations
Content-Type: application/json

{
  "user_id": 1,
  "first_message": "Hello!",
  "mode": "chat"
}
```

**Response:**
```json
{
  "conversation_id": 1,
  "response": "Hello! How can I help you today?"
}
```

---

**3. Send Message:**
```bash
POST http://localhost:8000/api/conversations/1/messages
Content-Type: application/json

{
  "content": "Tell me about artificial intelligence"
}
```

**Response:**
```json
{
  "response": "Artificial intelligence (AI) is..."
}
```

---

**4. Create RAG Conversation:**
```bash
POST http://localhost:8000/api/conversations
Content-Type: application/json

{
  "user_id": 1,
  "first_message": "I want to analyze a document",
  "mode": "rag"
}
```

---

**5. Upload Document (RAG):**
```bash
POST http://localhost:8000/api/conversations/2/documents
Content-Type: multipart/form-data

file: document.pdf
title: My Document
```

**Response:**
```json
{
  "status": "uploaded",
  "filename": "document.pdf",
  "title": "My Document",
  "chunks_count": 15,
  "embeddings_count": 15,
  "text_length": 7543
}
```

---

**6. Ask Question About Document:**
```bash
POST http://localhost:8000/api/conversations/2/messages
Content-Type: application/json

{
  "content": "What are the main points in the document?"
}
```

---

**7. List Conversations:**
```bash
GET http://localhost:8000/api/conversations?user_id=1
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Hello!",
    "mode": "chat",
    "created_at": "2025-11-30T10:00:00",
    "last_updated": "2025-11-30T10:15:00"
  },
  {
    "id": 2,
    "title": "I want to analyze a document",
    "mode": "rag",
    "created_at": "2025-11-30T11:00:00",
    "last_updated": "2025-11-30T11:30:00"
  }
]
```

---

**8. Get Conversation Details:**
```bash
GET http://localhost:8000/api/conversations/1
```

**Response:**
```json
{
  "conversation": {
    "id": 1,
    "title": "Hello!",
    "mode": "chat",
    "created_at": "2025-11-30T10:00:00"
  },
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Hello!",
      "timestamp": "2025-11-30T10:00:00"
    },
    {
      "id": 2,
      "role": "model",
      "content": "Hello! How can I help you today?",
      "timestamp": "2025-11-30T10:00:05"
    }
  ]
}
```

---

**9. Delete Conversation:**
```bash
DELETE http://localhost:8000/api/conversations/1
```

**Response:**
```json
{
  "status": "deleted"
}
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/users` | Create/login user |
| `GET` | `/api/users/{id}` | Get user details |
| `POST` | `/api/conversations` | Create conversation |
| `GET` | `/api/conversations` | List user conversations |
| `GET` | `/api/conversations/{id}` | Get conversation history |
| `POST` | `/api/conversations/{id}/messages` | Send message |
| `DELETE` | `/api/conversations/{id}` | Delete conversation |
| `POST` | `/api/conversations/{id}/documents` | Upload document (RAG) |
| `GET` | `/api/conversations/{id}/documents` | List conversation documents |

## 🧪 Running Tests
```bash
# Install test dependencies
pip install pytest httpx pytest-cov

# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=app

# Run specific test
python -m pytest tests/test_api.py::test_create_user -v
```

**Test Coverage:**
- ✅ User management (create, get, duplicate handling)
- ✅ Conversation CRUD operations
- ✅ Message sending (chat & RAG modes)
- ✅ Document upload functionality
- ✅ RAG without document (error handling)
- ✅ History compression (15 message trigger)
- ✅ Invalid conversation ID handling
- ✅ Conversation deletion

**Expected Output:**
```
15 passed in 8.45s
```

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────┐
│                    Client Layer                      │
│              (Browser / API Client)                  │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend                         │
│  ┌────────────────────────────────────────────────┐ │
│  │          API Routes Layer                      │ │
│  │  - User Management                             │ │
│  │  - Conversation Management                     │ │
│  │  - Message Handling                            │ │
│  │  - Document Upload                             │ │
│  └──────────────────┬─────────────────────────────┘ │
│                     ▼                                │
│  ┌────────────────────────────────────────────────┐ │
│  │          Service Layer                         │ │
│  │  ┌──────────────────┐  ┌───────────────────┐  │ │
│  │  │  LLM Service     │  │   RAG Service     │  │ │
│  │  │  - Chat mode     │  │  - Chunking       │  │ │
│  │  │  - Summarization │  │  - Embeddings     │  │ │
│  │  │  - Context mgmt  │  │  - Retrieval      │  │ │
│  │  └──────────────────┘  └───────────────────┘  │ │
│  └──────────────────┬─────────────────────────────┘ │
│                     ▼                                │
│  ┌────────────────────────────────────────────────┐ │
│  │     Data Layer (SQLite)                        │ │
│  │  - User                                        │ │
│  │  - Conversation                                │ │
│  │  - Message                                     │ │
│  │  - Document                                    │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │  Gemini API   │
              │  - LLM calls  │
              │  - Embeddings │
              └───────────────┘
```

## 🔍 Key Design Decisions

### **1. Progressive History Compression**
- **Trigger:** Every 15 messages
- **Method:** Gemini summarizes last 15 messages into concise summary
- **Storage:** Summary appended to `conversation.summary` field
- **Context Sent:** `[Summary] + [Last 10 messages]`
- **Benefit:** Scales to unlimited conversation length

### **2. RAG Implementation**
- **Chunking:** 500 words per chunk
- **Embeddings:** Google text-embedding-004 (768 dimensions)
- **Retrieval:** Cosine similarity with NumPy
- **Top-K:** Returns 3 most relevant chunks
- **Context:** Relevant chunks + user question sent to Gemini

### **3. Database Schema**
```sql
User
  - id (PK)
  - name
  - email (UNIQUE)
  - created_at

Conversation
  - id (PK)
  - user_id (FK → User)
  - title
  - mode (chat/rag)
  - summary (TEXT)
  - created_at
  - last_updated

Message
  - id (PK)
  - conversation_id (FK → Conversation)
  - role (user/model)
  - content
  - timestamp

Document
  - id (PK)
  - conversation_id (FK → Conversation)
  - title
  - text
  - chunks (JSON)
  - embeddings (JSON)
  - created_at
```

### **4. Error Handling**
- **LLM API timeout:** Graceful fallback with retry logic
- **Database failures:** Transaction rollbacks
- **Missing documents:** Clear error message for RAG mode
- **Invalid requests:** HTTP 404/400 with descriptive errors

## 🌟 Bonus Features Implemented

- ✅ Progressive conversation summarization (every 15 messages)
- ✅ Semantic search with cosine similarity
- ✅ Document upload (PDF, DOCX, TXT)
- ✅ Professional web interface with modal dialogs
- ✅ Unit tests (15 comprehensive tests)
- ✅ Unique email validation
- ✅ Conversation history tracking
- ✅ Delete conversation functionality
- ✅ Dual-mode support (Chat & RAG)

## 📝 Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ Yes | `AIza...` |
| `DATABASE_URL` | SQLite database path | ✅ Yes | `sqlite:///./bot_gpt.db` |

## 🔒 Security Notes

- Email-based user identification (unique constraint)
- No password storage (suitable for demo/assignment)
- API key stored securely in environment variables
- CORS enabled for frontend access
- Input validation on all endpoints

## 🚧 Future Enhancements

- JWT-based authentication
- Multiple documents per conversation
- File type validation & size limits
- Token usage tracking & cost estimation
- Rate limiting per user
- Conversation export (PDF/JSON)
- Multi-language support
- WebSocket for real-time updates
- Vector database (Pinecone/Weaviate) for production scale

## 🐛 Known Limitations

- SQLite not suitable for production scale (use PostgreSQL)
- In-memory RAG retrieval (consider vector DB for 1000+ documents)
- No user session management
- Single LLM provider (Gemini only)

choco install graphviz

## 📄 License

This project is created as a case study assignment for BOT Consulting.

## 👤 Author

**Pragati Sethi**
- Email: pragatisethi2@gmail.com


## 🙏 Acknowledgments

- Google Gemini API for LLM capabilities
- FastAPI for excellent web framework
- SQLModel for elegant ORM
- NumPy for vector operations

---
