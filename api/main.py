from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from uuid import uuid4

from agents.client_agent import client_agent
from memory.persistent_memory import PersistentSessionMemory
from vector_db.company_knowledge import ensure_company_knowledge_loaded

# --------------------------------------------------
# CREATE FASTAPI APP (FIRST!)
# --------------------------------------------------
app = FastAPI(title="Xceed AI Pre-Sales Agent")

# --------------------------------------------------
# STARTUP EVENT
# --------------------------------------------------
@app.on_event("startup")
def startup_event():
    try:
        ensure_company_knowledge_loaded("company_docs")
        print("✅ Company knowledge loaded")
    except Exception as e:
        print("❌ Startup error:", str(e))

# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://SachithBandaraThennakoon.github.io",
        "https://www.xceed.live",
        "https://sachiththennakoon.com",
        "https://www.sachiththennakoon.com"
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# DATA MODELS
# --------------------------------------------------
class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str

# --------------------------------------------------
# SESSION STORE
# --------------------------------------------------
sessions = {}

# --------------------------------------------------
# CHAT API
# --------------------------------------------------
@app.post("/chat")
def chat(req: ChatRequest):
    if req.session_id and req.session_id in sessions:
        session = sessions[req.session_id]
        session_id = req.session_id
    else:
        session_id = str(uuid4())
        session = PersistentSessionMemory(session_id)
        sessions[session_id] = session

    reply, confirmed = client_agent(session, req.message)

    return {
        "session_id": session_id,
        "reply": reply,
        "confirmed": confirmed
    }

# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------
@app.get("/")
def health():
    return {"status": "Xceed AI backend running"}

# --------------------------------------------------
# CHAT UI
# --------------------------------------------------
templates = Jinja2Templates(directory="templates")

@app.get("/chat-ui", response_class=HTMLResponse)
def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
