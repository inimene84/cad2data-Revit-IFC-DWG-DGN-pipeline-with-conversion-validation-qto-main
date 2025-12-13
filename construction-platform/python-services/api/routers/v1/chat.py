# Chat Router - Version 1 with Gemini AI Integration
# construction-platform/python-services/api/routers/v1/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not installed. Chat will use fallback responses.")

# Configure Gemini if available
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_AVAILABLE and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini AI configured successfully")
else:
    logger.warning("GEMINI_API_KEY not set. Chat will use fallback responses.")

# Chat history storage (in-memory)
chat_sessions: dict = {}


class ChatMessage(BaseModel):
    message: str
    context: Optional[dict] = None
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime
    ai_provider: str


# Construction-focused system prompt
SYSTEM_PROMPT = """You are a helpful Construction AI Assistant specializing in Estonian construction projects. 
You help with:
- Material takeoffs and quantity calculations
- Cost estimation using Estonian market prices
- BOQ (Bill of Quantities) generation
- Construction document analysis (IFC, DWG, PDF)
- Building regulations and standards in Estonia
- Project planning and scheduling

Always provide practical, actionable advice. When discussing costs, use EUR and reference Estonian suppliers and market conditions.
Be concise but thorough in your explanations."""


def get_fallback_response(message: str) -> str:
    """Provide fallback responses when Gemini is not available."""
    message_lower = message.lower()
    
    if "hello" in message_lower or "hi" in message_lower:
        return "Hello! I'm your Construction AI Assistant. I can help you with material takeoffs, cost estimation, and construction document analysis. How can I assist you today?"
    
    elif "material" in message_lower:
        return "For material analysis, please upload a construction document (PDF, IFC, DWG) through the File Upload page. I'll help extract material quantities and estimate costs based on current Estonian market prices."
    
    elif "cost" in message_lower or "price" in message_lower:
        return "I can help with cost estimation. Upload your project files and I'll calculate material costs using current Estonian prices. The system includes VAT (22%) and regional price adjustments for Tallinn, Tartu, and other areas."
    
    elif "boq" in message_lower or "report" in message_lower:
        return "To generate a BOQ (Bill of Quantities) report, first upload your construction documents. After processing, go to the Reports page to generate a comprehensive cost breakdown including materials, quantities, and supplier information."
    
    elif "upload" in message_lower or "file" in message_lower:
        return "You can upload construction files via the File Upload page. Supported formats include: PDF (drawings, specifications), IFC (BIM models), DWG (CAD drawings), and Excel spreadsheets with material lists."
    
    else:
        return "I'm here to help with your construction project. You can ask me about:\n• Material takeoffs and quantities\n• Cost estimation\n• BOQ generation\n• Document analysis\n• Estonian construction regulations\n\nFor best results, please upload your project files first."


@router.post("", response_model=ChatResponse)
async def send_message(chat_message: ChatMessage):
    """Send a message and get AI response."""
    session_id = chat_message.session_id or "default"
    
    # Initialize session if needed
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {
            "history": [],
            "created_at": datetime.now()
        }
    
    # Store user message
    chat_sessions[session_id]["history"].append({
        "role": "user",
        "content": chat_message.message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Generate response
    ai_provider = "fallback"
    response_text = ""
    
    if GEMINI_AVAILABLE and GEMINI_API_KEY:
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # Build conversation with system prompt
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {chat_message.message}"
            
            # Add context if provided
            if chat_message.context:
                context_str = "\n".join([f"{k}: {v}" for k, v in chat_message.context.items()])
                full_prompt = f"{SYSTEM_PROMPT}\n\nContext:\n{context_str}\n\nUser: {chat_message.message}"
            
            response = model.generate_content(full_prompt)
            response_text = response.text
            ai_provider = "gemini"
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            response_text = get_fallback_response(chat_message.message)
            ai_provider = "fallback"
    else:
        response_text = get_fallback_response(chat_message.message)
    
    # Store AI response
    chat_sessions[session_id]["history"].append({
        "role": "assistant",
        "content": response_text,
        "timestamp": datetime.now().isoformat()
    })
    
    return ChatResponse(
        response=response_text,
        session_id=session_id,
        timestamp=datetime.now(),
        ai_provider=ai_provider
    )


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session."""
    if session_id not in chat_sessions:
        return {"session_id": session_id, "history": []}
    
    return {
        "session_id": session_id,
        "history": chat_sessions[session_id]["history"],
        "created_at": chat_sessions[session_id]["created_at"].isoformat()
    }


@router.delete("/history/{session_id}", status_code=204)
async def clear_chat_history(session_id: str):
    """Clear chat history for a session."""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return None


@router.get("/status")
async def get_chat_status():
    """Get chat service status."""
    return {
        "gemini_available": GEMINI_AVAILABLE,
        "gemini_configured": bool(GEMINI_API_KEY),
        "active_sessions": len(chat_sessions),
        "provider": "gemini" if (GEMINI_AVAILABLE and GEMINI_API_KEY) else "fallback"
    }
