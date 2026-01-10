from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from api.main import app as fastapi_app

# Create a WSGI-compatible app
app = WSGIMiddleware(fastapi_app)
