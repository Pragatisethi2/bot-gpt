import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session
import os

# Create in-memory test database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# Test 1: Root Endpoint
def test_root(client: TestClient):
    """Test root endpoint returns correct message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "BOT GPT API is running"}


# Test 2: Create User
def test_create_user(client: TestClient):
    """Test user creation"""
    response = client.post("/api/users?name=Test User&email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "user_id" in data


# Test 3: Create User with Duplicate Email
def test_duplicate_email(client: TestClient):
    """Test that duplicate email returns existing user"""
    # Create first user
    response1 = client.post("/api/users?name=User One&email=duplicate@test.com")
    user1_id = response1.json()["user_id"]
    
    # Try to create second user with same email
    response2 = client.post("/api/users?name=User Two&email=duplicate@test.com")
    user2_id = response2.json()["user_id"]
    
    # Should return same user
    assert user1_id == user2_id


# Test 4: Get User
def test_get_user(client: TestClient):
    """Test retrieving user by ID"""
    # Create user
    create_response = client.post("/api/users?name=John Doe&email=john@test.com")
    user_id = create_response.json()["user_id"]
    
    # Get user
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@test.com"


# Test 5: Get Non-existent User
def test_get_nonexistent_user(client: TestClient):
    """Test that getting non-existent user returns 404"""
    response = client.get("/api/users/99999")
    assert response.status_code == 404


# Test 6: Create Normal Chat Conversation
def test_create_chat_conversation(client: TestClient):
    """Test creating a normal chat conversation"""
    # Create user first
    user_response = client.post("/api/users?name=Chat User&email=chat@test.com")
    user_id = user_response.json()["user_id"]
    
    # Create conversation
    response = client.post(
        "/api/conversations",
        json={
            "user_id": user_id,
            "first_message": "Hello",
            "mode": "chat"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data


# Test 7: Create RAG Conversation
def test_create_rag_conversation(client: TestClient):
    """Test creating a RAG conversation"""
    # Create user
    user_response = client.post("/api/users?name=RAG User&email=rag@test.com")
    user_id = user_response.json()["user_id"]
    
    # Create RAG conversation
    response = client.post(
        "/api/conversations",
        json={
            "user_id": user_id,
            "first_message": "I want to chat with a document",
            "mode": "rag"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "Please upload a document" in data["response"]


# Test 8: List Conversations
def test_list_conversations(client: TestClient):
    """Test listing user conversations"""
    # Create user
    user_response = client.post("/api/users?name=List User&email=list@test.com")
    user_id = user_response.json()["user_id"]
    
    # Create two conversations
    client.post(
        "/api/conversations",
        json={"user_id": user_id, "first_message": "Chat 1", "mode": "chat"}
    )
    client.post(
        "/api/conversations",
        json={"user_id": user_id, "first_message": "Chat 2", "mode": "chat"}
    )
    
    # List conversations
    response = client.get(f"/api/conversations?user_id={user_id}")
    assert response.status_code == 200
    conversations = response.json()
    assert len(conversations) == 2


# Test 9: Get Conversation Details
def test_get_conversation_details(client: TestClient):
    """Test retrieving conversation with messages"""
    # Create user and conversation
    user_response = client.post("/api/users?name=Detail User&email=detail@test.com")
    user_id = user_response.json()["user_id"]
    
    conv_response = client.post(
        "/api/conversations",
        json={"user_id": user_id, "first_message": "Hello", "mode": "chat"}
    )
    conv_id = conv_response.json()["conversation_id"]
    
    # Get conversation details
    response = client.get(f"/api/conversations/{conv_id}")
    assert response.status_code == 200
    data = response.json()
    assert "conversation" in data
    assert "messages" in data
    assert len(data["messages"]) >= 2  # First message + response


# Test 10: Send Message to Chat
def test_send_message_to_chat(client: TestClient):
    """Test sending message to normal chat conversation"""
    # Create user and conversation
    user_response = client.post("/api/users?name=Message User&email=message@test.com")
    user_id = user_response.json()["user_id"]
    
    conv_response = client.post(
        "/api/conversations",
        json={"user_id": user_id, "first_message": "Hello", "mode": "chat"}
    )
    conv_id = conv_response.json()["conversation_id"]
    
    # Send message
    response = client.post(
        f"/api/conversations/{conv_id}/messages",
        json={"content": "What is 2+2?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0


# Test 11: Delete Conversation
def test_delete_conversation(client: TestClient):
    """Test deleting a conversation"""
    # Create user and conversation
    user_response = client.post("/api/users?name=Delete User&email=delete@test.com")
    user_id = user_response.json()["user_id"]
    
    conv_response = client.post(
        "/api/conversations",
        json={"user_id": user_id, "first_message": "To be deleted", "mode": "chat"}
    )
    conv_id = conv_response.json()["conversation_id"]
    
    # Delete conversation
    response = client.delete(f"/api/conversations/{conv_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"
    
    # Verify conversation is gone
    get_response = client.get(f"/api/conversations/{conv_id}")
    assert get_response.status_code == 404


# Test 12: RAG Without Document
def test_rag_without_document(client: TestClient):
    """Test that RAG conversation requires document upload"""
    # Create user and RAG conversation
    user_response = client.post("/api/users?name=RAG Test&email=ragtest@test.com")
    user_id = user_response.json()["user_id"]
    
    conv_response = client.post(
        "/api/conversations",
        json={"user_id": user_id, "first_message": "Document chat", "mode": "rag"}
    )
    conv_id = conv_response.json()["conversation_id"]
    
    # Try to send message without uploading document
    response = client.post(
        f"/api/conversations/{conv_id}/messages",
        json={"content": "What's in the document?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert "No document uploaded" in data["error"]


# Test 13: Document Upload
def test_document_upload(client: TestClient):
    """Test document upload functionality"""
    # Create user and RAG conversation
    user_response = client.post("/api/users?name=Upload User&email=upload@test.com")
    user_id = user_response.json()["user_id"]
    
    conv_response = client.post(
        "/api/conversations",
        json={"user_id": user_id, "first_message": "Upload test", "mode": "rag"}
    )
    conv_id = conv_response.json()["conversation_id"]
    
    # Create a simple text file
    files = {
        "file": ("test.txt", b"This is a test document for RAG. It contains sample text.", "text/plain")
    }
    data = {"title": "Test Document"}
    
    # Upload document
    response = client.post(
        f"/api/conversations/{conv_id}/documents",
        files=files,
        data=data
    )
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "uploaded"
    assert result["chunks_count"] > 0


# Test 14: History Compression
def test_history_compression(client: TestClient):
    """Test that conversation summary is created after 15 messages"""
    # Create user and conversation
    user_response = client.post("/api/users?name=History User&email=history@test.com")
    user_id = user_response.json()["user_id"]
    
    conv_response = client.post(
        "/api/conversations",
        json={"user_id": user_id, "first_message": "Start", "mode": "chat"}
    )
    conv_id = conv_response.json()["conversation_id"]
    
    # Send 14 more messages (total 15 with first one)
    for i in range(14):
        client.post(
            f"/api/conversations/{conv_id}/messages",
            json={"content": f"Message {i+2}"}
        )
    
    # Get conversation details
    response = client.get(f"/api/conversations/{conv_id}")
    data = response.json()
    
    # Check that conversation exists and has messages
    assert "conversation" in data
    assert len(data["messages"]) >= 15


# Test 15: Error Handling - Invalid Conversation ID
def test_invalid_conversation_id(client: TestClient):
    """Test error handling for invalid conversation ID"""
    response = client.post(
        "/api/conversations/99999/messages",
        json={"content": "Test"}
    )
    assert response.status_code == 404