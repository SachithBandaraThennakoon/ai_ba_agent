from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vector_db.company_knowledge import ensure_company_knowledge_loaded

app = FastAPI(title="Xceed AI Pre-Sales Agent")

@app.on_event("startup")
def startup_event():
    ensure_company_knowledge_loaded("company_docs")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://SachithBandaraThennakoon.github.io",        # GitHub Pages
        "https://www.xceed.live",           # Your domain (if any)
        "http://localhost:5173" ,
        "https://sachiththennakoon.com"
                  # Local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

