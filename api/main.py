from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vector_db.company_knowledge import ensure_company_knowledge_loaded

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

