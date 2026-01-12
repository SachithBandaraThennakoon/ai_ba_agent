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
    ensure_company_knowledge_loaded("company_docs")

# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://SachithBandaraThennakoon.github.io",
        "https://www.xceed.live",
        "https://sachiththennakoon.com",
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
def health_check():
    return {"status": "Xceed AI backend running"}
