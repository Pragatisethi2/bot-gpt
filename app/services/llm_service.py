from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary(messages):
    try:
        message_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        prompt = f"""Summarize this conversation concisely in 2-3 sentences:

{message_text}

Summary:"""
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Summary Error: {e}")
        return "Previous conversation context."

def build_context_with_summary(summary, recent_messages):
    context = []
    
    if summary:
        context.append({
            "role": "user",
            "parts": [{"text": f"Previous conversation summary: {summary}"}]
        })
        context.append({
            "role": "model",
            "parts": [{"text": "I understand the context."}]
        })
    
    for msg in recent_messages:
        context.append({
            "role": msg["role"],
            "parts": [{"text": msg["content"]}]
        })
    
    return context

def call_gemini_chat(conversation_summary, messages):
    try:
        context = build_context_with_summary(conversation_summary, messages)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=context
        )
        
        return response.text
    except Exception as e:
        print(f"LLM Error: {e}")
        return "Sorry, I'm having trouble responding right now."

def call_gemini_rag(question, context, conversation_summary=None):
    try:
        prompt = f"""Context from documents: {context}

Question: {question}

Answer based only on the context above."""
        
        if conversation_summary:
            prompt = f"Previous conversation: {conversation_summary}\n\n" + prompt
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        
        return response.text
    except Exception as e:
        print(f"RAG Error: {e}")
        return "Sorry, I couldn't process your question."