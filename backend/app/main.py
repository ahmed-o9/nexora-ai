from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .core.config import get_settings
from .core.logging import setup_logging
from .core.security import RequestIDMiddleware
from .core.exceptions import NexoraError
from .api import routes_teacher, routes_sessions, routes_quiz, routes_memory, routes_documents, routes_health

setup_logging()
app = FastAPI(title="Nexora", version="0.2.0")
s = get_settings()

app.add_middleware(RequestIDMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(NexoraError)
async def nexora_handler(request: Request, exc: NexoraError):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

for r in [routes_health, routes_teacher, routes_sessions, routes_quiz, routes_memory, routes_documents]:
    app.include_router(r.router)