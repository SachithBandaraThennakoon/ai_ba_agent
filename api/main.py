from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vector_db.company_knowledge import ensure_company_knowledge_loaded

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request


from uuid import uuid4
from agents.client_agent import client_agent
from memory.persistent_memory import PersistentSessionMemory

sessions = {}

@app.post("/chat")
def chat(req: ChatRequest):
    # Session handling
    if req.session_id and req.session_id in sessions:
        session = sessions[req.session_id]
        session_id = req.session_id
    else:
        session_id = str(uuid4())
        session = PersistentSessionMemory(session_id)
        sessions[session_id] = session

    # Agent response
    reply, confirmed = client_agent(session, req.message)

    # 🔥 IMPORTANT: reply key MUST exist
    return {
        "session_id": session_id,
        "reply": reply,
        "confirmed": confirmed
    }



# --------------------------------------------------
# CREATE SINGLE FASTAPI APP (ONLY ONCE)
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
        "http://localhost:5173",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# HEALTH CHECK (VERY IMPORTANT FOR AZURE)
# --------------------------------------------------
@app.get("/")
def health():
    return {"status": "Xceed AI backend running"}



templates = Jinja2Templates(directory="templates")

@app.get("/chat-ui", response_class=HTMLResponse)
def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

